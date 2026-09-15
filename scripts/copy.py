#!/usr/bin/env python3
"""Inventory every published piece of Foresee copy.

Tag copy in place with a comment the scanner can see:

  // @copy landing.hero audience=human
  {/* @copy chrome.announcement audience=human */}
  <!-- @copy docs audience=human url=/docs -->
  # @copy llms audience=agent url=/llms.txt

`@copy <id>` is required. Optional `key=value` attrs (audience, url,
source, file, …) are free-form. Use `file=` when the tag cannot live in
the copy itself (JSON).

  python3 scripts/copy.py                 list all
  python3 scripts/copy.py readme          filter (id / path / attr substring)
  python3 scripts/copy.py --audience agent
  python3 scripts/copy.py --json
  python3 scripts/copy.py --check         fail if required copy has no tag
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THIS = Path(__file__).resolve()

SKIP_DIR = {
    ".git",
    ".claude",
    ".venv",
    "__pycache__",
    "dist",
    "node_modules",
}

TEXT_EXT = {
    ".css",
    ".html",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

TAG_RE = re.compile(r"@copy\s+(\S+)((?:\s+[A-Za-z][\w-]*\s*=\s*\S+)*)")
ATTR_RE = re.compile(r"([A-Za-z][\w-]*)\s*=\s*(\S+)")

REQUIRED_JSON = (
    "plugins/foresee/plugin.json",
    "plugins/foresee/.claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "server.json",
)


def walk(root: Path) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR]
        for name in filenames:
            path = Path(dirpath) / name
            if path.resolve() == THIS:
                continue
            if Path(name).suffix in TEXT_EXT:
                out.append(path)
    return out


def parse_attrs(raw: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in ATTR_RE.finditer(raw)}


def collect() -> list[dict]:
    entries = []
    for path in walk(ROOT):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "\0" in text:
            continue
        rel = path.relative_to(ROOT).as_posix()
        for i, line in enumerate(text.splitlines(), 1):
            for m in TAG_RE.finditer(line):
                entries.append(
                    {
                        "id": m.group(1),
                        "file": rel,
                        "line": i,
                        "attrs": parse_attrs(m.group(2) or ""),
                    }
                )
    entries.sort(key=lambda e: (e["id"], e["file"]))
    return entries


def tagged_paths(entries: list[dict]) -> set[str]:
    paths: set[str] = set()
    for e in entries:
        paths.add(e["file"])
        if e["attrs"].get("file"):
            paths.add(e["attrs"]["file"])
    return paths


def required_files() -> list[str]:
    files: list[str] = []
    readme = ROOT / "README.md"
    if readme.is_file():
        files.append("README.md")
    plugins = ROOT / "plugins"
    if plugins.is_dir():
        for path in sorted(plugins.rglob("*.md")):
            files.append(path.relative_to(ROOT).as_posix())
    for rel in REQUIRED_JSON:
        if (ROOT / rel).is_file():
            files.append(rel)
    return files


def matches_filter(entry: dict, query: str | None, audience: str | None) -> bool:
    if audience and entry["attrs"].get("audience") != audience:
        return False
    if not query:
        return True
    hay = " ".join(
        filter(
            None,
            [entry["id"], entry["file"], entry["attrs"].get("file"), *entry["attrs"].values()],
        )
    ).lower()
    return query.lower() in hay


def format_row(entry: dict) -> dict[str, str]:
    dest = entry["attrs"].get("file") or entry["file"]
    loc = f"{entry['file']}:{entry['line']}"
    extras = " ".join(
        f"{k}={v}" for k, v in entry["attrs"].items() if k != "file"
    )
    return {"id": entry["id"], "dest": dest, "loc": loc, "extras": extras}


def print_table(rows: list[dict]) -> None:
    if not rows:
        print("No matching @copy tags.")
        return
    data = [[r["id"], r["dest"], r["loc"], r["extras"]] for r in rows]
    headers = ["ID", "COPY", "TAG", "ATTRS"]
    widths = [
        max(len(headers[i]), *(len(row[i]) for row in data))
        for i in range(4)
    ]

    def line(row: list[str]) -> str:
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))

    print(line(headers))
    print("  ".join("-" * w for w in widths))
    for row in data:
        print(line(row))
    print(f"\n{len(rows)} tagged")


def check(entries: list[dict]) -> int:
    tagged = tagged_paths(entries)
    missing = [f for f in required_files() if f not in tagged]
    if not missing:
        print(f"ok — {len(entries)} tags, every required copy file is tagged")
        return 0
    print("untagged copy files:", file=sys.stderr)
    for f in missing:
        print(f"  {f}", file=sys.stderr)
    print(
        "\nAdd an @copy comment, or list the file in content/external.md",
        file=sys.stderr,
    )
    return 1


def parse_args(argv: list[str]) -> tuple[set[str], str | None, str | None]:
    flags: set[str] = set()
    query = None
    audience = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--audience":
            i += 1
            audience = argv[i] if i < len(argv) else None
        elif a.startswith("--audience="):
            audience = a[len("--audience=") :]
        elif a.startswith("--"):
            flags.add(a)
        elif query is None:
            query = a
        i += 1
    return flags, query, audience


def main() -> int:
    flags, query, audience = parse_args(sys.argv[1:])
    entries = collect()
    if "--check" in flags:
        return check(entries)
    rows = [
        format_row(e)
        for e in entries
        if matches_filter(e, query, audience)
    ]
    if "--json" in flags:
        print(json.dumps(rows, indent=2))
    else:
        print_table(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
