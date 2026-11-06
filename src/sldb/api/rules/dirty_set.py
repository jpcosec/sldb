"""The dirty set of the rules cache (GO08, rules.md §9): `<.sldb_cache>/rules/dirty.json`.

Writing a document D adds D and every document with an edge to or from D in the index (one
hop: anchors and one-step paths). `rules_on_check` recomputes those, empties the set and keeps
the rest from the cache. A rule whose paths go further (a closure `+`, several steps, a nested
quantifier) is wide: any dirty document recomputes its whole family. An absent file means
everything is dirty. Each cached result also keeps a stamp of what it read (the document and its
neighbours, or the whole store for a wide rule), so a change made outside a write (a file edited
and rebuilt, a document created or deleted) recomputes too: the cache is never authority.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from sldb.api.rules.rule_cache import DIRTY, read_json, rules_dir, write_json
from sldb.store.edge_index.node_ids import bare, kind
from sldb.store.graph.language.predicate_ast import children
from sldb.store.graph.language.predicate_parser import parse_predicate
from sldb.store.io import store_lock


def read_dirty(store_path: Path) -> set[str] | None:
    """The dirty documents; None when the file is absent or unreadable (all are dirty)."""
    data = read_json(rules_dir(store_path) / f"{DIRTY}.json")
    return set(data["dirty"]) if data is not None and isinstance(data.get("dirty"), list) else None


def write_dirty(store_path: Path, dirty: set[str]) -> None:
    write_json(rules_dir(store_path) / f"{DIRTY}.json", {"dirty": sorted(dirty)})


def mark_dirty(store_path: Path, index: Any, node: str) -> None:
    """Add `node` and its neighbours, under the store lock; an absent set stays absent (all dirty)."""
    with store_lock(store_path, wait=True):
        dirty = read_dirty(store_path)
        if dirty is not None:
            write_dirty(store_path, dirty | {node} | neighbours(index, node))


def neighbours(index: Any, node: str) -> set[str]:
    edges = index.edges_from(node) + index.edges_to(node)
    return {bare(i) for e in edges for i in (e.source, e.target) if kind(i) == "document"} - {node}


def stamps_of(graph: Any, rule: dict[str, Any], family: list[str]) -> dict[str, str]:
    """What each result of `rule` reads: the document and its neighbours, or the whole store."""
    if wide(rule):
        whole = _digest([_state(graph, n) for n in sorted(graph.index_documents)])
        return {node: whole for node in family}
    return {node: _digest([_state(graph, n) for n in sorted({node} | neighbours(graph.index, node))]) for node in family}


def wide(rule: dict[str, Any]) -> bool:
    """Whether the rule reads further than one step from its subject."""
    texts = [rule.get("condition") or "", rule.get("where") or ""]
    return any(_wide(parse_predicate(t).root, False) for t in texts if t.strip())


def _wide(node: tuple, inside: bool) -> bool:
    if node[0] in ("quant", "count"):
        path = node[3] if node[0] == "quant" else node[2]
        if inside or len(path) > 1 or any(step[3] for step in path):
            return True
        inside = True
    return any(_wide(child, inside) for child in children(node))


def _state(graph: Any, node: str) -> list[Any]:
    record = graph.index.node(node)
    return [node, record.source_hash, record.payload] if record is not None else [node]


def _digest(states: list[Any]) -> str:
    return hashlib.sha256(json.dumps(states, sort_keys=True, default=str).encode()).hexdigest()
