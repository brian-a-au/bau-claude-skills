# Shared test cases

Each file in [`adobe-credentials-v1/`](adobe-credentials-v1/) holds the cases for one area of the [standard](../adobe-credentials-v1.md). Every tool that looks up a credential runs the cases that apply to it. No case calls Adobe.

## How a tool uses the cases

1. Copy the files into the tool repo with `python3 standards/sync_cases.py <folder in the tool repo>`. The script also writes `SOURCE.json`, which records the commit and a checksum for each file.
2. Write one test module that reads the files and builds each case in a temporary home and working folder. This module is the tool's adapter. It maps the abstract words in a case to the tool, e.g., `profile_variable` is `AA_PROFILE` in an Analytics tool.
3. List every case the tool cannot pass yet in the repo's `known-differences.json`. The adapter expects those cases to fail and every other case to pass. A listed case that starts to pass fails the run, so the list can only get shorter.

A tool skips a case in these situations:

- The case has `products` and the tool's product is not in it.
- The case has `tools` and the tool is not in it.
- The tool has no such command, e.g., a tool with no child process skips `run_child`. The tool lists the rule under `not_applicable` in `known-differences.json`.

## The format of a case

```json
{
  "id": "lookup-005",
  "level": 3,
  "rule": "L3.1",
  "title": "The environment variables beat .env",
  "given": {
    "sources": {
      "environment": {"credential": "A"},
      "dotenv": {"credential": "B"},
      "default_config": {"credential": "B"}
    }
  },
  "expect": {"source": "environment", "credential": "A"}
}
```

- `id` is unique across all files.
- `level` is 1, 2 or 3, and `rule` is a rule in the standard.
- `given.sources` names each source that exists in the case. A source that is not named is absent. The source names are `flag_profile`, `flag_config`, `profile_variable`, `environment`, `dotenv` and `default_config`.
- `credential` is the name of a made-up credential in [`fixtures.json`](adobe-credentials-v1/fixtures.json). `omit` lists fields to leave out. `override` replaces fields. `extra_keys` adds keys.
- `given.command` is `config_check`, `live_test` or `run_child`. A case with no command tests the lookup alone.
- `expect` holds the result. `source` is the source that must win. `error`, `notice` and `warning` are codes from [`codes-v1.json`](../codes-v1.json).

## Same credential as before

Each tool also runs its lookup cases against its previous release. The test fails when the winning source differs in a case that the changelog does not name. This check belongs to each tool repo, because it needs the previous release installed.
