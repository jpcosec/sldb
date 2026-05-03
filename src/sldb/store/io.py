from pathlib import Path

import yaml

from sldb.store.models import (
    DocumentsIndex,
    ModelsIndex,
    SemanticDAG,
    SemanticIndex,
    StoreIndex,
)


def load_store_index(store_path: Path) -> StoreIndex:
    index_file = store_path / "store_index.yaml"
    if not index_file.exists():
        raise FileNotFoundError(f"No store_index.yaml at {store_path}")
    data = yaml.safe_load(index_file.read_text(encoding="utf-8")) or {}
    return StoreIndex(**data)


def save_store_index(store_path: Path, index: StoreIndex) -> None:
    store_path.mkdir(parents=True, exist_ok=True)
    (store_path / "store_index.yaml").write_text(
        yaml.safe_dump(index.model_dump(), sort_keys=False),
        encoding="utf-8",
    )


def load_models_index(path: Path) -> ModelsIndex:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return ModelsIndex(**data)


def save_models_index(path: Path, index: ModelsIndex) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(index.model_dump(), sort_keys=False),
        encoding="utf-8",
    )


def load_documents_index(path: Path) -> DocumentsIndex:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return DocumentsIndex(**data)


def save_documents_index(path: Path, index: DocumentsIndex) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(index.model_dump(), sort_keys=False),
        encoding="utf-8",
    )


def load_semantic_dag(store_path: Path) -> SemanticDAG:
    dag_file = store_path / "semantic_dag.yaml"
    if not dag_file.exists():
        return SemanticDAG()
    data = yaml.safe_load(dag_file.read_text(encoding="utf-8")) or {}
    return SemanticDAG(**data)


def save_semantic_dag(store_path: Path, dag: SemanticDAG) -> None:
    store_path.mkdir(parents=True, exist_ok=True)
    (store_path / "semantic_dag.yaml").write_text(
        yaml.safe_dump(dag.model_dump(), sort_keys=False),
        encoding="utf-8",
    )


def load_semantic_index(store_path: Path) -> SemanticIndex:
    index_file = store_path / "semantic_index.yaml"
    if not index_file.exists():
        return SemanticIndex()
    data = yaml.safe_load(index_file.read_text(encoding="utf-8")) or {}
    return SemanticIndex(**data)


def save_semantic_index(store_path: Path, index: SemanticIndex) -> None:
    store_path.mkdir(parents=True, exist_ok=True)
    (store_path / "semantic_index.yaml").write_text(
        yaml.safe_dump(index.model_dump(), sort_keys=False),
        encoding="utf-8",
    )
