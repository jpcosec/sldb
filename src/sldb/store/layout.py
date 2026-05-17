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


def store_exists(store_path: Path) -> bool:
    return (
        store_index_path(store_path).exists()
        or legacy_store_index_path(store_path).exists()
    )
