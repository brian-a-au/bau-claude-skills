# aa-health-duckdb reference

Option tables for the `ahd` CLI. Verified 2026-11-19 against version 0.1.18. The command is `ahd`. The PyPI package is `aa-health-duckdb`. It is read-only against Adobe Analytics and needs Python 3.12 or newer. The full docs are in the repo's [`docs/`](https://github.com/brian-a-au/aa-health-duckdb/tree/main/docs) folder.

## Shared options

| Option | Purpose |
|---|---|
| `--profile NAME` | On every command. Use `~/.aa/orgs/NAME/config.json` and `~/.aa/orgs/NAME/ahd.duckdb`. It can go before or after the command. `AA_PROFILE` sets it too. |
| `--config PATH` | Use this credential file instead of `./config.json`. Not with a profile. Only on `check`, `suites`, `segments`, `run` and `individual`. |
| `--company ID_OR_NAME` | Choose the login company when the credential sees more than one. Only on `check`, `suites`, `segments`, `run` and `individual`. |
| `--db PATH` | Use this database file. On every command except `check`, `suites` and `segments`. |
| `--verbose` | Debug detail to stderr. Put it before the command, e.g., `ahd --verbose run ...`. |

The commands that sign in are `check`, `suites`, `segments`, `run` and `individual`. The commands `runs`, `render`, `alerts`, `export`, `prune` and `import` never call Adobe.

## Commands

| Command | What it does |
|---|---|
| `ahd check [--rsid S]` | Tests the sign-in. With `--rsid`, also counts components and tests anomaly detection, and names any missing permission. |
| `ahd suites` | Lists report suites the credential can see. |
| `ahd segments --rsid S` | Lists segments usable with that suite. |
| `ahd run` | Fetches 92 days, stores a run, writes the HTML report. |
| `ahd individual --run N --dimension D --metric M` | Adds a pair to a stored run and writes the report again. |
| `ahd render --run N` | Writes the report of a stored run again, with no calls to Adobe. |
| `ahd alerts` | Prints alerts of stored runs as text, JSON or CSV. |
| `ahd runs` | Lists stored runs, newest number first. |
| `ahd prune --run N` / `--before DATE` | Deletes stored runs. Asks first unless `--yes`. Keeps "running" runs unless `--force`. |
| `ahd export --out DIR` | Writes every stored run as Parquet files and a `manifest.json`. |
| `ahd import SOURCE` | Copies runs from another database or an export folder. |

## `run` options

| Option | Default | Purpose |
|---|---|---|
| `--rsid` | | Suite by ID or name. Repeat for several. Needs this or `--all-suites`. |
| `--all-suites` | | Every suite the credential sees. |
| `--segment` | none | Filter every request by a segment, by ID or name. |
| `--dimension`, `--metric` | Page by Occurrences | The first Individual Component Summary pair. |
| `--date YYYY-MM-DD` | today in the suite's time zone | Treat this date as today. Cannot be in the future. |
| `--change-alert` | 30 | Large drop slider start, 10 to 100 in steps of 5. |
| `--spike-alert` | 50 | Large spike slider start, 10 to 200 in steps of 10. |
| `--anomaly-method` | `adobe` | `adobe`, `weekday-median`, `weekday-iqr`, `weekday-trend`. |
| `--anomaly-sensitivity` | `normal` | `low`, `normal`, `high`. Local methods only. |
| `--out` | `./reports/` | Folder for the HTML report. |
| `--batch-size` | 20 | Columns per trend request, 1 to 100. |
| `--workers` | 8 | Requests at the same time, 1 to 16. |

With several suites, a failed suite does not stop the others. The exit code is that of the worst suite. Adobe allows 12 requests in any 6 seconds per user. Two `ahd` commands at the same time with one credential can go over that limit.

## `alerts` options

