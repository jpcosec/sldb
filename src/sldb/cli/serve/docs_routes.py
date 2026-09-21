"""POST /docs/create|track|untrack: document lifecycle over the native sldb API.

All store logic comes from sldb.api, under the same lock /save uses.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from sldb.api import create_document, serialize_document, track_document_file, untrack_document
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.serve.responses import read_json_body
from sldb.cli.serve.save_plan import ID_PATTERN, bad, default_document_path
from sldb.cli.serve.save_routes import SAVE_LOCK
from sldb.core.exceptions import SLDBError, SLDBValidationError
from sldb.store.query import load_runtime_documents


def dispatch_docs(handler, route, store_path, project_root, pythonpath):
    request = read_json_body(handler)
    with SAVE_LOCK:
        return _ACTION_ROUTES.get(route, lambda *_: ({"ok": False, "error": f"Unknown route: {route}"}, 404))(request, store_path, project_root, pythonpath)


def create_action(request, store_path, project_root, pythonpath):
    name = request.get("name")
    if invalid_name(name) is not None or find_document(store_path, pythonpath, name) is not None:
        return invalid_name(name) or bad(f"Ya existe el documento {name}.", 409)
    target, error = create_probe(request, name, store_path, project_root, pythonpath)
    if error is not None:
        return error
    return run_and_serialize(lambda: create_document(store_path, request.get("model"), target, request.get("payload"), name=name, pythonpath=pythonpath), name, store_path, pythonpath)


def track_action(request, store_path, project_root, pythonpath):
    name = request.get("name")
    invalid = invalid_name(name) if name is not None else None
    if invalid is not None:
        return invalid
    target, doc_name, error = track_probe(request, name, store_path, project_root, pythonpath)
    if error is not None:
        return error
    return run_and_serialize(lambda: track_document_file(store_path, request.get("model"), target, name=doc_name, pythonpath=pythonpath), doc_name, store_path, pythonpath)


def untrack_action(request, store_path, project_root, pythonpath):
    name = request.get("name")
    doc = find_document(store_path, pythonpath, name) if isinstance(name, str) else None
    if doc is None:
        return bad(f"Doc '{name}' not found.", 404)
    response = {"ok": True, "doc": serialize_document(doc)}
    try:
        untrack_document(store_path, name, pythonpath=pythonpath)
    except SLDBError as exc:
        return bad(str(exc), 404)
    return response, 200


def create_probe(request, name, store_path, project_root, pythonpath):
    if not isinstance(request.get("payload"), dict):
        return None, bad(f"Contenido inválido: {name}.", 422)
    target = resolve_path(request.get("path"), request.get("model"), name, store_path, project_root, pythonpath)
    conflict = None if target is not None and not target.exists() else bad(f"El archivo de {name} ya existe; elige otro ID.", 409)
    return target, conflict or registration_error(store_path, request.get("model"), pythonpath)


def track_probe(request, name, store_path, project_root, pythonpath):
    target = resolve_path(request.get("path"), request.get("model"), name, store_path, project_root, pythonpath)
    if not isinstance(request.get("path"), str) or target is None or not target.is_file():
        return None, None, bad(f"El archivo {request.get('path')} no existe.", 404)
    doc_name = name or target.stem
    if find_document(store_path, pythonpath, doc_name) is not None:
        return None, None, bad(f"Ya existe el documento {doc_name}.", 409)
    return target, doc_name, registration_error(store_path, request.get("model"), pythonpath)


def run_and_serialize(operation, name, store_path, pythonpath):
    try:
        operation()
    except (SLDBValidationError, ValidationError) as exc:
        return bad(str(exc), 422)
    except SLDBError as exc:
        return bad(str(exc), 404)
    doc = find_document(store_path, pythonpath, name)
    return {"ok": True, "doc": serialize_document(doc)}, 200


def invalid_name(name):
    if isinstance(name, str) and ID_PATTERN.fullmatch(name):
        return None
    return bad("El ID nuevo solo admite letras, números, guiones y guiones bajos.", 400)


def registration_error(store_path, model, pythonpath):
    try:
        load_registered_model(store_path, model, pythonpath)
    except SLDBError as exc:
        return bad(str(exc), 404)
    return None


def resolve_path(raw, model, name, store_path, root, pythonpath):
    if raw is None:
        docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
        return default_document_path(model, name, docs, root)
    if not isinstance(raw, str):
        return None
    path = Path(raw)
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def find_document(store_path, pythonpath, name):
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    return next((doc for doc in docs if doc.name == name), None)


_ACTION_ROUTES = {"/docs/create": create_action, "/docs/track": track_action, "/docs/untrack": untrack_action}