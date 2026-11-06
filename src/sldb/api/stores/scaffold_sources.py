"""The bytes a seed's source stands for: `text` encoded, a `file` template read from the template
root or from a package (`pkg:module/path`, `importlib.resources`), or a `document` rendered
through its model. `managed` seeds compare these bytes with the file's."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Any

from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.stores.seed import Seed
from sldb.core.exceptions import SLDBStoreError

PACKAGE_PREFIX = "pkg:"


def seed_bytes(seed: Seed, store_path: Path, root: Path, template_root: Path) -> bytes:
    """What the seed's file must hold."""
    if seed.text is not None:
        return seed.text.encode("utf-8")
    if seed.file is not None:
        return template_bytes(seed.file, template_root)
    return document_bytes(seed.document, store_path, root)


def template_bytes(source: str, template_root: Path) -> bytes:
    """A `pkg:module/path` resource, or a path relative to the template root."""
    if source.startswith(PACKAGE_PREFIX):
        return _package_bytes(source[len(PACKAGE_PREFIX):])
    path = Path(source) if Path(source).is_absolute() else template_root / source
    if not path.is_file():
        raise SLDBStoreError(f"seed template {source!r} not found at {path}")
    return path.read_bytes()


def _package_bytes(reference: str) -> bytes:
    module, _, relative = reference.partition("/")
    try:
        resource = resources.files(module).joinpath(relative)
        return resource.read_bytes()
    except (ModuleNotFoundError, FileNotFoundError, IsADirectoryError, TypeError) as exc:
        raise SLDBStoreError(f"seed template pkg:{reference} cannot be read: {exc}") from exc


def document_bytes(document: dict[str, Any], store_path: Path, root: Path) -> bytes:
    """The document's payload rendered through its registered model, in UTF-8."""
    from sldb.runtime.validation import render_model_markdown

    model_type = load_registered_model(store_path, document["model"], str(root)).model_type
    return render_model_markdown(model_type, document["payload"], root).encode("utf-8")
