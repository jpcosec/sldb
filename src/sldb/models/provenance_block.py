"""The `sldb` block in a document's frontmatter: read it, strip it, attach it.

The block is text the store carries, not a field of the model: the extractor ignores a
frontmatter key no template declares, so reading it needs no model, and attaching it never
changes what the model extracts (`content_hash` stays; `source_hash` moves, as with any write).
"""

from __future__ import annotations

import re
from typing import Any

import yaml

from sldb.models.provenance import BLOCK_KEY

_FENCE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
_OWN_LINE = re.compile(rf"^{BLOCK_KEY}:.*\n(?:[ \t]+.*\n?|\n)*", re.MULTILINE)


def read_block(text: str) -> dict[str, Any] | None:
    """The mapping under the `sldb` key of the frontmatter, or None."""
    fence = _FENCE.match(text)
    if fence is None:
        return None
    try:
        data = yaml.safe_load(fence.group(1))
    except yaml.YAMLError:
        return None
    return data.get(BLOCK_KEY) if isinstance(data, dict) and isinstance(data.get(BLOCK_KEY), dict) else None


def strip_block(text: str) -> str:
    """`text` without its `sldb` block; a frontmatter left empty goes with it."""
    fence = _FENCE.match(text)
    if fence is None or read_block(text) is None:
        return text
    body = _OWN_LINE.sub("", fence.group(1) + "\n", count=1).rstrip("\n")
    rest = text[fence.end():]
    return f"---\n{body}\n---\n{rest}" if body.strip() else rest.lstrip("\n")


def attach_block(text: str, block: dict[str, Any]) -> str:
    """`text` with `block` under the `sldb` key, first in its frontmatter (created if absent)."""
    bare = strip_block(text)
    dumped = yaml.safe_dump({BLOCK_KEY: block}, sort_keys=False, allow_unicode=True).rstrip("\n")
    fence = _FENCE.match(bare)
    if fence is None:
        return f"---\n{dumped}\n---\n\n{bare}"
    return f"---\n{dumped}\n{fence.group(1)}\n---\n{bare[fence.end():]}"
