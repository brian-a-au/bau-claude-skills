#!/usr/bin/env python3
"""Copy the shared cases, the JSON shapes and the codes into a tool repo.

Usage: python3 standards/sync_cases.py <destination folder> [--check]

The script copies the files of one version of the standard and writes SOURCE.json
beside them. SOURCE.json records the commit and a SHA-256 for each file. With
--check the script copies nothing. It exits 1 when the destination differs from
this folder. It uses the standard library only.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSION = "adobe-credentials-v1"


def sources() -> list[Path]:
    files = sorted((HERE / "cases" / VERSION).glob("*.json"))
    files += sorted((HERE / "schemas").glob("*-v1.schema.json"))
    files.append(HERE / "codes-v1.json")
    return files


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def commit() -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(HERE), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return out.stdout.strip()


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--check"]
    check = "--check" in argv
    if len(args) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    dest = Path(args[0])
    files = {p.name: digest(p) for p in sources()}

    if check:
        wrong = [n for n, d in files.items() if not (dest / n).is_file() or digest(dest / n) != d]
        extra = sorted(
            p.name for p in dest.glob("*.json") if p.name not in files and p.name != "SOURCE.json"
        )
        for name in wrong:
            print(f"differs or is missing: {name}", file=sys.stderr)
        for name in extra:
            print(f"not in the standard: {name}", file=sys.stderr)
        return 1 if wrong or extra else 0

    dest.mkdir(parents=True, exist_ok=True)
    for path in sources():
        shutil.copyfile(path, dest / path.name)
    record = {"spec": "adobe-credentials/v1", "commit": commit(), "files": files}
    (dest / "SOURCE.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"Copied {len(files)} files to {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
