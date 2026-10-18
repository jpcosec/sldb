"""What a rewrite of a document would lose: its blocks that do not survive render(extract(text)).

A model that cannot read its own document (written by hand, or by an older template) extracts
empty fields; the hashes stay consistent over that empty extraction, so `stores check` passed,
and any rewrite wrote the empties (deskops found 34 such documents and lost content in
`deskops edit`; inbox 20260924-011411). This compares the document with its own rewrite.
"""

from __future__ import annotations

import re
from typing import Any

_CONTENT = ("paragraph", "fence", "code_block", "bullet_list", "ordered_list", "blockquote", "table", "html_block")


def rewrite_loss(model_type: Any, markdown: str) -> list[str]:
    """The source of each body block a rewrite would drop, in document order; [] when none
    (or when the document does not extract at all: that is reported elsewhere)."""
    from sldb.runtime.validation import extract_model_data, render_model_markdown

    try:
        rewritten = _flat(render_model_markdown(model_type, extract_model_data(model_type, markdown)))
    except Exception:  # noqa: BLE001 - a document that does not extract is another finding
        return []
    return [src for src in _content_blocks(markdown, _derived_headings(model_type.__template__)) if _flat(src) not in rewritten]


def _content_blocks(markdown: str, derived: set[str]) -> list[str]:
    """The source of each content block, except those under a heading the template derives."""
    from sldb.core.ast import AST_Handler

    lines, under, blocks = markdown.splitlines(), None, []
    for node in AST_Handler().split_nodes(markdown):
        if node.type == "heading":
            under = _flat(node.children[0].content if node.children else node.content)
        elif node.type in _CONTENT and node.map and under not in derived:
            blocks.append("\n".join(lines[node.map[0]:node.map[1]]).strip())
    return [b for b in blocks if b]


def _derived_headings(template: str) -> set[str]:
    """Headings whose section the template fills only with `render`/`py` markers: what sits
    there is regenerated from other data on every write, so a stale copy is not a loss."""
    from sldb.core.handlers.utils import parse_marker

    sections: dict[str, list] = {}
    heading = None
    for line in template.splitlines():
        if (m := re.match(r"#{1,6}\s+(.*)", line)) and "⸢" not in line:
            heading = _flat(m.group(1))
        elif heading is not None:
            sections.setdefault(heading, []).extend(parse_marker(x) for x in re.findall(r"⸢([^⸥]+)⸥", line))
    return {h for h, markers in sections.items() if markers and not any(mk.is_reversible or mk.is_optional for mk in markers)}


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
