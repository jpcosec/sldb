"""Materialize static Python facts into authored, tracked documentation."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from sldb.models.knowledge_surface import PythonSymbolDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown

from .planned_document import PlannedDocument
from .python_symbol import PythonSymbol


def plan_python_documents(records: list[PythonSymbol], system: str, output: Path, architecture_spec: Path | None = None) -> list[PlannedDocument]:
    _validate_system(system)
    spec = _architecture_spec(architecture_spec, output.parent)
    plans = [_plan(record, system, output, spec) for record in records]
    _validate_paths(plans, output)
    return plans


def _validate_system(system: str) -> None:
    if not re.fullmatch(r"[a-z][a-z0-9_-]*", system):
        raise ValueError("system must be a lowercase identifier without path separators")


def _plan(record: PythonSymbol, system: str, output: Path, spec: str) -> PlannedDocument:
    fields = _fields(record, system, spec)
    path = (output / "symbols" / f"{fields['id']}.md").resolve()
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    existing = extract_model_data(PythonSymbolDoc, previous) if previous else _defaults(record)
    payload = PythonSymbolDoc.model_validate({**existing, **fields})
    return _planned(path, previous, existing, fields, payload)


def _fields(record: PythonSymbol, system: str, spec: str) -> dict:
    digest = hashlib.sha256(json.dumps(record.model_dump(), sort_keys=True).encode()).hexdigest()
    safe = re.sub(r"[^a-z0-9_]+", "-", f"{record.module}-{record.qualname}".lower()).strip("-")
    return {"id": f"python-{system}-{safe}", "system": system, "module": record.module,
            "qualname": record.qualname, "kind": record.kind, "source_path": record.path,
            "source_span": f"{record.line_start}:{record.line_end}", "source_sha256": record.source_sha256,
            "signature": record.signature or "Not applicable.", "docstring": record.docstring or "Not documented.",
            "imports": json.dumps(record.imports), "architecture_spec": spec,
            "provenance": f"python-ast:{record.id}; contract-sha256:{digest}"}


def _architecture_spec(path: Path | None, root: Path) -> str:
    if path is None:
        return "Not declared."
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        raise ValueError("Architecture spec must be an existing file within the project")
    return f"{resolved.relative_to(root)}; sha256={hashlib.sha256(resolved.read_bytes()).hexdigest()}"


def _defaults(record: PythonSymbol) -> dict:
    return {"purpose": "Not documented.", "architecture": "Not documented.", "tags": []}


def _planned(path, previous, existing, fields, payload) -> PlannedDocument:
    markdown = render_model_markdown(PythonSymbolDoc, payload.model_dump(mode="json")) + "\n"
    if extract_model_data(PythonSymbolDoc, markdown) != payload.model_dump(mode="json"):
        raise ValueError(f"Documentation roundtrip failed: {path}")
    return PlannedDocument(path=path, payload=payload, markdown=markdown, previous=previous,
                           changed=previous is None or any(existing.get(key) != value for key, value in fields.items()))


def _validate_paths(plans: list[PlannedDocument], output: Path) -> None:
    if len({plan.path for plan in plans}) != len(plans):
        raise ValueError("Python symbols collide when converted to document IDs")
    if any(not plan.path.is_relative_to(output.resolve()) for plan in plans):
        raise ValueError("A documentation destination escapes the output directory")
