"""Prevalidation of each batch change for the HTTP contract: shape, ids, stale `expected`,
target path. The model checks (round-trip, guards by source hash, free targets) are
`sldb.api.apply_batch`'s own prevalidation; `save_routes` maps its errors to 409/422."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

ID_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,159}$")
_TRACKED_ACTIONS = ("update", "delete", "move", "untrack")


def bad(message: str, status: int = 400) -> tuple[dict[str, Any], int]:
    return {"ok": False, "error": message}, status


def prevalidate(change: dict[str, Any], name: str, current: dict[str, Any], docs: list[Any], store_path: Path, project_root: Path, pythonpath: str) -> tuple[Path | None, tuple[dict[str, Any], int] | None]:
    action = change.get("action")
    existing = current.get(name)
    if action == "create":
        return create_target(change, name, existing, docs, project_root)
    if action == "track":
        return None, track_error(change, name, existing, project_root)
    if action in _TRACKED_ACTIONS:
        return None, tracked_error(change, name, action, existing)
    return None, bad("Operación inválida.")


def create_target(change: dict[str, Any], name: str, existing: Any, docs: list[Any], project_root: Path) -> tuple[Path | None, tuple[dict[str, Any], int] | None]:
    if existing is not None:
        return None, bad(f"Ya existe el documento {name}.", 409)
    if not ID_PATTERN.fullmatch(name):
        return None, bad("El ID nuevo solo admite letras, números, guiones y guiones bajos.")
    error = payload_error(change, name)
    if error is not None:
        return None, error
    return pointed(default_document_path(change["model"], name, docs, project_root), name)


def pointed(path: Path, name: str) -> tuple[Path | None, tuple[dict[str, Any], int] | None]:
    if path.exists():
        return None, bad(f"El archivo de {name} ya existe; elige otro ID.", 409)
    return path, None


def track_error(change: dict[str, Any], name: str, existing: Any, project_root: Path) -> tuple[dict[str, Any], int] | None:
    if existing is not None:
        return bad(f"Ya existe el documento {name}.", 409)
    if not isinstance(change.get("path"), str):
        return bad(f"Ruta inválida: {name}.")
    if not (project_root / change["path"]).is_file():
        return bad(f"No existe el archivo {change['path']}.", 404)
    return None


def tracked_error(change: dict[str, Any], name: str, action: str, existing: Any) -> tuple[dict[str, Any], int] | None:
    if existing is None or stale(change, action, existing):
        return bad(f"{name} cambió en SLDB. Recarga para evitar sobrescribirlo.", 409)
    if action == "update" and change.get("model") != existing.model_name:
        return bad("No se puede cambiar la clase de un documento existente.")
    if action == "update":
        return payload_error(change, name)
    if action == "move" and not isinstance(change.get("path"), str):
        return bad(f"Ruta inválida: {name}.")
    return None


def stale(change: dict[str, Any], action: str, existing: Any) -> bool:
    """`expected` (when sent) must match the current payload; an update or delete needs some
    guard, `expected` or `expected_source_hash` (the latter is checked by `apply_batch`)."""
    if "expected" in change:
        return existing.payload != change["expected"]
    return action in ("update", "delete") and "expected_source_hash" not in change


def default_document_path(model_name: str, name: str, docs: list[Any], root: Path) -> Path:
    existing = next((d for d in docs if d.model_name == model_name), None)
    directory = root / Path(existing.path).parent if existing is not None else root / model_name
    return directory / f"{name}.md"


def payload_error(change: dict[str, Any], name: str) -> tuple[dict[str, Any], int] | None:
    if not isinstance(change.get("payload"), dict):
        return bad(f"Contenido inválido: {name}.")
    return None
