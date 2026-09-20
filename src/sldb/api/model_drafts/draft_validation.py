"""Validate a model's draft contract against its tracked documents, and promote it."""

from __future__ import annotations

import sys
from pathlib import Path

from sldb.api.journal import record, store_hash
from sldb.api.model_drafts.backfill import BackfillDoc, apply_backfill, plan_backfill
from sldb.api.model_drafts.draft_checks import check_documents, current_version
from sldb.api.model_drafts.draft_loading import load_model_from_path
from sldb.api.model_drafts.draft_restore import restored_on_failure, store_index_files
from sldb.api.model_drafts.draft_validation_report import DraftValidationReport
from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_registry.reindex_model import reindex_model
from sldb.api.schema.describe_field import schema_snapshot
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelDraftError
from sldb.store.io import load_store_index


def validate_model_draft(store: str | Path | None, model_name: str, pythonpath: str | None = None) -> DraftValidationReport:
    """Check the draft (or the active model when there is no draft) without installing it.

    The report's `backfill` names the tracked documents a backfill promote would rewrite.

    Raises:
        SLDBModelError: When the model is not registered.
        SLDBModelEditError: When the template references unknown fields or the draft is broken.
        SLDBValidationError: When a tracked document does not round-trip under the contract.
    """
    return _checked(store, model_name, pythonpath)[4]


def promote_model_draft(store: str | Path | None, model_name: str, pythonpath: str | None = None, actor: str | None = None, backfill: bool = False) -> DraftValidationReport:
    """Validate the draft, install it, reindex, and bump the version.

    With `backfill=True`, tracked documents missing a new field's default are re-rendered
    under the new contract and each gets its own journal entry; the report lists them, so
    nothing is rewritten without the caller asking for it. On reindex failure the active
    model, the draft and the store indexes are put back.
    """
    source, old_type, new_type, plan, report = _checked(store, model_name, pythonpath)
    before = store_hash(open_store(store).store_path)
    version = _install_draft(store, model_name, source, new_type, plan, pythonpath, actor, backfill)
    _record_promote(store, model_name, old_type, new_type, report.version, version, before, actor)
    return report.model_copy(update={"promoted": True, "version": version})


def _checked(store: str | Path | None, model_name: str, pythonpath: str | None) -> tuple[ModelSource, type, type, list[BackfillDoc], DraftValidationReport]:
    """Locate the model, load both contracts, check every document and plan the backfill."""
    source = locate_model_source(store, model_name, pythonpath)
    checked_path, draft = source.editable_path, source.draft_path.exists()
    new_type = load_model_from_path(checked_path, source.module_name, source.attr_path, pythonpath)
    documents = check_documents(store, model_name, new_type)
    old_type = load_model_from_path(source.path, source.module_name, source.attr_path, pythonpath) if draft else new_type
    plan = plan_backfill(store, model_name, old_type, new_type) if draft else []
    report = DraftValidationReport(model=model_name, draft=draft, path=checked_path, documents=documents, backfill=[b.name for b in plan], promoted=False, version=current_version(store, model_name))
    return source, old_type, new_type, plan, report


def _install_draft(store: str | Path | None, model_name: str, source: ModelSource, new_type: type, plan: list[BackfillDoc], pythonpath: str | None, actor: str | None, backfill: bool) -> int:
    """Install the draft, backfill if asked, reindex, and drop the draft; returns the version."""
    if not source.draft_path.exists():
        raise SLDBModelDraftError(f"No draft template for '{model_name}' to promote.")
    modules = _model_modules(store, model_name, source)
    try:
        version = _install_and_reindex(store, model_name, source, new_type, plan, pythonpath, modules, actor, backfill)
    finally:
        _drop_modules(modules)  # promoted or restored, the next import reads what is on disk now
    source.draft_path.unlink()
    return version


def _install_and_reindex(store: str | Path | None, model_name: str, source: ModelSource, new_type: type, plan: list[BackfillDoc], pythonpath: str | None, modules: set[str], actor: str | None, backfill: bool) -> int:
    paths = [source.path, source.draft_path, *store_index_files(store), *(b.path for b in plan)]
    with restored_on_failure(paths):
        if backfill:
            apply_backfill(store, model_name, new_type, plan, actor)
        source.path.write_text(source.draft_path.read_text(encoding="utf-8"), encoding="utf-8")
        _drop_modules(modules)  # the reindex (document hashes, field nodes) reads the new contract
        return reindex_model(store, model_name, pythonpath, bump_version=True).version


def _record_promote(store: str | Path | None, model_name: str, old_type: type, new_type: type, before_version: int, after_version: int, before: str, actor: str | None) -> None:
    sp = open_store(store).store_path
    record(sp, {"operation": "promote_model_draft", "address": model_name, "previous_value": schema_snapshot(old_type, before_version), "new_value": schema_snapshot(new_type, after_version), "hash_a_before": before, "hash_a_after": store_hash(sp), "actor": actor})


def _model_modules(store: str | Path | None, model_name: str, source: ModelSource) -> set[str]:
    """The modules the model is imported through: the defining one and the registered one."""
    entry = next((m for m in load_store_index(open_store(store).store_path).models if m.name == model_name), None)
    return {source.module_name} | ({entry.model_ref.split(":", 1)[0]} if entry else set())


def _drop_modules(modules: set[str]) -> None:
    for module_name in modules:
        sys.modules.pop(module_name, None)
