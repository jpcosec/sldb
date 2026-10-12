"""Pieces of a Markdown file that a link can address: frontmatter and `#Heading` sections."""
from __future__ import annotations
import re

_FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")
_FENCE = re.compile(r"^[ \t]*(```|~~~)")


def strip_frontmatter(markdown: str) -> str:
    """Drop a leading YAML frontmatter block (and the blank lines after it)."""
    return _FRONTMATTER.sub("", markdown, count=1).lstrip("\r\n")


def split_anchor(target: str) -> tuple[str, str | None]:
    """`doc#Section` -> (`doc`, `Section`); no `#` -> (target, None)."""
    base, sep, anchor = target.partition("#")
    return (base.strip(), anchor.strip() or None) if sep else (target, None)


def _headings(lines: list[str]):
    """(index, level, title) of every heading outside code fences."""
    fenced = False
    for i, line in enumerate(lines):
        fenced ^= bool(_FENCE.match(line))
        if not fenced and (m := _HEADING.match(line)):
            yield i, len(m.group(1)), m.group(2).strip().lower()


def extract_section(markdown: str, heading: str) -> str | None:
    """Text of the section titled `heading` (case-insensitive): its heading line down to the
    next heading of the same or a higher level. None if absent."""
    lines, heads = markdown.splitlines(), list(_headings(markdown.splitlines()))
    hit = next(((i, lvl) for i, lvl, t in heads if t == heading.strip().lower()), None)
    if hit is None: return None
    end = next((i for i, lvl, _ in heads if i > hit[0] and lvl <= hit[1]), len(lines))
    return "\n".join(lines[hit[0]:end]).rstrip()
