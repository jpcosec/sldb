"""
Handles the ingestion of raw source files and their transformation into Knowledge Graph draft nodes.
"""

from __future__ import annotations

import re
from pathlib import Path

from .scanner import load_wikiignore_rules, match_ignore_reason


def ingest_raw_sources(
    source_dir: Path,
    dest_dir: Path,
    project_root: Path | None = None,
    overwrite: bool = False,
    manifest_path: Path | None = None,
) -> list[Path]:
    """
    Scans a directory for raw source files and generates draft markdown nodes for each valid file.
    Draft nodes land in dest_dir/<source_subdir>/ mirroring the first path component under source_dir.
    After ingestion, generates an INDEX.md per subdirectory.
    """
    from .manifest import compute_content_hash, add_to_manifest

    root = project_root or source_dir.parent
    ignore_rules = load_wikiignore_rules(root / ".wikiignore")
    written: list[Path] = []
    subdir_nodes: dict[str, list[dict]] = {}

    for source_path in sorted(
        path for path in source_dir.rglob("*.md") if path.is_file()
    ):
        rel_to_source = source_path.relative_to(source_dir)
        if any(part.startswith(".") for part in rel_to_source.parts):
            continue
        rel_source = source_path.relative_to(root).as_posix()
        if match_ignore_reason(rel_source, ignore_rules) is not None:
            continue

        source_subdir = _source_subdir(rel_to_source)
        subdir_dest = dest_dir / source_subdir if source_subdir else dest_dir

        source_hash = compute_content_hash(source_path)
        if manifest_path:
            add_to_manifest(root, manifest_path, source_path)

        nodes = decompose_source(source_path)
        for title, content, node_type in nodes:
            draft_slug = slugify(title)
            draft_path = subdir_dest / f"{draft_slug}.md"
            if draft_path.exists() and not overwrite:
                continue
            draft_path.parent.mkdir(parents=True, exist_ok=True)
            node_id = _compute_node_id(dest_dir, source_subdir, draft_slug)
            draft_path.write_text(
                render_draft(
                    rel_source, node_id, title, content, node_type, source_hash
                ),
                encoding="utf-8",
            )
            written.append(draft_path)
            abstract = _extract_abstract(content)
            subdir_nodes.setdefault(source_subdir, []).append(
                {"node_id": node_id, "title": title, "abstract": abstract}
            )

    for source_subdir, entries in subdir_nodes.items():
        index_path = (
            (dest_dir / source_subdir / "INDEX.md")
            if source_subdir
            else (dest_dir / "INDEX.md")
        )
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(_render_index(source_subdir, entries), encoding="utf-8")

    return written


def _source_subdir(rel_to_source: Path) -> str:
    """Returns the first path component of a relative source path, or empty string if top-level."""
    parts = rel_to_source.parts
    return parts[0] if len(parts) > 1 else ""


def _compute_node_id(dest_dir: Path, source_subdir: str, draft_slug: str) -> str:
    """Computes the canonical node_id for a draft node given its destination details."""
    if dest_dir.is_absolute():
        if dest_dir.parent.name == "wiki":
            base = Path(dest_dir.parent.name) / dest_dir.name
        elif dest_dir.parent.name == "desk":
            base = Path("desk") / dest_dir.name
        else:
            base = Path(dest_dir.name)
    else:
        base = dest_dir
    if source_subdir:
        return f"doc:{(base / source_subdir / draft_slug).as_posix()}.md"
    return f"doc:{(base / draft_slug).as_posix()}.md"


def _extract_abstract(content: str) -> str:
    """Extracts the first non-empty line from content as the abstract."""
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return lines[0] if lines else "No abstract provided."


def _render_index(source_subdir: str, entries: list[dict]) -> str:
    """Renders an INDEX.md listing all draft node IDs, titles, and abstracts."""
    label = source_subdir or "drafts"
    lines = [f"# Index: {label}", ""]
    for entry in entries:
        lines.append(
            f"- **{entry['node_id']}** — {entry['title']}: {entry['abstract']}"
        )
    lines.append("")
    return "\n".join(lines)


def decompose_source(source_path: Path) -> list[tuple[str, str, str]]:
    """
    Splits a single source file into multiple atomic nodes based on its internal heading structure.
    """
    try:
        text = source_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [(source_path.stem, f"Binary source `{source_path.name}`.", "concept")]

    # Split by ## headings
    sections = re.split(r"\n(?=## )", "\n" + text)
    nodes = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.splitlines()
        if lines[0].startswith("## "):
            title = lines[0].lstrip("# ").strip()
            content = "\n".join(lines[1:]).strip()
            node_type = "concept"
            if "rule" in title.lower() or "standard" in title.lower():
                node_type = "doc_standard"
        else:
            if lines[0].startswith("# "):
                title = lines[0].lstrip("# ").strip()
                content = "\n".join(lines[1:]).strip()
            else:
                title = source_path.stem.replace("_", " ").title()
                content = section
            node_type = "concept"

        nodes.append((title, content, node_type))

    return nodes


def render_draft(
    rel_source: str,
    node_id: str,
    title: str,
    content: str,
    node_type: str = "concept",
    source_hash: str = "",
) -> str:
    """
    Generates the markdown content for a draft node, including required frontmatter.
    """
    from datetime import datetime

    abstract = _extract_abstract(content)
    compiled_at = datetime.now().isoformat()

    lines = [
        "---",
        "identity:",
        f'  node_id: "{node_id}"',
        f'  node_type: "{node_type}"',
        "edges:",
        f'  - {{target_id: "raw:{rel_source}", relation_type: "documents"}}',
        "compliance:",
        '  status: "planned"',
        "  failing_standards: []",
        "source:",
        f'  source_path: "{rel_source}"',
        f'  source_hash: "{source_hash}"',
        f'  compiled_at: "{compiled_at}"',
        '  compiled_from: "wiki-compiler"',
        "---",
        "",
        abstract,
        "",
        f"## Details",
        "",
        content,
        "",
        f"Generated from `{rel_source}`.",
    ]
    return "\n".join(lines)


def summarize_source(source_path: Path) -> tuple[str, str]:
    """
    Extracts a concise title and summary from a source file for preliminary indexing.
    """
    try:
        text = source_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        title = source_path.stem.replace("_", " ").replace("-", " ").title()
        return title, f"Binary or non-UTF-8 source captured from `{source_path.name}`."
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title = source_path.stem.replace("_", " ").replace("-", " ").title()
    if lines and lines[0].startswith("#"):
        title = lines[0].lstrip("# ")
        lines = lines[1:]
    summary = lines[0] if lines else f"Draft generated from `{source_path.name}`."
    return title, summary


def draft_node_path(dest_dir: Path, stem: str) -> str:
    """
    Computes the canonical node path for a draft markdown file.
    Kept for backwards compatibility.
    """
    if dest_dir.is_absolute():
        base_path = Path(dest_dir.name)
        if dest_dir.parent.name == "wiki":
            base_path = Path(dest_dir.parent.name) / dest_dir.name
    else:
        base_path = dest_dir
    return (base_path / f"{slugify(stem)}.md").as_posix()


_MAX_SLUG_LENGTH = 80


def slugify(value: str) -> str:
    """
    Converts a string into a URL-friendly slug using underscores, capped at 80 chars.
    """
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    return (slug or "draft_node")[:_MAX_SLUG_LENGTH].rstrip("_")
