---
name: aa-auto-sdr
description: Run the aa_auto_sdr CLI to generate Solution Design Reference docs from Adobe Analytics report suites (Excel/CSV/JSON/HTML/Markdown), batch and sample across suites, snapshot and diff for change tracking, template-fill the Adobe BRD/SDR template, and gate on quality. Use for Adobe Analytics SDR generation, audits, or CI checks.
---

# aa-auto-sdr

Guide for the [`aa_auto_sdr`](https://github.com/brian-a-au/aa_auto_sdr) CLI, which automates Solution Design Reference (SDR) documentation from Adobe Analytics report suites using the Analytics 2.0 API. It is read-only against Adobe Analytics.

## When to use

- Generating SDR docs from Adobe Analytics report suites.
- Documenting many suites in one batch, or sampling a subset.
- Snapshotting and diffing report suites to track configuration changes.
- Filling the official Adobe BRD/SDR Excel template.
- Gating a pipeline on naming or quality rules.

For the Adobe API credentials this tool needs, use the `adobe-api-setup` skill. To turn a snapshot into a browsable catalog, use the `sdr-visualizer` skill. To grade an implementation, use the `sdr-grader` tool and its skill. For a full generate-grade-visualize workflow, use `sdr-workflow`. For the complete flag matrix, see [reference.md](reference.md).

## Install and configure

```bash
uv tool install aa-auto-sdr           # PyPI (recommended)
uvx aa-auto-sdr --list-reportsuites   # run once without installing
pip install aa-auto-sdr              # pip alternative
```

Requires Python 3.14+. The CLI command is `aa_auto_sdr` (underscore). For env-file, completion, and Notion support: `uv tool install "aa-auto-sdr[env,completion,notion]"`.

Credentials resolve in this order: `--profile` > environment variables > `.env` > `config.json`. Fields: `ORG_ID` (`...@AdobeOrg`), `CLIENT_ID`, `SECRET`, `SCOPES` (for example `openid,AdobeID,additional_info.projectedProductContext`).

For multiple orgs, use profiles (stored in `~/.aa/orgs/<name>/config.json`):

```bash
aa_auto_sdr --profile-add prod        # capture credentials interactively
aa_auto_sdr <RSID> --profile prod
aa_auto_sdr --profile-test prod
```

## Verify setup

```bash
aa_auto_sdr --show-config             # which credential source resolved
aa_auto_sdr --list-reportsuites       # list accessible report suites
```

## Generate

```bash
aa_auto_sdr <RSID>                    # single suite (Excel default)
aa_auto_sdr "Report Suite Name"       # by name (case-insensitive exact match)
aa_auto_sdr <RSID> --open             # open the result
aa_auto_sdr RS1 RS2 RS3               # batch (auto-detected)
aa_auto_sdr --batch RS1 RS2 --workers 4 --fail-fast
aa_auto_sdr --batch RS1 RS2 RS3 RS4 RS5 --sample 2 --sample-seed 42   # reproducible sample
```

Formats: `--format json|csv|html|markdown|excel|all`. Aliases: `reports` (Excel+Markdown), `data` (CSV+JSON), `ci` (JSON+Markdown). Fill the Adobe template with `--template ~/aa_en_BRD_SDR_template.xlsx`.

## Snapshots, diff, and trend

```bash
aa_auto_sdr <RSID> --snapshot                         # capture alongside generation
aa_auto_sdr <RSID> --auto-snapshot --keep-last 10     # snapshot every run, keep 10
aa_auto_sdr --list-snapshots <RSID>
aa_auto_sdr --diff <RSID>@latest <RSID>@previous      # compare two snapshots
aa_auto_sdr --diff a.json b.json --format pr-comment  # GitHub-friendly diff
aa_auto_sdr <RSID> --trending-window 30d              # 30-day drift
```

Snapshots live in `~/.aa/orgs/<profile>/snapshots/`. Diff tokens include `<RSID>@latest`, `<RSID>@previous`, a timestamp, or `git:REF:path`.

## Watch mode

```bash
aa_auto_sdr rs_prod_us --watch --interval 1h --watch-threshold 5
aa_auto_sdr rs_prod_us --watch --interval 1h --agent-mode   # NDJSON output
aa_auto_sdr rs_prod_us --watch --interval 1h --git-commit --git-push
```

## Quality gates for CI

```bash
aa_auto_sdr <RSID> --audit-naming --quality-report json
aa_auto_sdr <RSID> --flag-stale
aa_auto_sdr <RSID> --fail-on-quality HIGH             # exit non-zero if HIGH or worse
aa_auto_sdr --diff a.json b.json --warn-threshold 10  # exit 3 if >= 10 changes
```

## Common troubleshooting

```bash
aa_auto_sdr --validate-config         # validate credentials
aa_auto_sdr --exit-codes              # list every exit code
aa_auto_sdr --explain-exit-code 11    # explain a code plus remediation
```

Exit `0` is success; exit `3` is the `--warn-threshold` gate. Pipe-path failures print a machine-readable JSON error envelope on stderr. For auth errors (`401`/`403`), see the `adobe-api-setup` skill.
