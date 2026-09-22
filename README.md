# Claude Code Skills

A collection of Claude Code skills for Adobe Analytics and Customer Journey Analytics. Use them to understand the core concepts, set up API access, and run the Solution Design Reference tools for generating, grading, visualizing, and tracking your implementation.

## Skills

### Concepts

| Skill | What it does |
|-------|--------------|
| [adobe-analytics-concepts](skills/adobe-analytics-concepts/SKILL.md) | Explains Adobe Analytics concepts such as eVars, props, events, scopes, attribution, tracking design, and governance. It does not connect to live data. |
| [customer-journey-analytics-concepts](skills/customer-journey-analytics-concepts/SKILL.md) | Explains CJA concepts such as connections, data views, datasets, identity and stitching, and cross channel analysis. It does not connect to live data. |

### Setup

| Skill | What it does |
|-------|--------------|
| [adobe-analytics-api-setup](skills/adobe-analytics-api-setup/SKILL.md) | Sets up Adobe Analytics API 2.0 access with OAuth Server to Server auth, for `aa_auto_sdr`. Use it to configure credentials or to fix 401 and 403 errors. |
| [adobe-cja-api-setup](skills/adobe-cja-api-setup/SKILL.md) | Sets up Adobe CJA and AEP API access with OAuth Server to Server auth, for `cja_auto_sdr`. Use it to configure credentials or to fix 401 and 403 errors. |

### SDR tooling

| Skill | What it does |
|-------|--------------|
| [aa-auto-sdr](skills/aa-auto-sdr/SKILL.md) | Runs the `aa_auto_sdr` CLI to generate Solution Design Reference docs from Adobe Analytics report suites, with batch runs, snapshots, diffs, and quality gates. |
| [cja-auto-sdr](skills/cja-auto-sdr/SKILL.md) | Runs the `cja_auto_sdr` CLI to generate SDR docs from CJA Data Views, diff and snapshot changes, run org wide reports, and publish to Notion. |
| [sdr-visualizer](skills/sdr-visualizer/SKILL.md) | Runs `sdr-visualizer` to turn SDR snapshots into a browsable HTML catalog with search, a reference graph, and Changes and Trend views. |
| [sdr-grader](https://github.com/brian-a-au/sdr-grader/tree/main/skills/sdr-grader) | Reads and explains an `sdr-grader` grade report. This skill lives in the [sdr-grader repo](https://github.com/brian-a-au/sdr-grader), so install it from there. |

### Workflow

| Skill | What it does |
|-------|--------------|
| [sdr-workflow](skills/sdr-workflow/SKILL.md) | Ties the SDR tools together. It walks you through generating, grading, visualizing, and diffing an implementation for audits, migrations, drift monitoring, and CI gating. |

## The SDR ecosystem

These skills wrap a set of command line tools. Each tool installs from PyPI with `uv tool install`.

| Tool | Repository | Role |
|------|------------|------|
| aa_auto_sdr | https://github.com/brian-a-au/aa_auto_sdr | Generate SDR docs and snapshots from Adobe Analytics |
| cja_auto_sdr | https://github.com/brian-a-au/cja_auto_sdr | Generate SDR docs and snapshots from CJA |
| sdr-grader | https://github.com/brian-a-au/sdr-grader | Grade a snapshot against a rubric and produce a scorecard |
| sdr-visualizer | https://github.com/brian-a-au/sdr-visualizer | Build a browsable HTML catalog from a snapshot |

The `sdr-grader` skill listed above lives in its own repository, so install it from there. The `sdr-workflow` skill in this collection covers how to run the grader as part of the full workflow.

## Installation

You need [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured.

### Step 1: Create the skills directory

```bash
mkdir -p ~/.claude/skills
```

### Step 2: Install the skills

Clone this repository and copy the skills you want.

```bash
git clone https://github.com/brian-a-au/bau-claude-skills.git
cd bau-claude-skills
```

Install one skill:

```bash
cp -r skills/adobe-analytics-api-setup ~/.claude/skills/
```

Install all of them:

```bash
cp -r skills/* ~/.claude/skills/
```

If you installed an earlier version, remove the folders that were renamed. `cja-sdr-generator` is now `cja-auto-sdr`, and `adobe-api-setup` was split into `adobe-analytics-api-setup` and `adobe-cja-api-setup`.

```bash
rm -rf ~/.claude/skills/cja-sdr-generator ~/.claude/skills/adobe-api-setup
```

### Step 3: Check the install

```bash
ls ~/.claude/skills/
```

You should see the skill folders you copied.

### Step 4: Use the skills

Start a new Claude Code session. The skills load on their own. You can trigger one by describing the task or by naming the skill in your prompt.

## Updating

```bash
cd bau-claude-skills
git pull
cp -r skills/* ~/.claude/skills/
```

## License

MIT
