from __future__ import annotations
import re
from pathlib import Path
from .parser import LINK_PATTERN
from .resolver import resolve_link_target
from .render import render_links
from .sections import extract_section, split_anchor, strip_frontmatter

def _load(dp: Path, root: bool, section: str | None) -> str | None:
    text = dp.read_text("utf-8")
    text = text if root else strip_frontmatter(text)
    return text if section is None else extract_section(text, section)

def _expand(m: re.Match[str], dp: Path, sp: Path | None, s: tuple[Path, ...], tr: list, un: list, lb: Path | None) -> str:
    raw = m.group(2).strip()
    if not m.group(1): return m.group(0)
    res = resolve_link_target(raw, dp, sp)
    if not res.path: un.append(raw); return m.group(0)
    n = compose_document(Path(res.path), sp, (*s, dp), False, split_anchor(raw)[1], lb)
    if n.get("missing_section"): un.append(raw); return m.group(0)
    tr.append(raw); un.extend(n["unresolved"]); tr.extend(n["transclusions"]); return n["markdown"].rstrip()

def compose_document(dp: Path, sp: Path | None, s: tuple[Path, ...] = (), _root: bool = True, section: str | None = None, links_base: Path | None = None) -> dict:
    """Expand `![[x]]` / `![[x#Section]]`. An included document loses its YAML frontmatter;
    only the root keeps its own. `s` is the include chain (cycle guard), so a document may be included twice."""
    dp, tr, un = dp.resolve(), [], []
    if (text := _load(dp, _root, section)) is None: return {"markdown": "", "transclusions": [], "unresolved": [], "missing_section": True}
    if dp in s: return {"markdown": text, "transclusions": [], "unresolved": []}
    if links_base is not None: text = render_links(text, dp, sp, links_base)
    md = LINK_PATTERN.sub(lambda m: _expand(m, dp, sp, s, tr, un, links_base), text)
    return {"root": dp.stem, "path": str(dp), "markdown": md, "transclusions": sorted(dict.fromkeys(tr)), "unresolved": sorted(dict.fromkeys(un))}
