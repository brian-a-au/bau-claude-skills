---
name: cja-audit-log-monitor
description: Run cja-audit-log-monitor to search, export and watch Adobe Customer Journey Analytics (CJA) audit logs, and to alert on risky activity such as bulk deletes, bulk exports, bulk shares and off-hours bursts, with Slack and webhook delivery. Use for CJA audit log questions (who deleted, exported or shared what), alert rules, scheduled anomaly scans, or audit exports.
---

# cja-audit-log-monitor

Guide for the [`cja-audit-log-monitor`](https://github.com/brian-a-au/cja-audit-log-monitor) terminal app (TUI) and CLI. It reads the Adobe CJA Audit Logs API and never changes anything in Adobe. It is an unofficial community tool.

## When to use

- Finding who created, edited, deleted, shared or exported a CJA component, e.g., a data view.
- Exporting audit logs to JSON, CSV or TSV for a review or a ticket.
- Watching new audit events live, with alert rules.
- Writing or testing alert rules, and sending alerts to Slack or a webhook.
- Scanning for anomalies on a schedule.

For the full flag tables, the anomaly checks and the notification fields, see [reference.md](reference.md). For the Adobe credential, the `adobe-cja-api-setup` skill covers the Developer Console steps. This tool uses the same OAuth Server-to-Server credential as `cja_auto_sdr`, but it reads it from its own places (below).

## Command shape

The command is `cja-audit-log-monitor`. With no arguments it opens the TUI. Every CLI command starts with `cli`:

```bash
cja-audit-log-monitor                          # open the TUI
cja-audit-log-monitor cli <command> [flags]    # run a CLI command
cja-audit-log-monitor -c ./config.yaml cli list   # global flags go BEFORE cli
```

Global flags (`-v`, `-c PATH`, `--version`) go before `cli` or `tui`. `cja-audit-log-monitor cli verify -v` is wrong. Write `cja-audit-log-monitor -v cli verify`.

## Install and credentials

```bash
uv tool install cja-audit-log-monitor     # or: pipx install cja-audit-log-monitor
```

Needs Python 3.11 or newer. Credentials come from, in order: environment variables, a `.env` file in the current folder, then the config file. The names have no prefix:

```bash
ORG_ID=YOUR_ORG_ID@AdobeOrg
CLIENT_ID=your_client_id
SECRET=your_client_secret
SCOPES=openid,AdobeID,read_organizations,additional_info.projectedProductContext
```

Copy `SCOPES` exactly as the Developer Console shows it. The Developer Console project needs both the Customer Journey Analytics API and the Experience Platform API.

```bash
cja-audit-log-monitor cli verify          # logs in, makes one call, prints the log count
cja-audit-log-monitor cli init            # writes the config file (see below)
cja-audit-log-monitor cli config          # shows settings in use and the config path
```

`cli init` writes to the `-c` path, else `CJA_CONFIG_PATH`, else `~/.cja-audit-log-monitor/config.yaml`. If the file exists, it asks before it replaces it. Do not run `init` over an existing config without asking the user. If you write the config by hand, run `chmod 600` on it, or the tool warns on every run.

## Common tasks

```bash
# Who deleted data views or connections in the last 30 days (-s is the date 30 days ago, in UTC)
cja-audit-log-monitor cli search -a DELETE -C DATA_VIEW -C CONNECTION -s 2026-10-20 -F json

# Every use of one action, or one user's activity
cja-audit-log-monitor cli find-action -a EXPORT -d 30
cja-audit-log-monitor cli user -u someone@example.com -d 30 -F json

# History of one component or one Workspace project
cja-audit-log-monitor cli component -i <component_id>
cja-audit-log-monitor cli dashboard -i <project_id>

# Export to a file (format comes from -F or the file suffix)
cja-audit-log-monitor cli export -o audit.csv -d 14 -a EXPORT -a SHARE
cja-audit-log-monitor cli export -F json -o - -s 2026-11-01 -e 2026-11-15 > audit.json

# Summaries
cja-audit-log-monitor cli stats -d 7 -F json
cja-audit-log-monitor cli timeline -d 7 -a DELETE
cja-audit-log-monitor cli report -d 30 -o report.json
```

Facts that agents often get wrong:

- `search` takes dates (`-s`, `-e`), not `--days`. `-s` and `-e` take `YYYY-MM-DD`, `YYYYMMDD` or an ISO date and time, read as UTC. For a relative window, compute the start date, or use `query --last-month`, `user -d N` or `find-action -d N`.
- `search`, `query`, `user`, `component` and `dashboard` return at most 100 entries, and `list` and `find-action` at most 50. Raise `-l` for wider questions, e.g., `-l 5000`. `export` has no limit unless you give `--max-entries`.
- `-a` (action) can be repeated on `search`, `query`, `export`, `timeline` and `tail`. `-C` (component) can be repeated on `list`, `search`, `query`, `export` and `timeline`. Both ignore case. `find-action -a` takes one action, and a second `-a` silently replaces the first. For several actions, use `search -a X -a Y`.
- Action names: `CREATE`, `EDIT`, `DELETE`, `SHARE`, `UNSHARE`, `APPROVE`, `UNAPPROVE`, `EXPORT`, `TRANSFER`, `API_REQUEST`, and more. Component names: `PROJECT`, `FILTER` (segments), `CALCULATED_METRIC`, `DATA_VIEW`, `CONNECTION`, `AUDIENCE`, `FULL_TABLE_EXPORT`, and more. Run `cli actions` and `cli components` for the full lists.
- `export -o` and `report -o` refuse a file that exists unless you add `--force`.
- `report` reads at most 10,000 entries unless you raise `--max-entries`. When it stops early, it warns on stderr and sets `"truncated": true`.
- `-F json` works on most read commands. `export` uses `-F` for `json`, `csv` or `tsv`. `report` always writes JSON. `monitor` and `tail` have no JSON mode.
- Data goes to stdout and messages go to stderr, so `> file` captures only data. The exceptions are `verify`, which prints its failure on stdout, `monitor` and `tail`, which print status lines on stdout, and `anomalies`, which prints "No anomalies found ..." on stdout.

## Alert rules

Rules live under `alert_rules:` in the config file (`~/.cja-audit-log-monitor/config.yaml`, or `-c PATH`, or `CJA_CONFIG_PATH`). A rule fires when `threshold_count` or more matching events happen within `threshold_window_minutes`.

```yaml
alert_rules:
  - name: bulk_delete           # built-in rule, copied so it is kept
    description: Multiple delete operations in short timeframe
    actions: [DELETE]
    threshold_count: 5
    threshold_window_minutes: 60
    per_user: true

  - name: user_bulk_export
    description: More than 3 exports by one user in 30 minutes
    actions: [EXPORT]
    threshold_count: 4          # "more than 3" means 4 or more
    threshold_window_minutes: 30
    per_user: true              # count each account on its own

notifications:
  slack_webhook_url: https://hooks.slack.com/services/XXX/YYY/ZZZ
  notify_on_alerts: true
```

- If the file has any `alert_rules`, they replace the four built-in rules (`bulk_delete`, `bulk_export`, `sensitive_component_delete`, `bulk_share`). They are not merged. Copy the built-in rules you want to keep. `cli init` writes them, commented out. `alert_rules: []` turns off every rule. Only a missing `alert_rules` key gives the built-in rules.
- Use `per_user: true` for volume rules. Without it, events from everyone count together.
- A misspelled key, e.g., `treshold_count`, only gives a warning. The tool drops the key, so `threshold_count` falls back to 1 and the rule fires on every matching event. After every edit, run `cli alerts list` and check the warnings and the Count and Win columns.
- `cli alerts list` shows the loaded rules. `cli alerts test -d 1` runs the rules and the anomaly checks against the last day and sends nothing.
- Rules fire only in `cli monitor`, `cli tail` and the TUI monitor view. A one-off `search` never fires a rule, and `anomalies` does not use rules. So for Slack alerts from rules, keep `cli monitor` running, e.g., in `tmux` or under systemd or launchd.
- Rules do not look back. The first poll of `monitor` or `tail` shows recent events as a baseline, and they do not count toward rules. To check a burst that already happened, run `cli alerts test -d N`.

## Monitoring and anomalies

```bash
cja-audit-log-monitor cli monitor -i 30                  # live, with rules, Ctrl+C to stop
cja-audit-log-monitor cli tail -u someone@example.com    # live, filtered first
cja-audit-log-monitor cli anomalies                      # one scan of the last 24 hours
cja-audit-log-monitor cli anomalies --watch --interval 600 --lookback 24 -F json
```

Anomalies are three fixed checks, separate from rules: `off_hours_activity` (midnight to 5am, judged in UTC in the CLI), `high_activity_user` and `bulk_delete_single_user`. You cannot configure them.

`anomalies` sends to Slack or webhooks only when the config has `notifications:` and `notify_on_anomalies: true`. The default is `false`, so a new setup prints anomalies but sends nothing. `anomalies --watch` keeps running, so run it under a process manager (systemd, launchd) or in `tmux`, not from cron. While it runs, it sends each anomaly to each channel once. A channel that failed gets it again on the next scan, and an anomaly that clears and later comes back is sent again. Each scan prints only the anomalies that are new in that scan, so `count` in the JSON is the new ones. A cron job that runs `anomalies` without `--watch` forgets between runs, so it can send the same anomaly every time.

## Exit codes and errors

`0` worked. `1` failed, which covers config, login, API and file errors and a failed `verify`. `2` bad command line, and nothing is sent to the API.

- `403` from `verify` or any command: add the Experience Platform API to the Developer Console project, and put the service account in a product profile with CJA access in the Admin Console.
- `401`: the secret changed or expired. Retrieve the client secret again.
- `invalid_scope`: `SCOPES` does not match the Developer Console. Copy it again after both APIs are added.
- `Configuration error:` names the bad key and the file. An unknown key is not an error. It only warns, and the tool ignores it (see Alert rules).
