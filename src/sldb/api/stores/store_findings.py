"""A store diagnosis as findings: what is broken (error) apart from what moved (alert).

The owner's rule (docs/architecture/anchoring.md, §4): a stale root or roster, a moved
contract and a changed document are the source moving against the index, alerts; a tracked
file that is gone and a model that does not import are errors. A reformatted document is
neither: its fields held still, and the summary counts it.
"""

from __future__ import annotations

from typing import Any

from sldb.core.finding import Finding, alert, error
from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote

_UPDATE = "sldb stores update"
_DOC_CODES = {DiagnosisNote.DATA_MUTATION: "store/data-mutation", DiagnosisNote.CONTRACT_MUTATION: "store/contract-mutation"}


def diagnosis_findings(diagnosis: Any) -> list[Finding]:
    """Every finding of one diagnosis: the root, then each model and its documents."""
    root = [] if diagnosis.root_ok else [alert("store/root-stale", "store_hash", "a model node moved, or the set of models changed", _UPDATE)]
    return root + [f for model in diagnosis.models for f in _model_findings(model)]


def _model_findings(model: Any) -> list[Finding]:
    found = [] if model.resolved else [_unresolved(model)]
    if not model.contract_ok:
        found.append(alert("store/contract-moved", model.name, model.explain(), _UPDATE))
    elif not model.roster_ok:
        found.append(alert("store/roster-stale", model.name, model.explain(), _UPDATE))
    elif model.legacy_contract:
        found.append(alert("store/legacy-contract", model.name, model.explain(), _UPDATE))
    return found + [f for doc in model.documents if (f := _document_finding(model.name, doc))]


def _unresolved(model: Any) -> Finding:
    fix = "make the model importable (install its package, or pass --pythonpath)"
    removable = "" if model.documents else f"; with no documents left, `sldb models remove {model.name}` unregisters it"
    return error("store/model-unresolved", model.name, "the model's class cannot be imported here, so its fields were not re-extracted", fix + removable)


def _document_finding(model: str, doc: Any) -> Finding | None:
    subject = f"{model}:{doc.name}"
    if doc.note is DiagnosisNote.MISSING:
        return error("store/missing", subject, doc.explain(), doc.remedy(), doc.name)
    code = _DOC_CODES.get(doc.note)
    return alert(code, subject, doc.explain(), doc.remedy(), doc.name) if code else None
