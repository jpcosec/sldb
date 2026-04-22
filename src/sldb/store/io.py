from pathlib import Path

import yaml

from sldb.store.models import StoreIndex, ModelsIndex, DocumentsIndex


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
