---
name: sdr-workflow
description: Orchestrate the Adobe SDR toolchain end to end - generate an SDR/snapshot (aa_auto_sdr or cja_auto_sdr), grade it (sdr-grader), visualize it (sdr-visualizer), and diff/trend for change tracking. Use for onboarding audits, pre-migration validation, drift monitoring, or PR/CI gating of an Adobe Analytics or CJA implementation.
---

# sdr-workflow

Orchestrate the Adobe Solution Design Reference toolchain: generate, grade, visualize, and track changes across an Adobe Analytics or CJA implementation. This skill chains the tools; each individual skill has the full flag detail.

## When to use

- Auditing a new Adobe Analytics or CJA implementation end to end.
- Validating an implementation before or during a migration.
- Monitoring configuration drift on a schedule.
- Gating pull requests or CI on quality and change thresholds.

## The toolchain

| Tool | Skill | Role |
|------|-------|------|
| `aa_auto_sdr` | `aa-auto-sdr` | Generate + snapshot Adobe Analytics report suites |
| `cja_auto_sdr` | `cja-auto-sdr` | Generate + snapshot CJA Data Views |
| `sdr-grader` | `sdr-grader` (in the sdr-grader repo) | Grade a snapshot against a rubric |
| `sdr-visualizer` | `sdr-visualizer` | Build a browsable HTML catalog |

All four tools install from PyPI (`uv tool install ...`) and use OAuth Server-to-Server credentials. The setup differs by platform: for Adobe Analytics use the `adobe-analytics-api-setup` skill, and for CJA use the `adobe-cja-api-setup` skill. The generators, grader, and visualizer all read the same JSON snapshots.

## Pick the platform

- Adobe Analytics report suites: use `aa_auto_sdr` and target suites by RSID or name.
- Customer Journey Analytics data views: use `cja_auto_sdr` and target Data Views by ID or name.

The examples below show the AA commands; swap in the CJA equivalents (`cja_auto_sdr <dv_ID>`, `--diff-snapshot`, `--include-all-inventory` for the grader) when the platform is CJA.

## Playbook 1: onboarding audit

Generate, grade, and visualize a suite so a new team can see the whole implementation.

```bash
aa_auto_sdr <RSID> --snapshot --format excel        # generate + capture a snapshot
sdr-grader ~/.aa/orgs/<profile>/snapshots/ --output grade.html   # newest snapshot -> grade
sdr-visualizer ~/.aa/orgs/<profile>/snapshots/ --output catalog.html
```

Open `grade.html` for the scorecard and `catalog.html` for the browsable catalog. To read a grade-report JSON in detail, use the canonical `sdr-grader` skill.

## Playbook 2: pre-migration validation

Baseline, make the change, then diff and re-grade to confirm nothing regressed.

```bash
aa_auto_sdr <RSID> --snapshot                       # baseline
# ... perform the migration or config change ...
aa_auto_sdr <RSID> --snapshot                       # new state
aa_auto_sdr --diff <RSID>@previous <RSID>@latest --format markdown --output diff.md
sdr-grader <RSID>@latest --json after.json          # re-grade (or pass the snapshot file)
```

Compare the before and after grades, and review `diff.md` for added, removed, and changed components. For CJA, use `cja_auto_sdr --diff-snapshot ./baseline.json <dv_ID>`.

## Playbook 3: drift monitoring

Watch a suite on an interval and alert when it moves.

```bash
aa_auto_sdr rs_prod_us --watch --interval 1h --auto-snapshot --watch-threshold 5
aa_auto_sdr rs_prod_us --trending-window 30d --format json   # 30-day drift report
sdr-visualizer ~/.aa/orgs/<profile>/snapshots/ --trend --output trend.html
```

Commit each snapshot to git for an audit trail with `--git-commit --git-push`.

## Playbook 4: PR / CI gating

Fail the pipeline on quality regressions or large changes. Wire the exit codes.

```bash
aa_auto_sdr <RSID> --fail-on-quality HIGH           # exit non-zero if HIGH or worse
sdr-grader <RSID> --fail-below B                     # exit non-zero if grade below B
aa_auto_sdr --diff <RSID>@previous <RSID>@latest --warn-threshold 10   # exit 3 at >= 10 changes
```

Exit-code reference for a CI script:

- Generators (`aa_auto_sdr`, `cja_auto_sdr`): `0` success, `1` error or quality breach, `2` policy threshold (CJA org-report), `3` diff warn threshold.
- `sdr-visualizer`: `0` success, `1` runtime error, `3` invalid input.
- `sdr-grader`: non-zero when `--fail-below` is breached.

## Notes

- Keep credentials out of the repo; inject them in CI. See `adobe-analytics-api-setup` (Adobe Analytics) or `adobe-cja-api-setup` (CJA).
- The grader auto-detects platform from the snapshot. For CJA, generate with `--include-all-inventory` so all checks have evidence; AA includes inventory by default.
