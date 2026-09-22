#!/usr/bin/env python3
"""Validate the skills in this repo and the plugin manifests.

Runs with the standard library only, so it works anywhere Python 3 is present.
It checks each skills/<name>/SKILL.md and the .claude-plugin manifests, then
exits non-zero if anything is wrong. Run it locally or in CI.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
PLUGIN_DIR = ROOT / ".claude-plugin"

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def frontmatter(text: str) -> str | None:
    """Return the YAML frontmatter block, or None if it is missing."""
    if not text.startswith("---\n"):
        return None
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return None
    return parts[1]


def field(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else None


def check_skill(skill_dir: Path) -> None:
    name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        err(f"{name}: missing SKILL.md")
        return

    text = skill_file.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if fm is None:
        err(f"{name}: SKILL.md has no YAML frontmatter")
        return

    fm_name = field(fm, "name")
    if fm_name is None:
        err(f"{name}: frontmatter is missing 'name'")
    elif fm_name != name:
        err(f"{name}: frontmatter name '{fm_name}' does not match folder '{name}'")

    desc = field(fm, "description")
    if desc is None:
        err(f"{name}: frontmatter is missing 'description'")
    else:
        if len(desc) < 10:
            err(f"{name}: description is too short ({len(desc)} chars)")
        if len(desc) > 500:
            err(f"{name}: description is too long ({len(desc)} chars)")

    # Relative markdown links (e.g. reference.md) must resolve inside the folder.
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        rel = target.split("#", 1)[0]
        if not rel:
            continue
        if not (skill_dir / rel).exists():
            err(f"{name}: broken link to '{target}'")


def check_json(path: Path) -> dict | None:
    if not path.is_file():
        err(f"{path.relative_to(ROOT)}: missing")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        err(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
        return None


def check_plugin() -> None:
    plugin = check_json(PLUGIN_DIR / "plugin.json")
    if plugin is not None:
        if not plugin.get("name"):
            err("plugin.json: missing 'name'")
        if not plugin.get("version"):
            err("plugin.json: missing 'version'")

    market = check_json(PLUGIN_DIR / "marketplace.json")
    if market is not None:
        if not market.get("name"):
            err("marketplace.json: missing 'name'")
        plugins = market.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            err("marketplace.json: 'plugins' must be a non-empty list")
        else:
            for i, entry in enumerate(plugins):
                if not entry.get("name"):
                    err(f"marketplace.json: plugins[{i}] missing 'name'")
                if not entry.get("source"):
                    err(f"marketplace.json: plugins[{i}] missing 'source'")


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print("No skills/ directory found", file=sys.stderr)
        return 1

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    for skill_dir in skill_dirs:
        check_skill(skill_dir)
    check_plugin()

    if errors:
        print(f"FAIL: {len(errors)} problem(s) found\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK: {len(skill_dirs)} skills and plugin manifests valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
