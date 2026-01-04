#!/usr/bin/env python3
"""
gen_indexes.py
Create a simple index.md in each docs subfolder listing files and subfolders.
Run from project root. Intended to be minimal and idempotent.
"""
import os
from pathlib import Path

DOCS_DIR = Path("docs")

INDEX_TEMPLATE = """---
title: {title}
---

# {title}

This folder contains:

{listing}
"""

def make_index(folder: Path):
    index_file = folder / "index.md"
    if index_file.exists():
        return
    items = []
    for p in sorted(folder.iterdir()):
        if p.name == "index.md": continue
        if p.is_dir():
            items.append(f"- **{p.name}/** — see [{p.name}]({p.name}/index.md)")
        elif p.suffix.lower() in {".md", ".markdown"}:
            # link without extension
            name = p.stem
            items.append(f"- [{name}]({p.name})")
    if not items:
        # don't create empty indexes
        return
    listing = "\n".join(items)
    title = folder.name or "Home"
    index_file.write_text(INDEX_TEMPLATE.format(title=title, listing=listing), encoding="utf-8")
    print(f"Created {index_file}")

def walk_docs():
    for root, dirs, files in os.walk(DOCS_DIR):
        folder = Path(root)
        make_index(folder)

if __name__ == "__main__":
    walk_docs()

