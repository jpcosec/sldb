"""`.sldb/` (`store.yaml`, `core/`: versioned whole, git holds its past) and its sibling `.sldb_cache/`
(the derived shards: regenerable, ignored; `.sldb/runtime/` until 2026-11-04). docs/architecture/derived-store-boundary.md."""

from __future__ import annotations

from pathlib import Path

CACHE_DIR_NAME = ".sldb_cache"


def project_root(store_path: Path) -> Path:
    return store_path.resolve().parent


def core_dir(store_path: Path) -> Path:
    return store_path / "core"


def cache_dir(store_path: Path) -> Path:
    """`.sldb_cache/` beside the store directory, whatever that one is named (`kb/.sldb_custom` -> `kb/.sldb_cache`)."""
    return store_path.parent / CACHE_DIR_NAME


def runtime_dir(store_path: Path) -> Path:  # the cache, under the name every derived-index writer uses
    return cache_dir(store_path)


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


def _index_relpath(store_path: Path, *parts: str) -> str:
    """A store index's path relative to the project root, from the store's real directory name:
    a store named `.sldb_custom` records `.sldb_custom/core/...`, not a phantom `.sldb/core/...`."""
    root = project_root(store_path).resolve()
    return str((store_path.resolve() / Path(*parts)).relative_to(root))


def models_index_relpath(store_path: Path, model_name: str) -> str:
    return _index_relpath(store_path, "core", "models", f"{model_name}.yaml")


def documents_index_relpath(store_path: Path, model_name: str) -> str:
    return _index_relpath(store_path, "core", "documents", f"{model_name}.yaml")


def sections_index_relpath(store_path: Path, model_name: str) -> str:
    """A key, not a file: the shards live in `.sldb_cache/`, but the models index still records
    this legacy-shaped path and `SectionsIndexIO` reads the store and model name out of it."""
    return _index_relpath(store_path, "runtime", "sections", f"{model_name}.yaml")


def semantic_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's semantic contribution per file (PLAN 15 capa 5): a write touches only its own shard."""
    return runtime_dir(store_path) / "semantic" / model_name


def semantic_shard_path(store_path: Path, model_name: str, doc_name: str) -> Path:
    return semantic_shards_dir(store_path, model_name) / f"{doc_name}.yaml"


def sections_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's sections per file (PLAN 15 capa 5), keyed by the model name `sections_index_relpath` names."""
    return runtime_dir(store_path) / "sections" / model_name


def sections_shard_path(store_path: Path, model_name: str, doc_name: str) -> Path:
    return sections_shards_dir(store_path, model_name) / f"{doc_name}.yaml"


def edges_store_shard_path(store_path: Path) -> Path:
    """The store's own contribution to the edge index (store node, semantic DAG edges)."""
    return runtime_dir(store_path) / "edges.yaml"


def edges_shards_root(store_path: Path) -> Path:
    return runtime_dir(store_path) / "edges"


def edges_model_shard_path(store_path: Path, model_name: str) -> Path:
    """One model's contribution (model node, fields, extends), next to its documents' dir."""
    return edges_shards_root(store_path) / f"{model_name}.yaml"


def edges_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's edges per file, the same per-document pattern as sections."""
    return edges_shards_root(store_path) / model_name


def edges_shard_path(store_path: Path, model_name: str, doc_name: str) -> Path:
    return edges_shards_dir(store_path, model_name) / f"{doc_name}.yaml"


def model_name_of_sections_path(path: Path) -> str:
    """The model name a (legacy-shaped, still used as a key) per-model sections path names."""
    return path.stem


def documents_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's index entry per file (PLAN 15 capa 7): the Merkle tree's own leaf level."""
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
