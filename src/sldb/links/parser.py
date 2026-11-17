from __future__ import annotations
import re
from collections.abc import Mapping
from .parsed_link import ParsedLink
from .scan_text import scannable_text

LINK_PATTERN = re.compile(r"(!)?\[\[([^\]]+)\]\]")
INLINE_PREDICATE_LINK_PATTERN = re.compile(r"\[([a-zA-Z0-9_-]+)::\s*(!)?\[\[([^\]]+)\]\]\]")

def _parse_inline(m: re.Match, p_types: Mapping[str, str], seen: set) -> ParsedLink:
    seen.add(m.span())
    return ParsedLink(m.group(0), m.group(3).strip(), "transclusion" if m.group(2) else "predicate_link", m.group(1).strip(), p_types.get(m.group(1).strip(), "CUSTOM"))

def _parse_standard(m: re.Match, seen: set) -> ParsedLink | None:
    if any(s[0] <= m.start() and m.end() <= s[1] for s in seen): return None
    return ParsedLink(m.group(0), m.group(2).strip(), "transclusion" if m.group(1) else "link", None, None)

def parse_links(markdown: str, predicate_types: Mapping[str, str] | None = None) -> list[ParsedLink]:
    """Links of the Markdown outside code (fenced, indented and inline, as markdown-it parses it):
    predicate links first, then the others, each group in document order."""
    if "[[" not in markdown:
        return []  # both patterns need it: no parse
    seen, p_types, text = set(), predicate_types or {}, scannable_text(markdown)
    inline = [_parse_inline(m, p_types, seen) for m in INLINE_PREDICATE_LINK_PATTERN.finditer(text)]
    return inline + [p for m in LINK_PATTERN.finditer(text) if (p := _parse_standard(m, seen))]
