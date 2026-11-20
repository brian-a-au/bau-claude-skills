---
name: aa-health-duckdb
description: Run the ahd CLI (PyPI aa-health-duckdb) to check the health of Adobe Analytics report suites, finding anomalies, large drops and spikes, and drops to zero for every custom event, eVar and prop, with runs stored in DuckDB and an offline HTML report. Use for report suite health checks, daily alert emails or Slack posts, re-rendering stored runs, or querying run history with SQL.
---

# aa-health-duckdb

Guide for the [`aa-health-duckdb`](https://github.com/brian-a-au/aa-health-duckdb) CLI. It is an unofficial, open source alternative to Adobe's "Analytics Health Dashboard" Excel workbook. It reads from the Adobe Analytics 2.0 API and never changes anything in Adobe.

## When to use

- Checking whether the custom events, eVars and props of a report suite still collect data as usual.
- Getting yesterday's alerts for one suite or every suite, as text, JSON or CSV.
- Setting up a daily check that emails or posts alerts only when there are any.
- Writing a report again from a stored run, e.g., with another anomaly method, with no calls to Adobe.
- Querying the history of runs with SQL in DuckDB.

For the full option tables, the JSON fields and the DuckDB views, see [reference.md](reference.md). For the Adobe credential, use the `adobe-analytics-api-setup` skill. To document a suite rather than check its health, use the `aa-auto-sdr` skill.

## Install

```bash
uv tool install aa-health-duckdb      # or: pipx install aa-health-duckdb
```

Needs Python 3.12 or newer. The package is `aa-health-duckdb`, but the command is `ahd`. There is no `aa-health-duckdb` command.

## Credentials

`ahd` uses the first of these that it finds:

1. A profile: `--profile NAME` or `AA_PROFILE=NAME`. It reads `~/.aa/orgs/NAME/config.json`, the same file as `aa_auto_sdr`. A profile made with `aa_auto_sdr --profile-add` works in `ahd` with no other setup.
2. All four environment variables: `AHD_ORG_ID`, `AHD_CLIENT_ID`, `AHD_SECRET`, `AHD_SCOPES`.
3. A config file: `--config PATH`, or `./config.json` with the keys `org_id`, `client_id`, `secret`, `scopes`.

If only some `AHD_*` variables are set, each one wins over the same key in the config file. `--config` together with all four variables is an error. When a credential sees more than one login company, `ahd` uses the first one and prints its name when it signs in. Choose another with `--company ID_OR_NAME` on `check`, `suites`, `segments`, `run` or `individual`. `ahd` only reads profiles. Create or test them with `aa_auto_sdr --profile-add` and `aa_auto_sdr --profile-test`. A profile and `--config` cannot be used together.

## A typical session

```bash
ahd check --profile prod                       # does the sign-in work?
ahd suites --profile prod                      # which suites can it see?
ahd check --profile prod --rsid "My Suite"     # full access to this suite, incl. anomaly detection?
ahd run --profile prod --rsid "My Suite"       # fetch 92 days, store a run, write the HTML report
ahd runs --profile prod                        # list stored runs and their numbers
```

- `--rsid` takes a report suite ID (exact case) or a name (any case). On `run`, give it more than once for several suites, or use `--all-suites`. `check` and `segments` take one `--rsid`.
- The report goes to `./reports/` unless you give `--out`. The run prints its path.
- With a profile, the database is `~/.aa/orgs/NAME/ahd.duckdb`. Without one it is `./data/ahd.duckdb`. `--db PATH` overrides both.
- So pass the same `--profile` (or set `AA_PROFILE`) on every command, including `runs`, `render`, `alerts` and `individual`. Without it, those commands look in `./data/ahd.duckdb` and do not find the runs.

## Dimension by metric pairs

The Individual Component Summary shows a dimension by a metric. The default is Page by Occurrences.

```bash
ahd run --rsid "My Suite" --dimension "Internal Search Term" --metric "Cart Additions"
ahd individual --run 3 --dimension evar17 --metric revenue    # add a pair to stored run 3 (5 requests)
```

`--dimension` and `--metric` take a full ID (`variables/evar17`), a short ID (`evar17`) or a name.

## Alerts

`ahd alerts` reads stored runs only. It never calls Adobe. The alerts are for the day before the run date, so after a run today, they are yesterday's alerts.

```bash
ahd alerts --rsid my_suite                           # text, latest finished run of the suite
ahd alerts --all-suites --new-only --format json     # only alerts that started on that day
ahd alerts --run 2 --format csv > alerts.csv
```

- `--rsid` here takes only the exact report suite ID, as `ahd runs` lists it. It does not look up names.
- There is no `--date yesterday`. `--date YYYY-MM-DD` only decides whether a run counts as old.
- Exit codes: `0` printed alerts, `4` no alerts, `1` error, `2` bad option. A daily job can send only when the exit code is 0.
- If today's run failed, `alerts` uses the latest older finished run. It adds a `Warning:` line, and the JSON has `"stale": true`. So exit 0 can mean old alerts, and exit 4 can hide a failed run. Check the exit code of `ahd run` too, or read `stale` from `--format json`.
- When one suite in `--rsid` has no finished run, `alerts` prints the others but exits 1, so an `&&` after it sends nothing.

## Daily job that sends only when there are alerts

```bash
ahd run --profile prod --all-suites
ahd alerts --profile prod --all-suites > alerts.txt && mail -s "Analytics Health alerts" team@example.com < alerts.txt
```

In cron or launchd, use the full path to `ahd` (find it with `which ahd`, often `~/.local/bin/ahd`), because the job's PATH may not include it. `ahd` itself sends no email. The repo has example scripts, `docs/examples/send_alerts.py` for HTML email and `send_slack.py` for Slack, which read `ahd alerts --format json`. `send_alerts.py` also warns about old runs, so prefer it over the plain `mail` line. The repo's `docs/scheduling.md` covers cron, launchd and Windows Task Scheduler. Add `--yes` to `ahd prune` in a scheduled job, because it cannot answer the prompt.

## Anomaly methods

`--anomaly-method` takes `adobe` (default), `weekday-median`, `weekday-iqr` or `weekday-trend`. `--anomaly-sensitivity` takes `low`, `normal` or `high`, and works only with the three local methods. With `adobe`, `low` or `high` is an error. `AHD_ANOMALY_METHOD` and `AHD_ANOMALY_SENSITIVITY` set the defaults for `run`, `individual`, `render` and `alerts`. Set them once in a scheduled job so the report and the alerts flag the same values.

```bash
ahd render --run 3 --anomaly-method weekday-median    # rebuild the report, no calls to Adobe
```

The method is not stored with the run, so you can `render` any stored run with any method.

## When the report has no Adobe anomaly flags

The credential's product profile is missing the Report Suite Tools permission "Anomaly Detection". The run still finishes, but the report has no expected values or Adobe flags, and it says so.

- Fix: in the Adobe Admin Console, add "Anomaly Detection" to the Adobe Analytics product profile that holds the technical account. Then run `ahd check --rsid <suite>` to confirm.
- Workaround with no new run: `ahd render --run N --anomaly-method weekday-median`.

## Common mistakes

- Running `aa-health-duckdb`. The command is `ahd`.
- Leaving out `--profile` on `runs`, `render`, `alerts` or `individual`. They then look in `./data/ahd.duckdb`.
- Passing a suite name to `ahd alerts --rsid`. It takes only the exact ID.
- Writing `--date yesterday`. Dates are `YYYY-MM-DD`, and `alerts` reports the day before the run date on its own.
- Using `--suite`, `--pair` or `report`. The real names are `--rsid`, `--dimension` with `--metric`, and `render`.
- Giving `--config` or `--company` to a command that does not sign in, e.g., `alerts`. That exits 2.

## Exit codes

`0` worked. `1` failed, or a run ended "failed", or an option conflicts with an environment variable, or `--anomaly-sensitivity` is not `normal` with the `adobe` method. `2` bad option on the command line, or `check` found limited access, or `check` or `suites` found no suites. `3` `run` or `individual` finished with some problems ("partial"). `4` `alerts` found no alerts. `130` stopped with Ctrl-C.
