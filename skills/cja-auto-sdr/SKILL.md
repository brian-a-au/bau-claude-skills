---
name: cja-auto-sdr
description: Run the cja_auto_sdr CLI to generate Solution Design Reference docs from Adobe CJA Data Views, diff and snapshot changes, run org-wide governance reports, and publish to Notion. Use for CJA SDR generation, audits, or migration validation.
---

# cja-auto-sdr

Guide for the [`cja_auto_sdr`](https://github.com/brian-a-au/cja_auto_sdr) CLI, which automates Solution Design Reference (SDR) documentation from Adobe Customer Journey Analytics.

## When to use

- Generating SDR docs from CJA Data Views.
- Diffing Data Views or tracking configuration changes over time.
- Running an org-wide governance report across many Data Views.
- Publishing an SDR registry to Notion.
- Setting up CJA audits in CI/CD.

For the Adobe API credentials this tool needs, use the `adobe-api-setup` skill. For a full generate-grade-visualize workflow, use the `sdr-workflow` skill. For the complete flag matrix, see [reference.md](reference.md).

## Install and configure

```bash
uv tool install cja-auto-sdr          # PyPI (recommended)
uvx cja-auto-sdr --list-dataviews     # run once without installing
pip install cja-auto-sdr              # pip alternative
```

Requires Python 3.14+. The CLI command is `cja_auto_sdr` (underscore). For clustering, env, completion, and Notion support: `uv tool install "cja-auto-sdr[full]"`.

Credentials come from environment variables, a `.env` file, or `config.json` (env vars win). Fields: `ORG_ID` (`...@AdobeOrg`), `CLIENT_ID`, `SECRET`, `SCOPES`. The Developer Console project needs both the CJA API and the AEP API. Generate a template with `cja_auto_sdr --sample-config`.

For multiple orgs, use profiles (stored in `~/.cja-auto-sdr/profiles/`):

```bash
cja_auto_sdr --profile-add client-a   # create interactively
cja_auto_sdr --profile client-a --list-dataviews
cja_auto_sdr --profile-test client-a
```

## Verify setup

```bash
cja_auto_sdr --validate-config        # check credentials and connectivity
cja_auto_sdr --list-dataviews         # list accessible Data Views
```

## Generate

```bash
cja_auto_sdr dv_12345                 # single Data View by ID (Excel default)
cja_auto_sdr "Production Analytics"   # by name (exact match)
cja_auto_sdr dv_12345 --open          # open the result
cja_auto_sdr dv_12345 --stats         # quick component count, no full report
cja_auto_sdr dv_1 dv_2 dv_3 --continue-on-error   # batch, keep going on failure
cja_auto_sdr dv_12345 --format all --output-dir ./reports
```

Formats: `excel` (default), `csv`, `json`, `html`, `markdown`, `notion`, `all`. Add inventory sheets with `--include-segments`, `--include-derived`, `--include-calculated`, or `--include-all-inventory`.

## Diff and snapshots

```bash
cja_auto_sdr --diff dv_12345 dv_67890 --changes-only      # compare two Data Views
cja_auto_sdr dv_12345 --snapshot ./baseline.json          # save a snapshot
cja_auto_sdr dv_12345 --diff-snapshot ./baseline.json     # current vs snapshot
cja_auto_sdr --compare-snapshots ./old.json ./new.json    # two files, no API calls
cja_auto_sdr --diff dv_12345 dv_67890 --format markdown   # or json, excel
```

Watch for drift: `cja_auto_sdr --watch dv_12345 --interval 1h --watch-threshold 5`. Commit snapshots to git with `--git-commit` (add `--git-push` to push).

## Org report and Notion

```bash
cja_auto_sdr --org-report --cluster                       # governance across all Data Views
cja_auto_sdr --org-report --fail-on-threshold             # exit 2 if governance violated
cja_auto_sdr dv_12345 --format notion --notion-create-database   # first-time Notion registry
```

## Quality gates for CI

```bash
cja_auto_sdr dv_12345 --fail-on-quality HIGH              # exit 1 if HIGH or worse
cja_auto_sdr --diff dv_prod dv_staging --warn-threshold 10
```

Exit codes: `0` success, `1` error or quality breach, `2` policy threshold exceeded, `3` diff warn threshold exceeded.

## Common troubleshooting

| Symptom | Fix |
|---------|-----|
| `Configuration file not found` | `cja_auto_sdr --sample-config` to generate a template |
| `HTTP 401 Unauthorized` | Confirm the Client Secret is current (see `adobe-api-setup`) |
| `HTTP 403 Forbidden` | Confirm both CJA API and AEP API are in the project |
| `Data view not found` | `--list-dataviews`; names are exact match |
| `No data views found` | Check product-profile permissions in the Admin Console |

Add `--dry-run` to validate without generating output.
