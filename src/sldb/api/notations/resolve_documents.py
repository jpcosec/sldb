"""Documents of any model styled with a notation, without needing a SpecDoc."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.fragments import fragments_of
from sldb.api.notations.legend import legend
from sldb.api.notations.node_view import node_view, pick_glyph
from sldb.api.notations.notation_context import notation_context
from sldb.api.notations.store_docs import load_docs
from sldb.api.notations.view_links import collect_links


def _nodes(docs: dict, node_refs: list[str], np_: dict, glyphs: list, spec_style: dict | None, palette: dict | None) -> list:
    """The resolved node of each document in the view."""
    markers = list(np_.get("markers") or [])
    return [node_view(r, docs[r]["payload"], glyphs, markers, docs[r]["model"], spec_style, palette) for r in node_refs]


def _split_gaps(docs: dict, node_refs: list[str], glyphs: list) -> tuple[list[str], list[dict[str, str]]]:
    """The refs some glyph matches, and the `{id, model}` of those no glyph matches."""
    drawn: list[str] = []
    gaps: list[dict[str, str]] = []
    for r in node_refs:
        if pick_glyph(docs[r]["payload"], glyphs, docs[r]["model"]) is None:
            gaps.append({"id": r, "model": docs[r]["model"]})
        else:
            drawn.append(r)
    return drawn, gaps


def _header(ref: str, np_: dict[str, Any]) -> dict[str, Any]:
    """What the notation says about the whole view."""
    return {
        "notation": ref,
        "palette": np_.get("palette") or "",
        "level": np_.get("level", "types"),
        "layout": dict(np_.get("layout") or {"kind": "graph"}),
    }


def _result(ref: str, np_: dict, nodes: list, links_out: list, skipped: list, glyphs: list, links: list, palette, gaps: list) -> dict:
    """The resolved view: header, nodes, links, fragments, skipped and legend."""
    return {
        **_header(ref, np_),
        "nodes": nodes,
        "links": links_out,
        "fragments": fragments_of(links_out),
        "skipped": skipped,
        "gaps": gaps,
        "legend": legend(glyphs, links, nodes, palette),
    }


def resolve_documents(
    store: Path | str,
    notation_ref: str,
    doc_refs: list[str],
    *,
    relation_refs: list[str] | None = None,
    spec_style: dict | None = None,
    pythonpath: str | None = None,
    docs: dict[str, dict[str, Any]] | None = None,
    strict: bool = True,
) -> dict[str, Any]:
    """Documents of any model styled with a notation: nodes, links, fragments, skipped, gaps, legend.

    A document no glyph matches is a gap (`{id, model}`) unless `strict`, which raises ViewError."""
    docs = docs if docs is not None else load_docs(Path(store), pythonpath)
    ref, np_, palette, glyphs, links = notation_context(docs, notation_ref)
    node_refs = [r for r in doc_refs if r in docs]
    gaps: list[dict[str, str]] = []
    if not strict:
        node_refs, gaps = _split_gaps(docs, node_refs, glyphs)
    nodes = _nodes(docs, node_refs, np_, glyphs, spec_style, palette)
    out_links, skipped = collect_links(docs, node_refs, links, relation_refs, ref, palette)
    return _result(ref, np_, nodes, out_links, skipped, glyphs, links, palette, gaps)
