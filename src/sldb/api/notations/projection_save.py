"""Save or update a `ViewDoc` in the store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.projection_constants import VIEW_MODEL, VIEWS_DIR
from sldb.api.notations.projection_filters import plan


def _register_model(api: Any, store_path: Path, pythonpath: str | None, actor: str | None) -> None:
    """Make sure the ViewDoc model is registered in the store."""
    try:
        api.load_registered_model(store_path, VIEW_MODEL, pythonpath)
    except Exception:
        api.add_model(store_path, "sldb.models.notation_models:ViewDoc", pythonpath, actor=actor)


def _payload(view: dict[str, Any], name: str) -> dict[str, Any]:
    """The view with `id`, `name` and `title` defaulted to its name."""
    payload = dict(view)
    for key in ("id", "name", "title"):
        payload.setdefault(key, name)
    return payload


def _write(api: Any, store_path: Path, target: Path, name: str, payload: dict[str, Any], pythonpath, actor) -> None:
    """Update the ViewDoc if it exists, create it at `target` otherwise."""
    if api.doc_exists(store_path, f"{VIEW_MODEL}/{name}"):
        api.save_document_payload(store_path, VIEW_MODEL, name, payload, pythonpath=pythonpath, actor=actor)
    else:
        api.create_document(store_path, VIEW_MODEL, target, payload, name=name, pythonpath=pythonpath, actor=actor)


def save_projection_view(
    store: Path | str,
    name: str,
    view: dict[str, Any],
    pythonpath: str | None = None,
    actor: str | None = None,
) -> dict[str, Any]:
    """Save or update a `ViewDoc` in the store."""
    store_path = Path(store)
    import sldb.api as api
    clean_name = name.split(":", 1)[-1]
    _register_model(api, store_path, pythonpath, actor)
    root = Path(api.open_store(store_path).project_root).resolve()
    plan(view)
    payload = _payload(view, clean_name)
    _write(api, store_path, root / VIEWS_DIR / f"{clean_name}.md", clean_name, payload, pythonpath, actor)
    return {"ref": f"{VIEW_MODEL}:{clean_name}", "saved": True}
