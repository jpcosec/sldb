"""Where a pointer lands (code-anchoring.md, tags.md): which documents cover a file or a symbol,
and which code a document or a tag covers. Read-only; it composes `CodeAnchorDoc` refs with the
semantic DAG and keeps no index of its own.

A document covers code `directly` when it is the anchor of it, and `tag:<t>` when it carries the
tag `t` (a payload `tags`/`semantic_tags` entry) and some anchor of that code carries `t` or a tag
below it, or one equivalent to either. A tag nobody declared is not an error: it is `unresolved`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.anchors.anchor_docs import MODEL as ANCHOR_MODEL
from sldb.core.exceptions import SLDBStoreError
from sldb.models.code_ref import parse_code_ref
from sldb.api.anchors.tag_reach import tag_reach
from sldb.store.io import load_semantic_dag
from sldb.store.semantic_dag_graph import dag_graph
from sldb.store.semantic_tags import payload_tags


def anchors_resolve(store: str | Path | None, target: str | None = None, document: str | None = None, tag: str | None = None, pythonpath: str | None = None) -> dict[str, Any]:
    """One question, three ways to ask it (exactly one argument).

    `target` (`path` or `path::Symbol`, optionally `code:`-prefixed): `{target, documents:
    [{doc, via}], unresolved}`. `document` (`Model:id`): `{document, code: [{path, symbol, via}],
    unresolved}`. `tag`: `{tag, documents: [{doc, via}], code: [...], unresolved}`: what the tag
    and everything below it reaches. `via` is `direct` or `tag:<tag>`; lists are sorted.

    Raises:
        SLDBStoreError: Not exactly one argument, or `document` is not a document of the store.
    """
    if [target, document, tag].count(None) != 2:
        raise SLDBStoreError("anchors_resolve takes exactly one of target, document, tag.")
    world = _World.load(store, pythonpath)
    if target is not None:
        return {"target": target, "documents": world.covering(*_split(target)), "unresolved": world.unresolved()}
    if document is not None:
        return {"document": document, "code": world.covered_by(document), "unresolved": world.unresolved()}
    return {"tag": tag, **world.tag(str(tag)), "unresolved": world.unresolved(tag)}


def _split(target: str) -> tuple[str, str | None]:
    text = target[len("code:"):] if target.startswith("code:") else target
    path, sep, symbol = text.partition("::")
    return path, (symbol if sep else None)


class _World:
    def __init__(self, docs: list[Any], dag: Any) -> None:
        self.docs, self.dag = docs, dag
        self.known = set(dag_graph(dag).nodes)
        self.anchors = [(f"{d.model_name}:{d.name}", *p, set(payload_tags(d.payload))) for d in docs if d.model_name == ANCHOR_MODEL and (p := parse_code_ref(str(d.payload.get("ref", ""))))]

    @classmethod
    def load(cls, store: str | Path | None, pythonpath: str | None) -> "_World":
        from sldb.api.model_registry.model_reference import resolve_model_ref
        from sldb.api.stores.open_store import open_store
        from sldb.store.query import load_runtime_documents

        path = open_store(store, mode="readonly").store_path
        return cls(load_runtime_documents(path, resolve_model_ref, pythonpath), load_semantic_dag(path))

    def reach(self, tag: str) -> set[str]:
        return tag_reach(self.dag, tag)

    def pointers(self) -> list[tuple[str, str]]:
        """`(doc, tag)` of every document that names a tag, anchors included."""
        return sorted((f"{d.model_name}:{d.name}", t) for d in self.docs for t in set(payload_tags(d.payload)))

    def covering(self, path: str, symbol: str | None) -> list[dict[str, str]]:
        hit = [a for a in self.anchors if a[1] == path and (symbol is None or a[2] == symbol)]
        found = {(a[0], "direct") for a in hit}
        found |= {(doc, f"tag:{t}") for doc, t in self.pointers() if t in self.known and any(a[0] != doc and a[3] & self.reach(t) for a in hit)}
        return [{"doc": doc, "via": via} for doc, via in sorted(found)]

    def covered_by(self, document: str) -> list[dict[str, str]]:
        if not any(f"{d.model_name}:{d.name}" == document for d in self.docs):
            raise SLDBStoreError(f"Unknown document '{document}'.")
        found = {(a[1], a[2], "direct") for a in self.anchors if a[0] == document}
        for doc, t in self.pointers():
            if doc == document and t in self.known:
                found |= self._code_of_tag(t, exclude=document)
        return _code(found)

    def _code_of_tag(self, tag: str, exclude: str | None = None) -> set[tuple[str, str, str]]:
        reach = self.reach(tag)
        return {(a[1], a[2], f"tag:{tag}") for a in self.anchors if a[0] != exclude and a[3] & reach}

    def tag(self, tag: str) -> dict[str, Any]:
        if tag not in self.known:
            return {"documents": [], "code": []}
        reach = self.reach(tag)
        docs = {(doc, f"tag:{t}") for doc, t in self.pointers() if t in reach}
        return {"documents": [{"doc": d, "via": v} for d, v in sorted(docs)], "code": _code(self._code_of_tag(tag))}

    def unresolved(self, only: str | None = None) -> list[dict[str, str]]:
        names = [{"tag": t, "doc": doc} for doc, t in self.pointers() if t not in self.known]
        if only is not None and only not in self.known:
            names.append({"tag": only, "doc": ""})
        return sorted(names, key=lambda n: (n["tag"], n["doc"]))


def _code(found: set[tuple[str, str, str]]) -> list[dict[str, str]]:
    return [{"path": p, "symbol": s, "via": v} for p, s, v in sorted(found)]
