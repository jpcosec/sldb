"""Prepare documentation while preserving the author's semantic explanations."""
from __future__ import annotations

import re
from pathlib import Path
from sldb.models.knowledge_surface import CliCommandDoc, SurfaceDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown
from .command import CommandRecord
from .planned_document import PlannedDocument
from .projection import command_fields, surface_fields


def plan_documents(records: list[CommandRecord], system: str, factory: str, output: Path) -> list[PlannedDocument]:
    """Prepare every file before sync writes any of them."""
    if not re.fullmatch(r"[a-z][a-z0-9_-]*", system):
        raise ValueError("system must be a lowercase identifier without path separators")
    plans = []
    for record in records:
        if not record.group:
            plans.append(_command(record, system, factory, output))
        if len(record.path) == 1:
            plans.append(_surface(record, records, system, factory, output))
    _validate_destinations(plans, output)
    return plans


def _command(record, system, factory, output):
    fields = command_fields(record, system, factory)
    return _prepare(CliCommandDoc, output / "commands" / (fields["id"] + ".md"), fields,
                    {"purpose": "Not documented.", "how_it_works": "Not documented.", "usage": record.usage})


def _surface(record, records, system, factory, output):
    fields = surface_fields(record, records, system, factory)
    return _prepare(SurfaceDoc, output / "surfaces" / (fields["id"] + ".md"), fields,
                    {"purpose": "Not documented.", "how_it_works": "Not documented."})


def _prepare(model, path, fields, defaults):
    path = path.resolve()
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    existing = extract_model_data(model, previous) if previous is not None else defaults
    payload = model.model_validate({**existing, **fields})
    rendered = render_model_markdown(model, payload.model_dump(mode="json")) + "\n"
    if extract_model_data(model, rendered) != payload.model_dump(mode="json"):
        raise ValueError(f"Documentation roundtrip failed: {path}")
    changed = previous is None or any(existing.get(k) != v for k, v in fields.items())
    return PlannedDocument(path=path, payload=payload, markdown=rendered, previous=previous, changed=changed)


def _validate_destinations(plans, output):
    paths = [plan.path for plan in plans]
    if len(set(paths)) != len(paths):
        raise ValueError("Command names collide when converted to document IDs")
    if any(not path.is_relative_to(output.resolve()) for path in paths):
        raise ValueError("A documentation destination escapes the output directory")
