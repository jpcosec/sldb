"""Reading one store's documents into corpus entries, and the ranked hits a rank produces."""

from __future__ import annotations

from typing import Any

from sldb.api.corpus.corpus_entry import CorpusEntry
from sldb.api.corpus.hit import Hit
from sldb.api.journal import doc_hashes
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.store.query import load_runtime_documents

LOCAL = "local"


def export_id(store_name: str, model: str, name: str) -> str:
    """`Model:name` for a local document, `store:Model:name` for a linked one."""
    return f"{model}:{name}" if store_name == LOCAL else f"{store_name}:{model}:{name}"


def corpus_entries(corpus) -> list[CorpusEntry]:
    """Every runtime document the corpus's projection admits, as an entry."""
    records = load_runtime_documents(
        corpus.store, resolve_model_ref, corpus.pythonpath, include_linked=True
    )
    return [e for e in (_entry(corpus, r) for r in records) if e is not None]


def _entry(corpus, record: Any) -> CorpusEntry | None:
    model = record.model_name or ""
    store = None if record.store_name == LOCAL else record.store_name
    if not _admits(corpus, model, store):
        return None
    text = corpus.projection.text(record.payload or {})
    if not text:
        return None
    return _build(corpus, record, model, store, text)


def _admits(corpus, model: str, store: str | None) -> bool:
    if not corpus.projection.admits(model):
        return False
    return corpus.projection.stores is None or store in corpus.projection.stores


def _build(corpus, record: Any, model: str, store: str | None, text: str) -> CorpusEntry:
    return CorpusEntry(
        id=export_id(record.store_name, model, record.name),
        model=model,
        name=record.name,
        store=store,
        text=text,
        hash=doc_hashes(record.store_path, model, record.name)[0] or "",
        payload=record.payload or {},
        tags=tuple(record.semantic_tags or ()),
    )


def select_hits(
    ranked: list[tuple[str, float]],
    by_id: dict[str, CorpusEntry],
    allowed: set[str] | None,
    k: int | None,
) -> list[Hit]:
    """The ranked entries still in the corpus (and among the allowed ones), at most k."""
    hits: list[Hit] = []
    for doc_id, score in ranked:
        entry = by_id.get(doc_id)
        if (allowed is not None and doc_id not in allowed) or entry is None:
            continue
        hits.append(Hit.of(entry, score))
        if k is not None and len(hits) >= k:
            break
    return hits
