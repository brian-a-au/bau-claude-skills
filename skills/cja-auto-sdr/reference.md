# cja-auto-sdr reference

Full flag matrix for the `cja_auto_sdr` CLI. Verified 2026-09-22. The command is `cja_auto_sdr`; the PyPI package is `cja-auto-sdr`.

## Install

```bash
uv tool install cja-auto-sdr          # PyPI
uv tool install "cja-auto-sdr[full]"  # clustering + env + completion + notion
uvx cja-auto-sdr --list-dataviews     # run once
pip install cja-auto-sdr              # pip
# dev:
git clone https://github.com/brian-a-au/cja_auto_sdr.git && cd cja_auto_sdr && uv sync
```

Python 3.14+.

## Credentials

Precedence: environment variables > `.env` (from `.env.example`) > `config.json` (from `config.json.example`).

Fields: `ORG_ID` (`YOUR_ORG_ID@AdobeOrg`), `CLIENT_ID`, `SECRET`, `SCOPES`. Developer Console project must include both CJA API and AEP API. See the `adobe-cja-api-setup` skill.

Profiles stored in `~/.cja-auto-sdr/profiles/`.

| Flag | Purpose |
|------|---------|
| `--profile NAME` | Use a named profile |
| `--profile-add` | Create a profile interactively |
| `--profile-test` | Validate a profile's credentials |
| `--sample-config` | Print a config.json template |
| `--validate-config` | Verify credentials and connectivity |

## Generation and discovery

| Command | Purpose |
|---------|---------|
| `cja_auto_sdr dv_ID` / `"Name"` | Generate SDR for one Data View |
| `cja_auto_sdr --interactive` | Guided selection |
| `cja_auto_sdr --stats dv_ID` | Quick component count |
| `--list-dataviews` | List Data Views |
| `--list-connections` | List data connections |
| `--list-datasets` | Data Views with dataset associations |
| `--list-metrics dv_ID` | Metrics |
| `--list-dimensions dv_ID` | Dimensions |
| `--list-segments dv_ID` | Segments |
| `--list-calculated-metrics dv_ID` | Calculated metrics |
| `--describe-dataview dv_ID` | Detailed inspection |

Discovery modifiers: `--filter PATTERN` (regex), `--sort name|id|type`.

## Output

| Flag | Values / notes |
|------|----------------|
| `--format` | `excel` (default), `csv`, `json`, `html`, `markdown`, `notion`, `all` |
| `--output-dir PATH` | Directory (default: current) |
| `--output PATH` / `-` | File path or stdout |
| `--open` | Open the generated file |

Excel workbook has up to 8 sheets: Metrics, Dimensions, Data Quality Dashboard, Calculated Metrics Inventory, Derived Fields Inventory, Segments Inventory, Summary/Index, Metadata/Changelog.

## Inventory

`--include-segments`, `--include-derived`, `--include-calculated`, `--include-all-inventory`, `--inventory-only`, `--inventory-summary`.

## Component filtering

`--metrics-only`, `--dimensions-only`, `--filter PATTERN`, `--sort name|id|type`.

## Batch and parallel

Positional list or `--batch dv_1 dv_2 dv_3`; `--workers N` (1-256, auto-tuned); `--continue-on-error`.

## Quality and validation

`--skip-validation`; `--fail-on-quality CRITICAL|HIGH|MEDIUM|LOW` (exit 1 if breached); `--quality-report json|excel|markdown`.

## Diff and snapshots

| Command | Purpose |
|---------|---------|
| `--diff dv_1 dv_2` | Compare two Data Views |
| `--snapshot ./baseline.json dv_ID` | Save a snapshot |
| `--diff-snapshot ./baseline.json dv_ID` | Current vs snapshot |
| `--compare-snapshots old.json new.json` | Compare two files |
| `--list-snapshots` | List saved snapshots |
| `--prune-snapshots --keep-last N` | Remove old snapshots |

Diff modifiers: `--auto-snapshot`, `--keep-last N` (default 30), `--auto-prune`, `--changes-only`, `--diff-labels "Before" "After"`, `--metrics-only`, `--dimensions-only`, `--format-pr-comment`, `--warn-threshold N`, `--quiet-diff`.

## Org-wide analysis (CJA-specific)

`--org-report` with `--cluster`, `--org-stats`, `--filter`, `--exclude`, `--limit N`, `--include-names`, `--skip-similarity`, `--core-threshold 0.7`, `--duplicate-threshold 5`, `--fail-on-threshold` (exit 2).

## Notion (CJA-specific)

`--format notion`; `--notion-create-database`; `--notion-prune-orphans [--dry-run]`; `--notion-repair-database [--dry-run]`; `--notion-print-database-schema`. Env: `NOTION_API_KEY`, `NOTION_DATABASE_ID`.

## Git integration

`--git-init --git-dir ./sdr-snapshots`, `--git-commit`, `--git-push`, `--git-message "text"`.

## Watch and trending

`--watch dv_ID --interval 1h|6h|1d`, `--watch-threshold N`.

## Other

`--dry-run`, `--no-color` (or `NO_COLOR`), `FORCE_COLOR`, `--version`, `--help`.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error or quality threshold breach (`--fail-on-quality`) |
| 2 | Policy threshold exceeded (`--fail-on-threshold`) |
| 3 | Diff warn threshold exceeded |

## Environment variables

```bash
export ORG_ID="your_org_id@AdobeOrg"
export CLIENT_ID="your_client_id"
export SECRET="your_client_secret"
export SCOPES="your_scopes"
export NOTION_API_KEY="..."           # for --format notion
export NOTION_DATABASE_ID="..."
```

## Resources

| Resource | URL |
|----------|-----|
| Repository | https://github.com/brian-a-au/cja_auto_sdr |
| CJA API docs | https://developer.adobe.com/cja-apis/docs/ |
| Developer Console | https://developer.adobe.com/console/ |
