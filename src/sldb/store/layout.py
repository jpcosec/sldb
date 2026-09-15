from __future__ import annotations

from pathlib import Path


def project_root(store_path: Path) -> Path:
    return store_path.resolve().parent


def core_dir(store_path: Path) -> Path:
    return store_path / "core"


def runtime_dir(store_path: Path) -> Path:
    return store_path / "runtime"


def config_dir(store_path: Path) -> Path:
    return store_path / ".config"


def store_index_path(store_path: Path) -> Path:
    return core_dir(store_path) / "store_index.yaml"


def legacy_store_index_path(store_path: Path) -> Path:
    return store_path / "store_index.yaml"


def semantic_index_path(store_path: Path) -> Path:
    return runtime_dir(store_path) / "semantic_index.yaml"


def legacy_semantic_index_path(store_path: Path) -> Path:
    return store_path / "semantic_index.yaml"


def semantic_dag_path(store_path: Path) -> Path:
    return runtime_dir(store_path) / "semantic_dag.yaml"


def legacy_semantic_dag_path(store_path: Path) -> Path:
    return store_path / "semantic_dag.yaml"


def lock_path(store_path: Path) -> Path:
    return runtime_dir(store_path) / "locks" / "store.lock"


def models_index_relpath(model_name: str) -> str:
    return f".sldb/core/models/{model_name}.yaml"


def documents_index_relpath(model_name: str) -> str:
    return f".sldb/core/documents/{model_name}.yaml"


def sections_index_relpath(model_name: str) -> str:
    return f".sldb/runtime/sections/{model_name}.yaml"


def semantic_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's semantic contribution per file (PLAN 15 capa 5): a write touches only
    its own shard, never the whole store's."""
    return runtime_dir(store_path) / "semantic" / model_name


def semantic_shard_path(store_path: Path, model_name: str, doc_name: str) -> Path:
    return semantic_shards_dir(store_path, model_name) / f"{doc_name}.yaml"


def sections_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's sections per file (PLAN 15 capa 5), keyed by the same model name the
    legacy per-model `sections_index_relpath` file used."""
    return runtime_dir(store_path) / "sections" / model_name


def sections_shard_path(store_path: Path, model_name: str, doc_name: str) -> Path:
    return sections_shards_dir(store_path, model_name) / f"{doc_name}.yaml"


def model_name_of_sections_path(path: Path) -> str:
    """The model name a (legacy-shaped, still used as a key) per-model sections path names."""
    return path.stem


def documents_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's index entry per file (PLAN 15 capa 7) — the Merkle tree's own leaf
    level, next to the (now legacy-shaped, still used as a key) per-model documents_index."""
    return core_dir(store_path) / "documents" / model_name


def documents_shard_path(store_path: Path, model_name: str, doc_name: str) -> Path:
    return documents_shards_dir(store_path, model_name) / f"{doc_name}.yaml"


def model_name_of_documents_path(path: Path) -> str:
    """The model name a (legacy-shaped, still used as a key) per-model documents path names."""
    return path.stem


def store_exists(store_path: Path) -> bool:
    return (
        store_index_path(store_path).exists()
        or legacy_store_index_path(store_path).exists()
    )