| Option | Purpose |
|---|---|
| `--run N` | Alerts of one stored run. |
| `--rsid ID` | Latest finished run of the suite. Exact ID only, no names. Repeat for several. |
| `--all-suites` | Latest finished run of every suite in the database. |
| `--segment ID` | With `--rsid` or `--all-suites`, use runs with this segment. |
| `--format text\|json\|csv` | Default `text`. |
| `--new-only` | Only alerts that started on the day. Exit 4 when none are new. |
| `--every-alert` | In text, list every alert of a suite-wide event, not only the first 5. |
| `--change-alert`, `--spike-alert` | A percent above 0, at most 100 for drops and 200 for spikes. Decimals work, e.g., `27.5`. |
| `--anomaly-method`, `--anomaly-sensitivity` | As in `run`. |
| `--date YYYY-MM-DD` | Only decides whether a run counts as old. |

JSON shape: `{"format_version": 1, "runs": [...]}`. Each run has `run_id`, `rsid`, `rsid_name`, `segment_id`, `status`, `day`, `method`, `method_name`, `sensitivity`, `threshold`, `spike_threshold`, `current_day`, `stale`, `failed_after`, `warning`, `events` and `alerts`. `threshold` and `spike_threshold` are shares, e.g., `0.3` is 30 percent. Each alert has `alert` (`unusual`, `large drop`, `large spike`, `dropped to zero`), `anomaly`, `component_id`, `name`, `group`, `metric_type`, `value`, `usual`, `expected`, `pct_vs_usual`, `since`, `days`, `at_least`, `is_new` and `event`. `pct_vs_usual` is also a share. Ignore fields you do not know, because later versions add fields.

A suite-wide event is 10 or more alerts of one kind that cover at least half of the components that collected data, e.g., when the whole suite stopped collecting.

## DuckDB

| You ran `ahd` with | The file is |
|---|---|
| no profile | `./data/ahd.duckdb` |
| `--profile prod` | `~/.aa/orgs/prod/ahd.duckdb` |
| `--db PATH` | that file |

Open it with `duckdb -readonly <file>`. The `duckdb` CLI (2.0 or newer) is a separate install, e.g., `brew install duckdb`. The `latest_runs` view has the columns of `runs`, e.g., `run_id`, `rsid`, `rsid_name`, `segment_id`, `today` and `status`. While `ahd run`, `ahd individual`, `ahd prune` or `ahd import` writes to the file, nothing else can open it. An open `duckdb` session blocks those four commands.

Tables: `runs`, `components`, `daily_values`, `pairs`, `top_items`, `breakdowns`, `breakdown_totals`, `issues`. Views: `latest_runs` (latest finished run per suite and segment) and `component_days`. Table macros: `alerts(run, ...)`, `suite_events(run, ...)` and `anomaly_days(run, ...)`.

```sql
FROM latest_runs SELECT run_id, rsid_name, today, status;
FROM alerts((SELECT max(run_id) FROM latest_runs WHERE rsid = 'my_suite' AND segment_id IS NULL));
```

The repo's `docs/duckdb.md` has recipes for alert emails, owner routing and digests across organizations.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `check` signs in but sees no suites | The technical account is not in an Adobe Analytics product profile. Add it in the Admin Console. |
| No custom data in the report | The product profile hides the custom components. Add the suite's metrics and dimensions to it. |
| No Adobe anomaly flags or expected values | The product profile lacks Report Suite Tools "Anomaly Detection". Add it, or use a local `--anomaly-method`. |
| Warning about 20 percent fewer components than last time | Data did not stop. The run cannot see some components. Usually the product profile changed, or the run used a different credential. |
| "is in use by another program" | A `duckdb` session or another `ahd` command has the file open. Close it. |
| A run stays "running" | The process stopped without Ctrl-C, e.g., the window closed. Make a new run. `ahd prune --run N --force` deletes the old one. |
| Sign-in messages, e.g., "the scopes are wrong" | Each message names the cause and the fix. Copy the value again from the Developer Console. |
