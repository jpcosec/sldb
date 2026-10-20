"""Findings read through the store's policy (docs/architecture/provenance.md §5).

Every builder proposes a level; the policy decides it, from the document's authority (its
block, else its model's `__authority__`), whether that authority was declared, and whether the
model is narrative. `ignore` and `allow` drop the finding; `reindex` and `hook:` keep it as an
alert naming what `stores check --apply` would run.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from sldb.api.stores.policy import LEVELS, Policy, Subject
from sldb.core.finding import Finding


def judged(findings: list[Finding], store_path: Path, pythonpath: str | None) -> list[Finding]:
    policy, subjects = Policy.of_store(store_path), SubjectIndex(store_path, pythonpath)
    kept = []
    for finding in findings:
        model, doc = split_subject(finding.subject)
        response = policy.response(finding.code, model, subjects.subject(model, doc))
        level = "alert" if response.startswith("hook:") else LEVELS.get(response, "alert")
        if level:
            kept.append(replace(finding, level=level, fix=_fix(finding, response)))
    return kept


def split_subject(subject: str) -> tuple[str | None, str | None]:
    """`Model:doc` -> (Model, doc); `Model` -> (Model, None); anything else -> (None, None)."""
    model, sep, doc = subject.partition(":")
    return (model, doc or None) if model and " " not in model and "/" not in model else (None, None)


def _fix(finding: Finding, response: str) -> str:
    if response == "reindex" or response.startswith("hook:"):
        return f"policy: {response}   (sldb stores check --apply runs it)"
    return finding.fix


class SubjectIndex:
    """Per model: its class authority and narrativity; per document: its indexed block."""

    def __init__(self, store_path: Path, pythonpath: str | None) -> None:
        self.store_path, self.pythonpath = store_path, pythonpath
        self._models: dict[str, tuple[str, bool, bool]] = {}

    def subject(self, model: str | None, doc: str | None) -> Subject:
        if model is None:
            return Subject()
        authority, declared, narrative = self._model(model)
        block = self._block(model, doc) if doc else None
        if block:
            return Subject(authority=block.get("authority", authority), declared=True, by=str(block.get("by", "agent")), narrative=narrative)
        return Subject(authority=authority, declared=declared, narrative=narrative)

    def _model(self, model: str) -> tuple[str, bool, bool]:
        if model not in self._models:
            self._models[model] = _model_facts(self.store_path, model, self.pythonpath)
        return self._models[model]

    def _block(self, model: str, doc: str) -> dict[str, Any] | None:
        from sldb.store import documents_hash

        try:
            return next((e.provenance for e in documents_hash.entries_of(self.store_path, model) if e.name == doc), None)
        except Exception:  # noqa: BLE001 - a model with no shards yet has no blocks
            return None


def _model_facts(store_path: Path, model: str, pythonpath: str | None) -> tuple[str, bool, bool]:
    """`(authority, declared, narrative)` of a registered model; defaults when it does not import."""
    from sldb.api.documents.structural_noise import declared_headings
    from sldb.models.provenance import Provenance

    model_type = _model_type(store_path, model, pythonpath)
    if model_type is None:
        return "generated", False, False
    authority, declared = Provenance.of_model(model_type)
    return authority, declared, not declared_headings(getattr(model_type, "__template__", "") or "")[0]


def _model_type(store_path: Path, model: str, pythonpath: str | None) -> type | None:
    from sldb.api.model_registry.model_reference import resolve_model_ref
    from sldb.store.io import load_store_index

    entry = next((m for m in load_store_index(store_path).models if m.name == model), None)
    try:
        return resolve_model_ref(entry.model_ref, pythonpath) if entry else None
    except Exception:  # noqa: BLE001 - an unimportable model is its own finding
        return None
