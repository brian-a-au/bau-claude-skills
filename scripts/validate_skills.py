#!/usr/bin/env python3
"""Validate the skills in this repo, the plugin manifests and the standards.

Runs with the standard library only, so it works anywhere Python 3 is present.
It checks each skills/<name>/SKILL.md, the .claude-plugin manifests and the
files under standards/, then exits non-zero if anything is wrong. Run it locally
or in CI.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
PLUGIN_DIR = ROOT / ".claude-plugin"
STANDARDS_DIR = ROOT / "standards"

SPEC = "adobe-credentials/v1"
CASE_SOURCES = {
    "flag_profile",
    "flag_config",
    "profile_variable",
    "profile_variable_target",
    "environment",
    "environment_plain",
    "dotenv",
    "default_config",
}
CASE_COMMANDS = {"config_check", "live_test", "run_child"}
CREDENTIAL_FIELDS = {"org_id", "client_id", "secret", "scopes"}

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


def check_links(path: Path) -> None:
    """Relative markdown links in a standards file must resolve."""
    text = path.read_text(encoding="utf-8")
    rel_path = path.relative_to(ROOT)
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        rel = target.split("#", 1)[0]
        if rel and not (path.parent / rel).exists():
            err(f"{rel_path}: broken link to '{target}'")


def check_case(where: str, case: dict, rules: set[str], creds: dict, codes: dict, seen: set[str]) -> None:
    case_id = case.get("id")
    if not isinstance(case_id, str) or not case_id:
        err(f"{where}: a case has no 'id'")
        return
    where = f"{where}: {case_id}"
    if case_id in seen:
        err(f"{where}: the id is used twice")
    seen.add(case_id)
    if case.get("level") not in (1, 2, 3):
        err(f"{where}: 'level' must be 1, 2 or 3")
    rule = case.get("rule")
    if rule not in rules:
        err(f"{where}: rule '{rule}' is not in the standard")
    elif isinstance(case.get("level"), int) and not rule.startswith(f"L{case['level']}."):
        # A Level 2 case may test the notice for a Level 3 rule, and never the reverse.
        err(f"{where}: rule '{rule}' is not a Level {case['level']} rule")
    if not isinstance(case.get("title"), str) or not case["title"]:
        err(f"{where}: missing 'title'")
    given, expect = case.get("given"), case.get("expect")
    if not isinstance(given, dict):
        err(f"{where}: 'given' must be an object")
        given = {}
    if not isinstance(expect, dict) or not expect:
        err(f"{where}: 'expect' must be a non-empty object")
        expect = {}
    for product in case.get("products", []):
        if product not in ("aa", "cja"):
            err(f"{where}: unknown product '{product}'")
    command = given.get("command")
    if command is not None and command not in CASE_COMMANDS:
        err(f"{where}: unknown command '{command}'")
    sources = given.get("sources", {})
    if not isinstance(sources, dict):
        err(f"{where}: 'given.sources' must be an object")
        sources = {}
    for name, source in sources.items():
        if name not in CASE_SOURCES:
            err(f"{where}: unknown source '{name}'")
        if not isinstance(source, dict):
            err(f"{where}: source '{name}' must be an object")
            continue
        if "credential" in source and source["credential"] not in creds:
            err(f"{where}: source '{name}' names credential '{source['credential']}', which is not a fixture")
        for field_name in list(source.get("omit", [])) + list(source.get("override", {})):
            if field_name not in CREDENTIAL_FIELDS:
                err(f"{where}: source '{name}' names field '{field_name}'")
    for key in ("credential",):
        if key in given and given[key] not in creds:
            err(f"{where}: 'given.{key}' is not a fixture")
    if "credential" in expect and expect["credential"] not in creds:
        err(f"{where}: 'expect.credential' is not a fixture")
    if "source" in expect and expect["source"] not in CASE_SOURCES:
        err(f"{where}: 'expect.source' is not a source name")
    for key, group in (("error", "errors"), ("problem", "errors"), ("notice", "notices"), ("warning", "warnings")):
        value = expect.get(key)
        if value is not None and value not in codes.get(group, {}):
            err(f"{where}: 'expect.{key}' is '{value}', which is not in codes-v1.json under '{group}'")
    for value in expect.get("notice_one_of", []):
        if value not in codes.get("notices", {}):
            err(f"{where}: notice '{value}' is not in codes-v1.json")
    for step in ("sign_in", "product_access"):
        code = (expect.get(step) or {}).get("code")
        if code is not None and code not in codes.get("codes", {}):
            err(f"{where}: {step} code '{code}' is not in codes-v1.json")
    schema = expect.get("json_schema")
    if schema is not None and not (STANDARDS_DIR / "schemas" / f"{schema}.schema.json").is_file():
        err(f"{where}: shape '{schema}' is not in standards/schemas")


def check_standards() -> int:
    """Check the standards folder. Returns the number of cases."""
    if not STANDARDS_DIR.is_dir():
        return 0
    for md in sorted(STANDARDS_DIR.rglob("*.md")):
        check_links(md)
    spec_file = STANDARDS_DIR / "adobe-credentials-v1.md"
    if not spec_file.is_file():
        err("standards/adobe-credentials-v1.md: missing")
        return 0
    rules = set(re.findall(r"^### (L[123]\.[0-9]+) ", spec_file.read_text(encoding="utf-8"), re.M))
    if not rules:
        err("standards/adobe-credentials-v1.md: no rule headings found")

    codes = check_json(STANDARDS_DIR / "codes-v1.json") or {}
    if codes.get("spec") != SPEC:
        err(f"standards/codes-v1.json: 'spec' must be '{SPEC}'")
    for group in ("codes", "errors", "notices", "warnings"):
        if not isinstance(codes.get(group), dict) or not codes[group]:
            err(f"standards/codes-v1.json: '{group}' must be a non-empty object")

    for schema in sorted((STANDARDS_DIR / "schemas").glob("*.json")):
        data = check_json(schema)
        if data is not None and not data.get("$id", "").startswith(SPEC):
            err(f"{schema.relative_to(ROOT)}: '$id' must start with '{SPEC}'")

    cases_dir = STANDARDS_DIR / "cases" / "adobe-credentials-v1"
    fixtures = check_json(cases_dir / "fixtures.json") or {}
    creds = fixtures.get("credentials", {})
    for name, cred in creds.items():
        if set(cred) != CREDENTIAL_FIELDS:
            err(f"fixtures.json: credential '{name}' must hold exactly the four fields")

    seen: set[str] = set()
    tested: set[str] = set()
    for path in sorted(cases_dir.glob("*.json")):
        if path.name == "fixtures.json":
            continue
        data = check_json(path)
        if data is None:
            continue
        where = str(path.relative_to(ROOT))
        if data.get("spec") != SPEC:
            err(f"{where}: 'spec' must be '{SPEC}'")
        if data.get("area") != path.stem:
            err(f"{where}: 'area' must be '{path.stem}'")
        cases = data.get("cases")
        if not isinstance(cases, list) or not cases:
            err(f"{where}: 'cases' must be a non-empty list")
            continue
        for case in cases:
            if not isinstance(case, dict):
                err(f"{where}: a case is not an object")
                continue
            check_case(where, case, rules, creds, codes, seen)
            tested.add(case.get("rule"))
    for rule in sorted(rules - tested):
        err(f"standards: rule {rule} has no case")
    return len(seen)


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print("No skills/ directory found", file=sys.stderr)
        return 1

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    for skill_dir in skill_dirs:
        check_skill(skill_dir)
    check_plugin()
    case_count = check_standards()

    if errors:
        print(f"FAIL: {len(errors)} problem(s) found\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK: {len(skill_dirs)} skills, the plugin manifests and {case_count} standard cases are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
