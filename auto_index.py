import os
from pathlib import Path

def on_page_markdown(markdown, page, config, files):
    # Only apply to index pages
    if not page.file.src_path.endswith("index.md"):
        return markdown
    # Skip blog and root index
    if page.file.src_path == "index.md":
        return markdown

    folder = Path(page.file.abs_src_path).parent
    links = []
    for f in sorted(folder.glob("*.md")):
        if f.name == "index.md":
            continue
        title = f.stem.replace("_", " ").replace("-", " ").title()
        links.append(f"- [{title}]({f.name})")

    if links:
        markdown += "\n\n## Pages\n\n" + "\n".join(links)
    return markdown
