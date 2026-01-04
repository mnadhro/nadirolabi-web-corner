#!/usr/bin/env python3
"""
gen_indexes.py

Create index.md files in each docs/ subfolder listing markdown pages,
ordered by the page title extracted from YAML frontmatter `title:` if present,
otherwise from the first '# Heading', otherwise fallback to filename.

Usage:
    python gen_indexes.py

Notes:
 - Intended to be idempotent.
 - Requires PyYAML for robust frontmatter parsing; falls back to a simple parser if missing.
"""
import os
from pathlib import Path
import re

DOCS_DIR = Path("docs")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL | re.UNICODE)
HEADING_RE = re.compile(r"^\s{0,3}#\s+(.*)$", re.MULTILINE)

try:
    import yaml
except Exception:
    yaml = None

def parse_frontmatter(text):
    """Return dict of frontmatter if present, else {}."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    raw = m.group(1)
    if yaml:
        try:
            data = yaml.safe_load(raw)
            return data if isinstance(data, dict) else {}
        except Exception:
            pass
    # fallback: simple 'key: value' parse (handles basic title lines)
    out = {}
    for line in raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out

def extract_title(file_path):
    """Return the best title for a markdown file."""
    text = file_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    title = None
    if isinstance(fm, dict):
        title = fm.get("title") or fm.get("Title") or fm.get("name")
        if title:
            return str(title).strip()
    # fallback: first-level heading
    m = HEADING_RE.search(text)
    if m:
        return m.group(1).strip()
    # final fallback: filename (without ext)
    return file_path.stem

def make_index(folder: Path):
    index_file = folder / "index.md"
    # Collect child entries
    entries = []
    for p in sorted(folder.iterdir()):
        if p.name == "index.md":
            continue
        if p.is_dir():
            # If the subdir contains index.md or markdown children, include
            # title from subdir/index.md if exists
            subindex = p / "index.md"
            if subindex.exists():
                title = extract_title(subindex)
                entries.append((str(title), f"{p.name}/index.md"))
            else:
                # fallback to folder name
                entries.append((p.name + "/", f"{p.name}/"))
        elif p.suffix.lower() in {".md", ".markdown"}:
            title = extract_title(p)
            # link should be relative and without leading slash for MkDocs
            entries.append((str(title), p.name))
    if not entries:
        # remove index.md if it exists but no child entries (optional)
        # if index_file.exists():
        #     index_file.unlink()
        return
    # sort entries by title, casefold for Unicode-friendly case-insensitive sort
    entries.sort(key=lambda t: t[0].casefold())

    # Build markdown listing
    listing_lines = []
    for title, link in entries:
        # Escape brackets in title
        safe_title = title.replace("[", "\\[").replace("]", "\\]")
        listing_lines.append(f"- [{safe_title}]({link})")

    # Determine folder title: try to use existing index title or folder name
    folder_title = folder.name or "Home"
    # If root docs folder, make a nicer title
    if folder.resolve() == DOCS_DIR.resolve():
        folder_title = "Home"

    index_content = f"""---
title: {folder_title}
---

# {folder_title}

This folder contains:

{os.linesep.join(listing_lines)}
"""
    # Write idempotently only if content changed (avoid touching timestamps unnecessarily)
    existing = index_file.read_text(encoding="utf-8") if index_file.exists() else ""
    if existing.strip() != index_content.strip():
        index_file.write_text(index_content, encoding="utf-8")
        print(f"Created/Updated: {index_file}")
    else:
        print(f"Unchanged: {index_file}")

def walk_docs():
    if not DOCS_DIR.exists():
        print(f"Docs folder not found: {DOCS_DIR}")
        return
    for root, dirs, files in os.walk(DOCS_DIR):
        folder = Path(root)
        make_index(folder)

if __name__ == "__main__":
    walk_docs()

