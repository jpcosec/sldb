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
from sldb.links.audit import audit_links
from sldb.links.tracked import tracked_documents
from sldb.store.diagnostics import diagnose_store

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
    """Every finding of `stores check`, an error as `error` and an alert as `warning`
    (anchoring.md §4), plus each reformatted document as a `warning`."""
    from sldb.api.stores.store_check import all_findings

    diagnosis = diagnose_store(store_path, resolve_model_ref, root, pythonpath)
    problems = [_problem("store", "error" if f.level == "error" else "warning", f.document, f"{f.subject}: {f.what}") for f in all_findings(diagnosis, store_path, root, pythonpath)]
    return problems + [_reformatted(m, d) for m, d in diagnosis.reformatted_documents]


def _reformatted(model_name: str, doc: Any) -> JsonDict:
    return _problem("store", "warning", doc.name, f"{model_name}:{doc.name} mutacion esperable: cambio el texto (hash_c), los campos (hash_d) no.")


def _edge_problems(store_path: Path) -> list[JsonDict]:
    report = check_edges(store_path, include_linked=False)
    problems = [_problem("edge", "error", None, message) for message in report.errors]
    problems += [_problem("edge", "warning", stale, f"Shard de aristas desactualizado para '{stale}'.") for stale in report.stale]
    return problems


def _link_problems(store_path: Path, root: Path) -> list[JsonDict]:
    found = audit_links(store_path, tracked_documents(store_path, root))
    return [_problem("link", "warning", p["doc"], f"Enlace [[{p['target']}]] no resuelve.") for p in found if p["kind"] == "unresolved"]


def _problem(kind: str, severity: str, doc: str | None, detail: str) -> JsonDict:
    return {"kind": kind, "severity": severity, "doc": doc, "detail": detail}