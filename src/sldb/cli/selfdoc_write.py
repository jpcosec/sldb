"""Persist prepared documentation through SLDB document tracking operations."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from sldb.cli.commands.model_add import add_model
from sldb.cli.commands.fields_save import save_payload
from sldb.cli.model_utils import resolve_model_ref
from sldb.selfdoc.planned_document import PlannedDocument
from sldb.store.io import load_store_index
from sldb.store.io.utils import StoreIOUtils
from sldb.store.ops import track_document
from sldb.store.section_rebuild import rebuild_sections_indexes
from .selfdoc_registry import DocumentationRegistry


def write_documents(plans: list[PlannedDocument], store: Path, root: Path) -> int:
    """Register models and apply only changed or untracked records."""
    _check_before_images(plans)
    _register_models(plans, store, root)
    written = _write_changed(plans, store, root)
    if written:
        rebuild_sections_indexes(store, root, resolve_model_ref, str(root))
    return written


def _write_changed(plans, store, root) -> int:
    registry = DocumentationRegistry(store, root)
    written = 0
    for plan in plans:
        status = registry.status(plan)
        if plan.changed or status:
            _save_document(plan, status, store, root)
            registry = DocumentationRegistry(store, root)
            written += 1
    return written


def _check_before_images(plans: list[PlannedDocument]) -> None:
    for plan in plans:
        current = plan.path.read_text(encoding="utf-8") if plan.path.exists() else None
        if current != plan.previous:
            raise ValueError(f"Document changed during planning: {plan.path}")


def _register_models(plans, store, root):
    existing = {entry.name for entry in load_store_index(store).models}
    for name in sorted({plan.model_name for plan in plans} - existing):
        add_model(SimpleNamespace(store=str(store), pythonpath=str(root), canonical=False,
                                  model=f"sldb.models.knowledge_surface:{name}"))


def _save_document(plan, status, store, root):
    if status != "untracked":
        runtime = SimpleNamespace(model_name=plan.model_name, name=plan.payload.id)
        save_payload(runtime, plan.payload.model_dump(mode="json"), str(store), str(root))
        return
    if plan.changed:
        StoreIOUtils._atomic_write(plan.path, plan.markdown)
    index = load_store_index(store)
    entry = next(m for m in index.models if m.name == plan.model_name)
    track_document(store, root, index, type(plan.payload), entry, plan.path, plan.payload.id,
                   resolve_model_ref, str(root))
