"""Prevalidation of each batch change: shape, model, payload round-trip, target path."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip

ID_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,159}$")


def bad(message: str, status: int = 400) -> tuple[dict[str, Any], int]:
    return {"ok": False, "error": message}, status


def prevalidate(change: dict[str, Any], name: str, current: dict[str, Any], docs: list[Any], store_path: Path, project_root: Path, pythonpath: str) -> tuple[Path | None, tuple[dict[str, Any], int] | None]:
    action = change.get("action")
    existing = current.get(name)
    if action == "create":
        return create_target(change, name, existing, docs, project_root, store_path, pythonpath)
    if action == "update":
        return update_target(change, name, existing, store_path, pythonpath)
    if action == "delete":
        return delete_target(change, name, existing)
    return None, bad("Operación inválida.")


def create_target(change: dict[str, Any], name: str, existing: Any, docs: list[Any], project_root: Path, store_path: Path, pythonpath: str) -> tuple[Path | None, tuple[dict[str, Any], int] | None]:
    if existing is not None:
        return None, bad(f"Ya existe el documento {name}.", 409)
    if not ID_PATTERN.fullmatch(name):
        return None, bad("El ID nuevo solo admite letras, números, guiones y guiones bajos.")
    error = payload_error(change, name, store_path, pythonpath)
    if error is not None:
        return None, error
    path = default_document_path(change["model"], name, docs, project_root)
    return pointed(path, name)


def pointed(path: Path, name: str) -> tuple[Path | None, tuple[dict[str, Any], int] | None]:
    if path.exists():
        return None, bad(f"El archivo de {name} ya existe; elige otro ID.", 409)
    return path, None


def update_target(change: dict[str, Any], name: str, existing: Any, store_path: Path, pythonpath: str) -> tuple[Path | None, tuple[dict[str, Any], int] | None]:
    if existing is None or existing.payload != change.get("expected"):
        return None, bad(f"{name} cambió en SLDB. Recarga para evitar sobrescribirlo.", 409)
    if change.get("model") != existing.model_name:
        return None, bad("No se puede cambiar la clase de un documento existente.")
    return payload_error(change, name, store_path, pythonpath), None


def delete_target(change: dict[str, Any], name: str, existing: Any) -> tuple[Path | None, tuple[dict[str, Any], int] | None]:
    if existing is None or existing.payload != change.get("expected"):
        return None, bad(f"{name} cambió en SLDB. Recarga para evitar sobrescribirlo.", 409)
    return None, None


def default_document_path(model_name: str, name: str, docs: list[Any], root: Path) -> Path:
    existing = next((d for d in docs if d.model_name == model_name), None)
    directory = root / Path(existing.path).parent if existing is not None else root / model_name
    return directory / f"{name}.md"


def payload_error(change: dict[str, Any], name: str, store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int] | None:
    if not isinstance(change.get("payload"), dict):
        return bad(f"Contenido inválido: {name}.")
    return roundtrip_error(change, name, store_path, pythonpath)


def roundtrip_error(change: dict[str, Any], name: str, store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int] | None:
    try:
        model_type = load_registered_model(store_path, change["model"], pythonpath).model_type
        valid, details = validate_payload(model_type, change["payload"])
        if not valid:
            raise ValueError(str(details))
    except (Exception, SystemExit) as exc:
        return bad(f"{name}: {exc}", 422)
    return None


def validate_payload(model_type: type, payload: dict[str, Any]) -> tuple[bool, Any]:
    return validate_model_input_roundtrip(model_type, render_model_markdown(model_type, payload))