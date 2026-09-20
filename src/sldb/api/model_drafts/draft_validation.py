"""Validate a model's draft contract against its tracked documents, and promote it."""

from __future__ import annotations

import sys
from pathlib import Path

from sldb.api.journal import record, store_hash
from sldb.api.model_drafts.draft_checks import check_documents, current_version
from sldb.api.model_drafts.draft_loading import load_model_from_path
from sldb.api.model_drafts.draft_restore import restored_on_failure, store_index_files
from sldb.api.model_drafts.draft_validation_report import DraftValidationReport
from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_registry.reindex_model import reindex_model
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelDraftError
from sldb.store.io import load_store_index


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


def promote_model_draft(store: str | Path | None, model_name: str, pythonpath: str | None = None, actor: str | None = None) -> DraftValidationReport:
    """Validate the draft, install it over the active model, reindex and bump the version.

    If the reindex fails, the active model, the draft and the store indexes are put back.
    The promoted model's modules (defining and registered) are dropped from `sys.modules` before
    the reindex and again after it, so the reindex and the next `resolve_model_ref` in this
    process both import the contract that is on disk.

    Args:
        store: The store registering the model (path, alias, or None to discover it).
        model_name: Registered model name.
        pythonpath: Directory to import the model's modules from.
        actor: Optional label recorded in the store journal for this write.

    Returns:
        The validation report, with `promoted` True and the bumped version.

    Raises:
        SLDBModelDraftError: When the model has no draft to promote.
        SLDBModelError: When the model is not registered.
        SLDBModelEditError: When the template references unknown fields or the draft is broken.
        SLDBValidationError: When a tracked document does not round-trip under the draft.
    """
    source, report = _checked(store, model_name, pythonpath)
    before = store_hash(open_store(store).store_path)
    version = _install_draft(store, model_name, source, pythonpath, actor, before)
    return report.model_copy(update={"promoted": True, "version": version})


def _checked(store: str | Path | None, model_name: str, pythonpath: str | None) -> tuple[ModelSource, DraftValidationReport]:
    """Locate the model, load the contract to check, and check every tracked document."""
    source = locate_model_source(store, model_name, pythonpath)
    checked_path, draft = source.editable_path, source.draft_path.exists()
    model_type = load_model_from_path(checked_path, source.module_name, source.attr_path, pythonpath)
    documents = check_documents(store, model_name, model_type)
    return source, DraftValidationReport(model=model_name, draft=draft, path=checked_path, documents=documents, promoted=False, version=current_version(store, model_name))


def _install_draft(store: str | Path | None, model_name: str, source: ModelSource, pythonpath: str | None, actor: str | None, before: str) -> int:
    """Copy the draft over the active source and reindex, restoring everything on failure; returns the new version."""
    if not source.draft_path.exists():
        raise SLDBModelDraftError(f"No draft template for '{model_name}' to promote.")
    modules = _model_modules(store, model_name, source)
    try:
        version = _install_and_reindex(store, model_name, source, pythonpath, modules)
    finally:
        _drop_modules(modules)  # promoted or restored, the next import reads what is on disk now
    source.draft_path.unlink()
    _record_promote(store, model_name, before, actor)
    return version


def _install_and_reindex(store: str | Path | None, model_name: str, source: ModelSource, pythonpath: str | None, modules: set[str]) -> int:
    with restored_on_failure([source.path, source.draft_path, *store_index_files(store)]):
        source.path.write_text(source.draft_path.read_text(encoding="utf-8"), encoding="utf-8")
        _drop_modules(modules)  # the reindex (document hashes, the edge index's field nodes) reads the new contract
        return reindex_model(store, model_name, pythonpath, bump_version=True).version


def _record_promote(store: str | Path | None, model_name: str, before: str, actor: str | None) -> None:
    sp = open_store(store).store_path
    record(sp, {"operation": "promote_model_draft", "address": model_name, "hash_a_before": before, "hash_a_after": store_hash(sp), "actor": actor})


def _model_modules(store: str | Path | None, model_name: str, source: ModelSource) -> set[str]:
    """The modules the model is imported through: the defining one and the registered one."""
    entry = next((m for m in load_store_index(open_store(store).store_path).models if m.name == model_name), None)
    return {source.module_name} | ({entry.model_ref.split(":", 1)[0]} if entry else set())


def _drop_modules(modules: set[str]) -> None:
    for module_name in modules:
        sys.modules.pop(module_name, None)
