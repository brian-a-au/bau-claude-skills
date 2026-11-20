# cja-audit-log-monitor reference

Flag tables for the `cja-audit-log-monitor` CLI. Verified 2026-11-19 against version 0.1.1. The command and the PyPI package are both `cja-audit-log-monitor`. It is read-only against the CJA Audit Logs API and needs Python 3.11 or newer. The full docs are in the repo's [`docs/`](https://github.com/brian-a-au/cja-audit-log-monitor/tree/main/docs) folder.

## Global options (before `cli` or `tui`)

| Option | Purpose |
|---|---|
| `-v`, `--verbose` | Debug logging to stderr. CLI only. Never logs the secret. |
| `-c`, `--config PATH` | Config file other than `~/.cja-audit-log-monitor/config.yaml`. `CJA_CONFIG_PATH` sets it too. |
| `--version` | Print the version. |

## Query commands

| Command | Key flags | Notes |
|---|---|---|
| `list` | `-l` (50), `-C` repeatable, `-D` details, `-F` | Newest entries. |
| `search` | `-u`, `-a` repeatable, `-s`, `-e`, `-C` repeatable, `--component-id`, `--desc`, `-l` (100), `-D`, `-F` | The API filters. Dates only, no `--days`. |
| `query` | one of `--today`, `--yesterday`, `--last-week`, `--last-month`, plus `-u`, `-a`, `-C`, `-l`, `-F`, `-q` | No preset means the last 7 days. |
| `user` | `-u` required, `-d`, `-l`, `-F` | One user's events. |
| `component` | `-i` required, `-t` type, `-l`, `-F` | One component's events. |
| `dashboard` | `-i` required, `-l`, `-F` | One Workspace project's events. |
| `find-action` | `-a` required, `-d`, `-l` (50), `-F` | Every use of one action. |
| `top-users` | `-d`, `-n` (10), `-F` | Most active users. |
| `show ENTRY_ID` | `--max-entries` (10000) | Every field of one entry. |

`-d` defaults to `default_days` in the config file, which is 7. `-u` takes a user id or an email address. `-i` is an id on `component` and `dashboard`, but the interval on `monitor` and `tail`.

## Analysis commands

| Command | Key flags | Notes |
|---|---|---|
| `stats` | `-d`, `-n`, `-F` | Summary statistics. |
| `timeline` | `-d`, `-a`, `-C`, `-u`, `-F` | Activity by day and by UTC hour. |
| `report` | `-d`, `-o`, `--pretty`/`--compact`, `--max-entries`, `--force` | Always JSON. stdout without `-o`. |

## Export

`cli export -o PATH` with `-F json|csv|tsv` (or the file suffix), `-s`, `-e`, `-d`, `-a`, `-C`, `--max-entries`, `--pretty`/`--compact`, `--force`.

- `-o -` writes to stdout.
- An existing file is refused unless `--force`. The file appears only when the export is complete, with mode 0600.
- When nothing matches, it still writes the file, so a scheduled export never leaves an old file.
- CSV and TSV columns: `id`, `timestamp`, `user_id`, `user_email`, `user_name`, `action`, `component_type`, `component_id`, `component_name`, `description`, `org_id`, `ip_address`, `changes`.
- Cells that start with `=`, `+`, `-` or `@` get a `'` in front, so a spreadsheet does not run them.

## Monitoring

| Command | Key flags | Notes |
|---|---|---|
| `monitor` | `-i` (config `monitor_interval`, 60, min 5), `--duration`, `--alerts`/`--no-alerts` | Prints new events and fires rules. Ctrl+C exits 0. |
| `tail` | `-i` (5), `-u`, `--component-id`, `-a`, `--alerts`/`--no-alerts` | Filters before rules. |
| `anomalies` | `--watch`, `--interval` (300, 5 to 86400), `--lookback` hours (24), `-F` | One scan, or a loop with `--watch`. |

Each poll reads from 5 minutes before the last good poll, so an event the API indexes more than 5 minutes late is missed. A 400, 401, 403 or 404 stops `monitor`, `tail` and `anomalies --watch` with exit 1. Other errors are tried again at the next interval.

`anomalies --watch -F json` prints one line per scan: `{"anomalies": [...], "count": N}`.

## Alert rules

| Field | Default | Purpose |
|---|---|---|
| `name` | required | Unique name. |
| `description` | none | Shown at the start of the alert message. |
| `enabled` | `true` | |
| `actions` | all | Action types. An empty list is an error. |
| `components` | all | Component types. An empty list is an error. |
| `threshold_count` | 1 | Events needed to fire. |
| `threshold_window_minutes` | 60 | 1 to 525,600. Measured by event time. |
| `users` | all | User ids, emails or display names. Case does not matter. |
| `per_user` | `false` | Count each account on its own. |

Built-in rules, used only when the config has no `alert_rules` key:

| Rule | Watches | Fires at | Per user |
|---|---|---|---|
| `bulk_delete` | `DELETE` | 5 in 60 minutes | yes |
| `bulk_export` | `EXPORT` | 3 in 30 minutes | yes |
| `sensitive_component_delete` | `DELETE` of a data view, connection, filter or calculated metric | 1 in 1 minute | no |
| `bulk_share` | `SHARE` | 10 in 60 minutes | yes |

After a rule fires, its count starts again from zero.

## Anomaly checks

| Check | Fires when |
|---|---|
| `off_hours_activity` | An hour from 00:00 to 04:59 has 5 or more actions and more than twice the hourly average. UTC in the CLI, local time in the TUI. |
| `high_activity_user` | One user has 20 or more actions and more than three times the average of the other users. Needs two or more users. |
| `bulk_delete_single_user` | One user has 11 or more deletes. |

## Notifications

```yaml
notifications:
  slack_webhook_url: https://hooks.slack.com/services/XXX/YYY/ZZZ
  notify_on_alerts: true       # default true
  notify_on_anomalies: true    # default false
  webhooks:
    - url: https://example.com/webhook
      method: POST
      headers:
        Authorization: Bearer your-token
      timeout: 30
      include_entry_details: true
```

- Rule alerts are sent by `monitor`, `tail` and the TUI monitor view.
- Anomalies are sent only by `cli anomalies`, and only with `notify_on_anomalies: true`. The TUI never sends anomalies.
- While `anomalies` runs, it sends each anomaly to each channel once. It forgets this when it exits, so a cron job that runs `anomalies` once per schedule can send the same anomaly again on each run.
- `alerts test` never sends.

## Config settings

| Key | Default | Range |
|---|---|---|
| `default_days` | 7 | 1 to 3,650 |
| `monitor_interval` | 60 | 5 to 86,400 |
| `default_page_size` | 100 | TUI only |
| `api_base_url` | `https://cja.adobe.io` | https only |
| `ims_base_url` | `https://ims-na1.adobelogin.com` | https only |

Priority: environment variables, then `.env` in the current folder, then the config file, then the default.

## TUI keys

`d` dashboard, `l` log browser, `m` monitor, `s` statistics, `a` alerts, `c` config, `/` search, `e` export, `r` refresh, `?` help, `q` quit. Rule toggles in the alerts view last until you quit.
