"""The store-wide (semantic) or per-model (sections) aggregate, composed from shards (PLAN
15 capa 5) — the same shapes `SemanticIndex.documents`/`SectionsIndex.documents` always had,
assembled by reading every shard instead of one file for the whole store or model."""

from __future__ import annotations

from pathlib import Path

from sldb.store.io.shards import list_shard_names, load_document_shard, load_edges_shard, load_semantic_shard, load_sections_shard
from sldb.store.models import DocEdges, DocSections, DocumentEntry, SemanticDocumentRecord


def compose_semantic_documents(store_path) -> dict[str, SemanticDocumentRecord]:
    from sldb.store.layout import runtime_dir

    root = runtime_dir(Path(store_path)) / "semantic"
    out: dict[str, SemanticDocumentRecord] = {}
    for model_dir in sorted(p for p in root.iterdir() if p.is_dir()) if root.is_dir() else []:
        _add_model_shards(model_dir, out)
    return out


def _add_model_shards(model_dir: Path, out: dict[str, SemanticDocumentRecord]) -> None:
    for shard_path in sorted(model_dir.glob("*.yaml")):
        rec = load_semantic_shard(shard_path)
        if rec is not None:
            out[shard_path.stem] = rec


def compose_sections_documents(store_path, model_name: str) -> list[DocSections]:
    from sldb.store.layout import sections_shards_dir

    shards_dir = sections_shards_dir(Path(store_path), model_name)
    out: list[DocSections] = []
    for name in list_shard_names(shards_dir):
        sec = load_sections_shard(shards_dir / f"{name}.yaml")
        if sec is not None:
            out.append(sec)
    return out


def compose_edges_documents(store_path, model_name: str) -> list[DocEdges]:
    """Every edges shard of one model's documents, by name (the model's own shard and the
    store's are single files: `layout.edges_model_shard_path` / `edges_store_shard_path`)."""
    from sldb.store.layout import edges_shards_dir

    shards_dir = edges_shards_dir(Path(store_path), model_name)
    shards = (load_edges_shard(shards_dir / f"{name}.yaml", DocEdges) for name in list_shard_names(shards_dir))
    return [shard for shard in shards if shard is not None]


def compose_documents_entries(store_path, model_name: str) -> list[DocumentEntry]:
    """Every document shard of one model, by name — the same shape a per-model
    DocumentsIndex.documents list always had (PLAN 15 capa 7)."""
    from sldb.store.layout import documents_shards_dir

    shards_dir = documents_shards_dir(Path(store_path), model_name)
    out: list[DocumentEntry] = []
    for name in list_shard_names(shards_dir):
        entry = load_document_shard(shards_dir / f"{name}.yaml")
        if entry is not None:
            out.append(entry)
    return out
