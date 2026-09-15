"""Compare parser-derived documents with their files and store registrations."""
from __future__ import annotations

from pathlib import Path
from sldb.selfdoc.planned_document import PlannedDocument
from sldb.selfdoc.report import DocumentationReport
from sldb.models.knowledge_surface import PythonSymbolDoc
from sldb.runtime.validation import extract_model_data
from .selfdoc_registry import DocumentationRegistry


def inspect_documents(plans: list[PlannedDocument], store: Path, root: Path, output: Path, system: str) -> DocumentationReport:
    """Report drift without writing files, caches, indexes, or migrations."""
    report = DocumentationReport(documents=len(plans))
    registry = DocumentationRegistry(store, root)
    for plan in plans:
        _inspect_plan(plan, registry, root, report)
    report.removed = removed_documents(plans, output, root, system, registry)
    report.renamed = rename_candidates(plans, report.removed, root)
    report.semantic_gaps = semantic_gap_count(plans)
    return report


def _inspect_plan(plan, registry, root, report) -> None:
    path = str(plan.path.relative_to(root))
    if plan.previous is None:
        report.missing.append(path)
    elif plan.changed:
        report.changed.append(path)
    if status := registry.status(plan):
        getattr(report, status).append(path)


def removed_documents(plans, output: Path, root: Path, system: str, registry) -> list[str]:
    """Find obsolete records without deleting or untracking them."""
    expected = {plan.path for plan in plans}
    models = {plan.model_name for plan in plans} or {"CliCommandDoc", "SurfaceDoc"}
    existing = _managed_files(output, system, models)
    existing.extend(registry.managed_paths(output, system, models))
    return sorted({str(path.relative_to(root)) for path in existing if path.resolve() not in expected})


def _managed_files(output: Path, system: str, models: set[str]) -> list[Path]:
    patterns = {"CliCommandDoc": ("commands", "cmd"), "SurfaceDoc": ("surfaces", "surface"),
                "PythonSymbolDoc": ("symbols", "python")}
    return [path for name, (folder, prefix) in patterns.items() if name in models
            for path in (output / folder).glob(f"{prefix}-{system}-*.md")]


def rename_candidates(plans, removed: list[str], root: Path) -> list[dict[str, str]]:
    """Report heuristic Python fact matches without guaranteeing uniqueness."""
    new = _new_symbol_ids(plans)
    candidates = [_rename_candidate(root / path, new) for path in removed if path.startswith("knowledge/symbols/")]
    return [candidate for candidate in candidates if candidate is not None]


def _new_symbol_ids(plans) -> dict[tuple, list[str]]:
    ids: dict[tuple, list[str]] = {}
    for plan in plans:
        if isinstance(plan.payload, PythonSymbolDoc):
            ids.setdefault(_symbol_key(plan.payload), []).append(plan.payload.id)
    return ids


def _rename_candidate(path: Path, new: dict[tuple, list[str]]) -> dict[str, str] | None:
    if not path.exists():
        return None
    old = extract_model_data(PythonSymbolDoc, path.read_text(encoding="utf-8"))
    targets = new.get(_symbol_key(PythonSymbolDoc.model_validate(old)), [])
    return {"from": old["id"], "to": targets[0]} if len(targets) == 1 and targets[0] != old["id"] else None


def _symbol_key(payload: PythonSymbolDoc) -> tuple:
    return (payload.source_sha256, payload.kind, payload.signature, payload.docstring)


def semantic_gap_count(plans) -> int:
    """Count authored semantic fields intentionally left for review."""
    return sum(_has_semantic_gap(plan.payload) for plan in plans if isinstance(plan.payload, PythonSymbolDoc))


def _has_semantic_gap(payload: PythonSymbolDoc) -> bool:
    return payload.purpose == "Not documented." or payload.architecture == "Not documented."
