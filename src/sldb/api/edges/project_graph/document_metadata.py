"""A document's declared id and title, parsed once per text of its file."""

from __future__ import annotations

from pathlib import Path

import yaml

from sldb.api.edges.project_graph.frontmatter_mapping import frontmatter_mapping
from sldb.store.source_guard import aggregate_text

# path -> (text, metadata)
_METADATA: dict[str, tuple[str, dict[str, str]]] = {}


def document_metadata(path: Path, root: Path | None = None) -> dict[str, str]:
    """`id` and `title` of a document: from YAML, frontmatter, or its `# ` heading and `ID:` line.

    Args:
        path: The document file.
        root: The project root: a path the read guard refuses there (outside it, or a symlink)
            is warned and carries no metadata. None: the file's own folder (a symlink is still refused).

    Returns:
        A fresh mapping holding the keys that were found.
    """
    root = root if root is not None else path.absolute().parent
    if (text := aggregate_text(root, path, path.relative_to(root).as_posix() if path.is_relative_to(root) else path.name)) is None:
        return {}
    hit = _METADATA.get(str(path))
    if hit is None or hit[0] != text:
        hit = _METADATA[str(path)] = (text, _parse_metadata(path, text))
    return dict(hit[1])


def _parse_metadata(path: Path, text: str) -> dict[str, str]:
    if path.suffix in {".yaml", ".yml"}:
        return _yaml_metadata(text)
    metadata = _text_metadata(text)
    frontmatter = _mapping_metadata(frontmatter_mapping(text) or {})
    if frontmatter:
        metadata.update(frontmatter)
    return metadata


def _yaml_metadata(text: str) -> dict[str, str]:
    try:
        loaded = yaml.safe_load(text)
    except yaml.YAMLError:
        return {}  # a file that is not a single YAML document carries no document metadata
    return _mapping_metadata(loaded) if isinstance(loaded, dict) else {}


def _mapping_metadata(loaded: dict) -> dict[str, str]:
    return {key: loaded[key].strip() for key in ("id", "title") if isinstance(loaded.get(key), str) and loaded[key].strip()}


def _text_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and "title" not in metadata:
            metadata["title"] = stripped.removeprefix("# ").strip()
        if stripped.startswith("ID:") and "id" not in metadata:
            metadata["id"] = stripped.removeprefix("ID:").strip()
        if "id" in metadata and "title" in metadata:
            break
    return metadata
