"""Validate a model's draft contract against its tracked documents, and promote it."""

from __future__ import annotations

import sys
from pathlib import Path

from sldb.api.model_drafts.draft_checks import check_documents, current_version
from sldb.api.model_drafts.draft_loading import load_model_from_path
from sldb.api.model_drafts.draft_restore import restored_on_failure, store_index_files
from sldb.api.model_drafts.draft_validation_report import DraftValidationReport
from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_registry.reindex_model import reindex_model
from sldb.core.exceptions import SLDBModelDraftError


def validate_model_draft(store: str | Path | None, model_name: str, pythonpath: str | None = None) -> DraftValidationReport:
    """Check the draft (or the active model when there is no draft) without installing it.

    Args:
        store: The store registering the model (path, alias, or None to discover it).
        model_name: Registered model name.
        pythonpath: Directory to import the model's modules from.

    Returns:
        The validation report, with `promoted` False.

    Raises:
        SLDBModelError: When the model is not registered.
        SLDBModelEditError: When the template references unknown fields or the draft is broken.
        SLDBValidationError: When a tracked document does not round-trip under the contract.
    """
    return _checked(store, model_name, pythonpath)[1]


def promote_model_draft(store: str | Path | None, model_name: str, pythonpath: str | None = None) -> DraftValidationReport:
    """Validate the draft, install it over the active model, reindex and bump the version.

    If the reindex fails, the active model, the draft and the store indexes are put back.
    The promoted model's modules (defining and registered) are dropped from `sys.modules`, so the next
    `resolve_model_ref` in this process imports the new contract.

    Args:
        store: The store registering the model (path, alias, or None to discover it).
        model_name: Registered model name.
        pythonpath: Directory to import the model's modules from.

    Returns:
        The validation report, with `promoted` True and the bumped version.

    Raises:
        SLDBModelDraftError: When the model has no draft to promote.
        SLDBModelError: When the model is not registered.
        SLDBModelEditError: When the template references unknown fields or the draft is broken.
        SLDBValidationError: When a tracked document does not round-trip under the draft.
    """
    source, report = _checked(store, model_name, pythonpath)
    version = _install_draft(store, model_name, source, pythonpath)
    return report.model_copy(update={"promoted": True, "version": version})


def _checked(store: str | Path | None, model_name: str, pythonpath: str | None) -> tuple[ModelSource, DraftValidationReport]:
    """Locate the model, load the contract to check, and check every tracked document."""
    source = locate_model_source(store, model_name, pythonpath)
    checked_path, draft = source.editable_path, source.draft_path.exists()
    model_type = load_model_from_path(checked_path, source.module_name, source.attr_path, pythonpath)
    documents = check_documents(store, model_name, model_type)
    return source, DraftValidationReport(model=model_name, draft=draft, path=checked_path, documents=documents, promoted=False, version=current_version(store, model_name))


def _install_draft(store: str | Path | None, model_name: str, source: ModelSource, pythonpath: str | None) -> int:
    """Copy the draft over the active source and reindex, restoring everything on failure; returns the new version."""
    if not source.draft_path.exists():
        raise SLDBModelDraftError(f"No draft template for '{model_name}' to promote.")
    with restored_on_failure([source.path, source.draft_path, *store_index_files(store)]):
        source.path.write_text(source.draft_path.read_text(encoding="utf-8"), encoding="utf-8")
        registration = reindex_model(store, model_name, pythonpath, bump_version=True)
    source.draft_path.unlink()
    for module_name in {source.module_name, registration.model_ref.split(":", 1)[0]}:
        sys.modules.pop(module_name, None)
    return registration.version
