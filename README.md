# Claude Code Skills

Personal collection of Claude Code skills for workflow automation and integration.

## Skills

| Skill | Description |
|-------|-------------|
| [adobe-analytics-concepts](skills/adobe-analytics-concepts/SKILL.md) | Conceptual guidance for Adobe Analytics - core concepts (eVars, props, events), tracking design, analysis workflows, and governance |
| [adobe-api-setup](skills/adobe-api-setup/SKILL.md) | Guide for configuring Adobe AEP and CJA API access with OAuth Server-to-Server authentication |
| [cja-sdr-generator](skills/cja-sdr-generator/SKILL.md) | Generate SDR documents from CJA, compare Data Views, and track configuration changes |
| [customer-journey-analytics-concepts](skills/customer-journey-analytics-concepts/SKILL.md) | Conceptual guidance for Adobe CJA - connections, data views, identity, cross-channel journey analysis |

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) must be installed and configured

### Step 1: Create the skills directory (if it doesn't exist)

```bash
mkdir -p ~/.claude/skills
```

### Step 2: Install skills

**Option A: Install a single skill**

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/brian-a-au/bau-claude-skills.git
cd bau-claude-skills

# Copy the desired skill to your Claude skills directory
cp -r skills/adobe-api-setup ~/.claude/skills/
```

**Option B: Install all skills at once**

```bash
# Clone and install all skills
git clone https://github.com/brian-a-au/bau-claude-skills.git
cd bau-claude-skills
cp -r skills/* ~/.claude/skills/
```

### Step 3: Verify installation

Check that your skills are installed correctly:

```bash
ls ~/.claude/skills/
```

You should see the skill folders listed (e.g., `adobe-analytics-concepts`, `adobe-api-setup`, `cja-sdr-generator`, `customer-journey-analytics-concepts`).

### Step 4: Use the skills

Start a new Claude Code session. The skills will be automatically available. You can invoke them by describing the task or by referencing the skill name in your prompt.

### Updating skills

To update to the latest version of the skills:

```bash
cd bau-claude-skills
git pull
cp -r skills/* ~/.claude/skills/
```

## License

MIT
