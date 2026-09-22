---
name: sdr-visualizer
description: Run sdr-visualizer to turn Adobe Analytics/CJA SDR snapshots into a self-contained, browsable HTML catalog with search, a reference graph, segment and calculated-metric anatomy, and Changes/Trend views. Also maps AEP dataset-to-CJA lineage as a shareable HTML diagram (cja-lineage). Use to visualize an SDR snapshot, a live report suite or data view, or dataset lineage.
---

# sdr-visualizer

Guide for the [`sdr-visualizer`](https://github.com/brian-a-au/sdr-visualizer) CLI, which turns Adobe Analytics and CJA SDR snapshots into a single offline HTML catalog.

## When to use

- Turning an SDR snapshot into a browsable, searchable catalog.
- Visualizing a live report suite (AA) or data view (CJA).
- Adding a Changes view between two snapshots, or a Trend view across a snapshot directory.
- Mapping AEP dataset lineage into CJA with the `cja-lineage` companion command.

It consumes the same JSON snapshots that `aa_auto_sdr` and `cja_auto_sdr` produce. See the `aa-auto-sdr` and `cja-auto-sdr` skills for generating those, and `sdr-workflow` for the end-to-end flow.

## Install

```bash
uv tool install sdr-visualizer
pip install sdr-visualizer
```

Optional workspace-usage evidence: `uv tool install "sdr-visualizer[workspace-cja]"` or `[workspace-aa]`.

## Basic usage

```bash
sdr-visualizer snapshot.json          # a saved snapshot file
sdr-visualizer path/to/snapshots/     # a directory (uses the most recent)
some-command | sdr-visualizer -       # stdin
```

## Live modes

```bash
sdr-visualizer --rsid prod_us         # live AA mode via aa_auto_sdr
sdr-visualizer --dataview dv_prod     # live CJA mode via cja_auto_sdr
```

`sdr-visualizer` stores no credentials of its own. Live modes rely on the upstream generator's credentials (see `adobe-api-setup`).

## Changes and Trend views

```bash
sdr-visualizer snapshot.json --compare-to previous.json   # adds a Changes view
sdr-visualizer path/to/snapshots/ --trend                 # adds a Trend view
sdr-visualizer a.json --compare-to b.json --allow-instance-mismatch
```

## Common flags

| Flag | Purpose |
|------|---------|
| `--output PATH` | HTML output location |
| `--json PATH` | Also emit the embedded JSON as a sidecar |
| `--title TEXT` | Override the document title |
| `--color-pack default\|ADBE\|OMTR\|BLUE` | Presentation palette |
| `--exclude-orphans` | Keep only referenced components |
| `--max-graph-nodes N` | Override the 1,000-node render threshold |
| `--platform cja\|aa` | Override platform auto-detection |
| `--at TIMESTAMP` | Pick the snapshot closest to a timestamp |
| `--quiet` | Suppress informational output |
| `--version` | Print version |

## cja-lineage companion

Visualizes AEP dataset connections into CJA:

```bash
cja_auto_sdr --list-datasets --format json --output - > discovery.json
cja-lineage --saved discovery.json --output lineage.html
```

## Output and exit codes

Produces a single self-contained offline HTML file, default `./visualize-{instance_id}-{timestamp}.html`. The catalog has a searchable table, a force-directed reference graph, segment anatomy diagrams, calculated-metric formula trees, and optional Changes and Trend views. Add a JSON sidecar with `--json`.

Exit codes: `0` success, `1` runtime error (for example an output write failure), `3` invalid input (generator failure, timeout, or ambiguous platform; set `--platform` to resolve).
