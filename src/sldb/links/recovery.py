from __future__ import annotations
from collections.abc import Mapping
from pathlib import Path
from sldb.store.io import load_store_index
from sldb.store.predicates import predicate_axes
from .parser import parse_links
from .resolver import resolve_link_target
from .sections import extract_section, split_anchor, strip_frontmatter

def _process_link(link, doc_path, store_path, inc_trans):
    res = resolve_link_target(link.target, doc_path, store_path, link.predicate, link.w5h1_type)
    res.kind, res.raw = link.kind, link.raw
    if res.resolved and res.path and (anchor := split_anchor(link.target)[1]) is not None:
        res.resolved = extract_section(strip_frontmatter(Path(res.path).read_text("utf-8")), anchor) is not None
    return res

def _dedup_links(links: list[dict]) -> list[dict]:
    seen, unique = set(), []
    for item in links:
        if (key := (item["target"], item["kind"])) not in seen: unique.append(item); seen.add(key)
    return unique

def recover_links(doc_path: Path, store_path: Path | None, include_transclusions: bool = False, depth: int = 1, seen: set[Path] | None = None, predicate_types: Mapping[str, str] | None = None) -> dict:
    doc_path, seen = doc_path.resolve(), seen or set()
    pt = predicate_types if predicate_types is not None else (predicate_axes(load_store_index(store_path).predicates) if store_path else {})
    if doc_path in seen or depth < 1: return {"root": doc_path.stem, "path": str(doc_path), "links": [], "unresolved": []}
    seen.add(doc_path)
    links = [{"target": e.target, "kind": e.kind, "resolved": e.resolved, "path": e.path, "source": e.source, "predicate": e.predicate, "w5h1_type": e.w5h1_type} for e in [_process_link(l, doc_path, store_path, include_transclusions) for l in parse_links(doc_path.read_text("utf-8"), pt)]]
    if depth > 1:
        for e in [l for l in links if l["resolved"] and l["path"]]: links.extend(recover_links(Path(e["path"]), store_path, include_transclusions, depth - 1, seen, pt)["links"])
    return {"root": doc_path.stem, "path": str(doc_path), "links": (u := _dedup_links(links)), "unresolved": [i["target"] for i in u if not i["resolved"]]}
