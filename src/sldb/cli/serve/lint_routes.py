"""GET /lint: a flat problem list over store integrity, edges and links.

Every problem is ``{kind, severity, doc, detail}`` so a client can paint it as a
decoration next to the document. The checks are the real ones: ``diagnose_store``
(the same info as `sldb stores check`), ``check_edges`` (the same as
`sldb edges check`) and link recovery per tracked document. Nothing is
reimplemented here.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api import check_edges
from sldb.cli.model_utils import resolve_model_ref
from sldb.links.recovery import recover_links
from sldb.store.diagnostics import diagnose_store
from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote
from sldb.store.io import load_documents_index, load_models_index, load_store_index

JsonDict = dict[str, Any]


def dispatch_lint(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    problems = _store_problems(store_path, project_root, pythonpath)
    problems += _edge_problems(store_path)
    problems += _link_problems(store_path, project_root)
    return {"problems": problems, "count": len(problems)}, 200


def _store_problems(store_path: Path, root: Path, pythonpath: str) -> list[JsonDict]:
    diagnosis = diagnose_store(store_path, resolve_model_ref, root, pythonpath)
    problems = []
    if not diagnosis.root_ok:
        problems.append(_problem("store", "error", None, "Store index (raiz, hash_a) desactualizado."))
    for model in diagnosis.models:
        if not model.roster_ok:
            problems.append(_problem("store", "error", None, f"Index del modelo '{model.name}' (roster, hash_b): {model.explain()}"))
        for doc in model.documents:
            problems += _document_problems(model.name, doc)
    return problems


def _document_problems(model_name: str, doc: Any) -> list[JsonDict]:
    if not doc.path_exists:
        return [_problem("store", "warning", doc.name, f"{model_name}:{doc.name} no existe en disco ({doc.path}).")]
    if doc.note is DiagnosisNote.DATA_MUTATION:
        return [_problem("store", "error", doc.name, f"{model_name}:{doc.name} cambiaron los campos (hash_d) bajo el contrato del modelo.")]
    if doc.note is DiagnosisNote.BENIGN_MUTATION:
        return [_problem("store", "warning", doc.name, f"{model_name}:{doc.name} mutacion esperable: cambio el texto (hash_c), los campos (hash_d) no.")]
    return []


def _edge_problems(store_path: Path) -> list[JsonDict]:
    report = check_edges(store_path, include_linked=False)
    problems = [_problem("edge", "error", None, message) for message in report.errors]
    problems += [_problem("edge", "warning", stale, f"Shard de aristas desactualizado para '{stale}'.") for stale in report.stale]
    return problems


def _link_problems(store_path: Path, root: Path) -> list[JsonDict]:
    problems = []
    for name, path in _tracked_documents(store_path, root):
        if not path.exists():
            continue
        unresolved = recover_links(path, store_path, depth=1).get("unresolved", [])
        problems += [_problem("link", "warning", name, f"Enlace [[{target}]] no resuelve.") for target in unresolved]
    return problems


def _tracked_documents(store_path: Path, root: Path) -> list[tuple[str, Path]]:
    index = load_store_index(store_path)
    docs = []
    for model in index.models:
        m_idx = load_models_index(root / model.models_index)
        d_idx = load_documents_index(root / m_idx.documents_index)
        docs += [(d.name, (root / d.path).resolve()) for d in d_idx.documents]
    return docs


def _problem(kind: str, severity: str, doc: str | None, detail: str) -> JsonDict:
    return {"kind": kind, "severity": severity, "doc": doc, "detail": detail}