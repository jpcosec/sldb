"""`docs compose --render-links`: [[x]] -> [title](relative/path.md), [pred:: [[x]]] -> *pred*: [title](...)."""
from __future__ import annotations
import os
import re
from pathlib import Path
import yaml
from .parser import INLINE_PREDICATE_LINK_PATTERN
from .resolver import resolve_link_target
from .sections import split_anchor

_PLAIN = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")
_FRONT = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---", re.DOTALL)

def _title(path: Path, fallback: str) -> str:
    m = _FRONT.match(path.read_text("utf-8"))
    meta = yaml.safe_load(m.group(1)) if m else None
    return str(meta["title"]) if isinstance(meta, dict) and meta.get("title") else fallback

def _slug(heading: str) -> str:
    return re.sub(r"[^\w\- ]", "", heading.lower()).strip().replace(" ", "-")

def _link(target: str, doc: Path, sp: Path | None, base: Path) -> str | None:
    res = resolve_link_target(target.strip(), doc, sp)
    if not res.path: return None
    name, anchor = split_anchor(target.strip())
    href = Path(os.path.relpath(res.path, base)).as_posix() + (f"#{_slug(anchor)}" if anchor else "")
    return f"[{_title(Path(res.path), name)}]({href})"

def render_links(markdown: str, doc: Path, sp: Path | None, base: Path) -> str:
    """Rewrite the resolvable links of `markdown` (a file at `doc`); the rest stays as written."""
    def pred(m: re.Match[str]) -> str:
        link = None if m.group(2) else _link(m.group(3), doc, sp, base)
        return m.group(0) if link is None else f"*{m.group(1)}*: {link}"
    markdown = INLINE_PREDICATE_LINK_PATTERN.sub(pred, markdown)
    return _PLAIN.sub(lambda m: _link(m.group(1), doc, sp, base) or m.group(0), markdown)
