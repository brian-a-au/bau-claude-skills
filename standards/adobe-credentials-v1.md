# Adobe credentials standard, version 1

This standard says how the Adobe tooling repos find, check, show and protect an Adobe OAuth Server-to-Server credential. It covers these tools:

- aa_auto_sdr
- aa-health-duckdb
- cja_auto_sdr
- cja-audit-log-monitor
- sdr-visualizer
- sdr-grader

The standard is a target. It does not describe any one tool as it is today. Each tool repo has a `known-differences.json` file that lists the rules the tool does not meet yet. The shape of that file is in [`schemas/known-differences-v1.schema.json`](schemas/known-differences-v1.schema.json).

The shared test cases are in [`cases/adobe-credentials-v1/`](cases/adobe-credentials-v1/). Each case names the rule it tests. [`cases/README.md`](cases/README.md) explains how a tool runs them.

## Words used here

- **Credential.** The four fields `org_id`, `client_id`, `secret` and `scopes`.
- **Source.** One place a credential can come from, e.g., a profile.
- **Product.** `aa` for Adobe Analytics tools and `cja` for Customer Journey Analytics tools.
- **Notice.** One line on stderr that says a later release will act differently. A notice never changes the result of the run.

## The three levels

The rules have three levels. The levels are ordered by how much a rule can change for a person who already uses a tool.

- **Level 1, safety.** Every tool meets these rules in its next release. None of them changes which credential a tool uses.
- **Level 2, visibility.** Every tool meets these rules in its next release. They add output and options, and they change no lookup result.
- **Level 3, strict lookup.** These rules can change which credential a tool uses. A tool first ships a release that prints a notice when the rule would change the result. It applies the rule in its next breaking release.

## Level 1: safety

### L1.1 No part of a secret is printed

A tool never prints any character of the secret. This covers logs, errors, machine output, exception text and the arguments of a child process.

- A secret that is set is shown as `****`. The four stars have a fixed length, so they do not show how long the secret is.
- Machine output reports the secret as a true or false value named `secret_set`.
- A tool that passes a credential to a worker or a child process uses the environment or a file path, never the command line.

### L1.2 The client ID is masked one way

A tool shows the first 4 characters of the client ID, then `****`, then the last 4 characters, e.g., `1a2b****9y0z`. A client ID of 8 characters or fewer is shown as `****`. Each tool has one function that does this, and every place that shows a client ID calls it.

### L1.3 Files are private

- A file that a tool writes with a credential in it has mode 0600.
- A folder that a tool creates for credentials has mode 0700. A folder that already exists is left as it is.
- When a tool reads a credential file that the group or other users can read, it prints one warning per run. It checks the target of a symlink, not the link.
- These checks are skipped on Windows, where the mode bits do not describe access.

### L1.4 Profile names are checked

A profile name holds letters, digits, dots, underscores and hyphens only. It starts with a letter or a digit, and it is 64 characters or fewer. A tool checks the name before it builds a path, on read and on write, so a name cannot point outside the profiles folder.

## Level 2: visibility

### L2.1 Fields

The credential fields are `org_id`, `client_id`, `secret` and `scopes`.

- File keys are lower case.
- A key that the tool does not know is ignored, with one debug log line that names the key.
- `scopes` is copied exactly as the Adobe Developer Console shows it. A tool does not add, remove or reorder scopes.
- `sandbox` is optional. The CJA tools read it. The Analytics tools accept it in a file and ignore it.
- The Analytics company is not a credential field, because one credential can see several companies.

### L2.2 Variable names

The environment variables are `ORG_ID`, `CLIENT_ID`, `SECRET` and `SCOPES`. aa-health-duckdb keeps its `AHD_ORG_ID`, `AHD_CLIENT_ID`, `AHD_SECRET` and `AHD_SCOPES` names as well.

### L2.3 Profiles stay per product

- Analytics tools share `~/.aa/orgs/<name>/`.
- CJA tools share `~/.cja/orgs/<name>/`.

A profile folder holds `config.json`. The two folders are not merged, because an Analytics credential and a CJA credential often differ in APIs, product profiles and scopes.

### L2.4 A config check that does not call Adobe

Each tool has a command that reports how it would find the credential, without a network call. The command reports these things:

- Every source that supplied a value, with the path of each file.
- Every source that was skipped because it was partial, with the names of the missing fields.
- The profile, when one is used.
- The client ID, masked as in L1.2.
- Whether the secret is set.
- The scopes.
- Any problems, e.g., a missing field. The problem codes are in [`codes-v1.json`](codes-v1.json) under `errors`.
- Any notices from Level 3.

The command has a JSON output. The shape is the same in every tool and is in [`schemas/config-check-v1.schema.json`](schemas/config-check-v1.schema.json).

### L2.5 A live test with two results

Each tool that calls Adobe has a command that tests the credential. The command reports two results separately, because one can pass while the other fails.

- **Sign-in.** The tool asks Adobe's sign-in service for a token.
- **Product access.** The tool makes one call to the product with that token.

The command has a JSON output. The shape is in [`schemas/live-test-v1.schema.json`](schemas/live-test-v1.schema.json).

A failed result has a code from the `codes` list in [`codes-v1.json`](codes-v1.json). A tool reports only the codes it can detect. For any other sign-in failure it reports `sign_in_failed` with Adobe's own message. The message is cut to 200 characters, and any secret in it is removed.

### L2.6 "No access" has one message per product

- **Analytics.** The message says that the credential sees no Analytics company. The fix is to add the credential's technical account to an Analytics product profile in the Admin Console.
- **CJA.** The message says that the credential cannot reach Customer Journey Analytics. The fix is to add the Customer Journey Analytics API and the Adobe Experience Platform API to the credential, and to add its technical account to a CJA product profile.

## Level 3: strict lookup

A tool applies these rules in its next breaking release. That is 0.2.0 for aa-health-duckdb and cja-audit-log-monitor, and the next major version for the other tools. Until then, the tool prints a notice when a rule would change the result. The notice codes are in [`codes-v1.json`](codes-v1.json) under `notices`.

### L3.1 Lookup order

A tool looks for the credential in this order and uses the first source that it finds.

1. `--profile <name>` or `--config <path>`. Both given together is an error.
2. The tool's profile variable. This is `AA_PROFILE` for Analytics tools and `CJA_PROFILE` for CJA tools.
3. The environment variables.
4. `.env` in the working folder. A tool reads it as a source of its own. The tool does not search parent folders and does not load the file into the environment.
5. The tool's default config file.

### L3.2 One source wins whole

The four credential fields come from one source. A tool does not mix fields from two sources. A source that has some of the four fields and not all of them is an error that names the missing fields. The rule covers the four credential fields only, so other settings can still come from another source.

### L3.3 No default scopes

A tool has no built-in scopes. A credential without scopes is an error.

## Versions of this standard

The version is in the file names. A change that would make a passing tool fail gets a new version number, and the old files stay.
