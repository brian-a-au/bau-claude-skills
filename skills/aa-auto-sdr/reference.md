# aa-auto-sdr reference

Full flag matrix for the `aa_auto_sdr` CLI. Verified 2026-09-22. The command is `aa_auto_sdr`; the PyPI package is `aa-auto-sdr`. Read-only, Adobe Analytics 2.0 API only, Python 3.14+.

## Install

```bash
uv tool install aa-auto-sdr
uv tool install "aa-auto-sdr[env,completion,notion]"   # extras
uvx aa-auto-sdr --list-reportsuites                     # run once
pip install aa-auto-sdr
# dev:
git clone https://github.com/brian-a-au/aa_auto_sdr && cd aa_auto_sdr && uv sync --all-extras
```

## Credentials

Precedence: `--profile` > env vars > `.env` (needs the `env` extra) > `config.json`.

```
ORG_ID="YOUR_ORG_ID@AdobeOrg"
CLIENT_ID="YOUR_CLIENT_ID"
SECRET="YOUR_CLIENT_SECRET"
SCOPES="openid,AdobeID,additional_info.projectedProductContext"
```

Recommended extra scopes for broader org access: `read_organizations`, `additional_info.job_function`.

| Flag | Purpose |
|------|---------|
| `--profile-add NAME` | Capture credentials -> `~/.aa/orgs/NAME/config.json` |
| `--profile NAME` | Use a named profile |
| `--profile-list` | List profiles |
| `--profile-show NAME` | Show profile details |
| `--profile-test NAME` | Verify credentials |
| `--profile-import NAME FILE` | Import (with `--profile-overwrite` to replace) |
| `--show-config` | Which credential source resolved |
| `--config-status` / `--validate-config` / `--sample-config` | Diagnostics |

## Generate

```bash
aa_auto_sdr <RSID>                     # Excel default
aa_auto_sdr "Report Suite Name"        # case-insensitive exact match
aa_auto_sdr <RSID> --output-dir /path
aa_auto_sdr <RSID> --metrics-only      # or --dimensions-only
aa_auto_sdr <RSID> --dry-run           # preview paths, no write
aa_auto_sdr <RSID> --open
```

Name matching: `--name-match fuzzy|exact` (default exact). A name matching N suites generates N SDRs.

## Batch and sampling

```bash
aa_auto_sdr RS1 RS2 RS3                 # positional batch
aa_auto_sdr --batch RS1 RS2 --workers 4 --fail-fast
aa_auto_sdr --batch RS1 RS2 RS3 RS4 RS5 --sample 2 --sample-seed 42
aa_auto_sdr --batch prod.us prod.eu dev.us --sample 2 --sample-stratified
```

## Formats

`--format json|csv|html|markdown|excel|all`. Aliases: `reports` (Excel+MD), `data` (CSV+JSON), `ci` (JSON+MD).

```bash
aa_auto_sdr <RSID> --format json --output -  | jq '.report_suite'   # pipe
aa_auto_sdr <RSID> --template ~/aa_en_BRD_SDR_template.xlsx         # Adobe template
aa_auto_sdr <RSID> --format notion            # Notion publish
aa_auto_sdr --notion-create-database          # one-command registry
```

Adobe template download: `https://cdn.experienceleague.adobe.com/assets/Adobe-Enterprise-Docs/analytics-learn.en/main/help/implementation/implementation-basics/assets/aa_en_BRD_SDR_template.xlsx`

## Discovery and inspection

```bash
aa_auto_sdr --list-reportsuites [--format json --output -]
aa_auto_sdr --list-virtual-reportsuites
aa_auto_sdr --list-metrics <RSID>
aa_auto_sdr --list-dimensions <RSID>
aa_auto_sdr --list-segments <RSID>
aa_auto_sdr --list-calculated-metrics <RSID>
aa_auto_sdr --list-classification-datasets <RSID>
aa_auto_sdr --describe-reportsuite <RSID>
aa_auto_sdr --stats <RSID> [RS2 RS3]
aa_auto_sdr --inventory-summary
aa_auto_sdr --interactive
```

List modifiers: `--filter PATTERN`, `--exclude PATTERN`, `--sort name|id`, `--limit N`.

## Snapshots

```bash
aa_auto_sdr <RSID> --snapshot
aa_auto_sdr <RSID> --auto-snapshot [--keep-last 10 | --keep-since 30d]
aa_auto_sdr --list-snapshots [<RSID>] [--format json]
aa_auto_sdr --prune-snapshots <RSID> [--dry-run | --yes]
```

Storage: `~/.aa/orgs/<profile>/snapshots/`.

## Diff

```bash
aa_auto_sdr --diff a.json b.json
aa_auto_sdr --diff <RSID>@latest <RSID>@previous
aa_auto_sdr --diff <RSID>@2026-04-26T17-29-01+00-00 <RSID>@latest
aa_auto_sdr --diff git:HEAD~1:snapshots/x.json git:HEAD:snapshots/x.json
```

Diff formats: `--format console|json|markdown|pr-comment`.
Modifiers: `--side-by-side`, `--summary`, `--ignore-fields description,tags`, `--extended-fields`, `--quiet-diff`, `--diff-labels A=Before B=After`, `--reverse-diff`, `--changes-only`, `--show-only dimensions,metrics`, `--max-issues 50`, `--warn-threshold 10` (exit 3 at threshold).

## Trend and watch

```bash
aa_auto_sdr <RSID> --trending-window 30d
aa_auto_sdr <RSID> --compare-with-prev
aa_auto_sdr rs_prod_us --watch --interval 1h [--agent-mode] [--watch-threshold 5]
aa_auto_sdr rs_prod_us --watch --interval 1h --format notion
aa_auto_sdr rs_prod_us --git-commit [--git-push]
```

## Quality and auditing

```bash
aa_auto_sdr <RSID> --audit-naming
aa_auto_sdr <RSID> --flag-stale
aa_auto_sdr <RSID> --quality-report json
aa_auto_sdr <RSID> --fail-on-quality HIGH
aa_auto_sdr <RSID> --quality-policy ./policy.json
```

## Diagnostics, logging, help

```bash
aa_auto_sdr <RSID> --show-timings
aa_auto_sdr <RSID> --run-summary-json PATH   # or - for stdout
aa_auto_sdr <RSID> --max-retries 6 --retry-base-delay 1.0 --retry-max-delay 30.0
aa_auto_sdr -V | --version
aa_auto_sdr -h | --help
aa_auto_sdr --exit-codes
aa_auto_sdr --explain-exit-code 11
aa_auto_sdr --completion bash|zsh|fish
```

Retry defaults: 3 retries, 0.5s base, 10s cap.

## Exit codes and errors

- `0`: success.
- `3`: `--warn-threshold` CI gate triggered.
- Pipe-path failures emit a machine-readable JSON error envelope on stderr.
- Use `--exit-codes` and `--explain-exit-code <CODE>` for the full reference plus remediation.

## Resources

| Resource | URL |
|----------|-----|
| Repository | https://github.com/brian-a-au/aa_auto_sdr |
| Adobe Analytics 2.0 API | https://developer.adobe.com/analytics-apis/docs/2.0/ |
| Developer Console | https://developer.adobe.com/console/ |
