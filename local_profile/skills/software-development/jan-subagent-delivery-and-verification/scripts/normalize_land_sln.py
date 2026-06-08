#!/usr/bin/env python3
"""Normalize a Visual Studio .sln header for LAND8R/LAND8116 recovery.

Usage:
    python scripts/normalize_land_sln.py C:/Users/yjs/Desktop/JAN/LAND8R-24HS4/LAND.sln

What it fixes:
- UTF-8 BOM followed by a blank physical first line, then the solution header.
- Mixed CRLF/LF newlines.

It writes UTF-8 BOM + CRLF and creates a timestamped .bak_YYYYmmdd_HHMMSS backup.
"""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def normalize(path: Path) -> tuple[Path, bool, bytes, bytes]:
    before = path.read_bytes()
    backup = path.with_name(path.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    backup.write_bytes(before)

    text = before.decode("utf-8-sig")
    text = text.lstrip("\r\n")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    after = ("\ufeff" + text).replace("\n", "\r\n").encode("utf-8")
    changed = after != before
    if changed:
        path.write_bytes(after)
    return backup, changed, before[:16], after[:16]


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize LAND.sln BOM/header/newlines.")
    parser.add_argument("sln", type=Path, help="Path to LAND.sln")
    args = parser.parse_args()

    if not args.sln.exists():
        raise SystemExit(f"not found: {args.sln}")

    backup, changed, before, after = normalize(args.sln)
    print(f"backup={backup}")
    print(f"changed={changed}")
    print(f"before16={before.hex(' ')}")
    print(f"after16={after.hex(' ')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
