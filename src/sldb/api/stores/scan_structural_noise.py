"""Report the already-tracked documents whose headings their model never declares.

Diagnosis, not enforcement: `docs track` and `docs create` refuse new noise, while
this lists the documents that entered the store before the refusal existed. Every
document is reported, never skipped: a scan that quietly drops what it cannot read
is the same silent degradation the refusal exists to end.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.structural_noise import find_structural_noise
from sldb.api.documents.structural_noise_report import StructuralNoiseReport


def scan_structural_noise(store_path: Path, project_root: Path, pythonpath: str | None = None) -> list[StructuralNoiseReport]:
    """Every tracked document carrying headings its model does not declare.

    Args:
        store_path: The `.sldb` directory to scan.
        project_root: The root the documents' paths are relative to.
        pythonpath: Directory to import the model modules from.

    Returns:
        One report per noisy document, in store order; empty when the store is clean.
    """
    from sldb.api.model_registry.model_reference import resolve_model_ref
    from sldb.store.query import load_runtime_documents

    documents = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    found = (_scan_one(doc, project_root) for doc in documents)
    return [report for report in found if report is not None and not report.clean]


def _scan_one(doc, project_root: Path) -> StructuralNoiseReport | None:
    """The noise report for one tracked document, or None when its file is gone."""
    doc_path = project_root / doc.path
    if not doc_path.exists():
        return None
    markdown = doc_path.read_text(encoding="utf-8")
    return find_structural_noise(doc.model_type, markdown, doc.name)
