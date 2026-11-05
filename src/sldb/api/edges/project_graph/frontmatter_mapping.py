"""The YAML frontmatter of a Markdown document, read as a mapping."""

from __future__ import annotations

import yaml

# frontmatter block -> parsed mapping (None when it is not one); a block is parsed once.
_PARSED: dict[str, dict | None] = {}
_PARSED_LIMIT = 20_000


def frontmatter_mapping(text: str) -> dict | None:
    """The mapping between the leading `---` lines, or None when there is none or it is not one.

    The parse is kept per block text and shared: callers read it and never change it.

    Args:
        text: The document's text.

    Returns:
        The parsed frontmatter, or None for no frontmatter, invalid YAML or a non-mapping.
    """
    if not text.startswith("---\n"):
        return None
    parts = text.split("---\n", 1)[1].split("\n---", 1)
    if len(parts) != 2:
        return None
    if parts[0] not in _PARSED:
        if len(_PARSED) >= _PARSED_LIMIT:
            _PARSED.clear()
        _PARSED[parts[0]] = _parse_block(parts[0])
    return _PARSED[parts[0]]


def _parse_block(block: str) -> dict | None:
    try:
        loaded = yaml.safe_load(block)
    except yaml.YAMLError:
        return None
    return loaded if isinstance(loaded, dict) else None


def is_record_text(text: str) -> bool:
    """Whether a document carries the archived-record marker (`record: true`) in its frontmatter."""
    mapping = frontmatter_mapping(text)
    return mapping is not None and mapping.get("record") is True
