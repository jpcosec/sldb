"""The links of a view: `contains` between nodes and the relation docs among them."""

from __future__ import annotations

from typing import Any

from sldb.api.notations.link_view import link_view
from sldb.notations.notation import ANY_RELATION


def _contained(docs: dict, node_refs: list[str]) -> list[tuple[str, str]]:
    """`(parent, child)` pairs of `contains` where both are in the view."""
    in_view = set(node_refs)
    return [(ref, c) for ref in node_refs for c in docs[ref]["payload"].get("contains") or [] if c in in_view]


def _contains_links(docs: dict, node_refs: list[str], link: dict | None, palette: dict | None, skipped: list[str]) -> list:
    """One link per contained pair; pairs are skipped if the notation has no `contains` link."""
    out: list[dict[str, Any]] = []
    for ref, child in _contained(docs, node_refs):
        if link is None:
            skipped.append(f"{ref} contains {child}")
        else:
            out.append(link_view(ref, child, link, None, None, palette))
    return out


def _relation_docs(docs: dict, in_view: set[str], wanted: set[str] | None):
    """`(ref, payload)` of the wanted RelationDocs with both endpoints in the view."""
    for ref, doc in docs.items():
        if doc["model"] != "RelationDoc" or (wanted is not None and ref not in wanted):
            continue
        rp = doc["payload"]
        if rp.get("source_id") in in_view and rp.get("target_id") in in_view:
            yield ref, rp


def _relation_links(docs: dict, node_refs: list[str], links: tuple, wanted: set[str] | None, notation_ref: str, palette, skipped) -> list:
    """One link per relation doc, ordered by `order` then doc; unmatched relations are skipped."""
    by_relation, wildcard = links
    out: list[dict[str, Any]] = []
    for ref, rp in _relation_docs(docs, set(node_refs), wanted):
        link = by_relation.get(rp.get("relation_type")) or wildcard
        if link is None:
            skipped.append(f"{ref}: relation '{rp.get('relation_type')}' has no link in {notation_ref}")
        else:
            out.append(link_view(rp.get("source_id"), rp.get("target_id"), link, rp, ref, palette))
    return sorted(out, key=lambda l: (l["order"], l["doc"] or ""))


def collect_links(docs: dict, node_refs: list[str], links: list[dict], relation_refs, notation_ref: str, palette) -> tuple[list, list]:
    """`(links, skipped)` of the view: `contains` links first, then relation links."""
    by_relation = {l["payload"]["relation"]: l for l in links if l["payload"]["relation"] != ANY_RELATION}
    wildcard = next((l for l in links if l["payload"]["relation"] == ANY_RELATION), None)
    skipped: list[str] = []
    out = _contains_links(docs, node_refs, by_relation.get("contains"), palette, skipped)
    wanted = set(relation_refs) if relation_refs is not None else None
    out.extend(_relation_links(docs, node_refs, (by_relation, wildcard), wanted, notation_ref, palette, skipped))
    return out, skipped
