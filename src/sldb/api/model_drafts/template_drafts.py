"""Replace the Markdown template of a model's draft contract."""

from __future__ import annotations

from pathlib import Path

from sldb.api.journal import record, store_hash
from sldb.api.model_drafts.model_draft import ModelDraft
from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_drafts.template_literals import read_template_literal, replace_template_literal
from sldb.api.stores.open_store import open_store


def edit_model_template(store: str | Path | None, model_name: str, template: str, pythonpath: str | None = None) -> ModelDraft:
    """Write `template` as the draft template of a registered model.

    Args:
        store: The store registering the model (path, alias, or None to discover it).
        model_name: Registered model name.
        template: The new template text; trailing newlines are dropped.
        pythonpath: Directory to import re-export modules from.

    Returns:
        The draft holding the new template.

    Raises:
        SLDBModelError: When the model is not registered.
        SLDBModelEditError: When the class or its `__template__` assignment is not found.
    """
    source = locate_model_source(store, model_name, pythonpath)
    previous = read_template_literal(source.editable_path, source.class_name)
    draft = write_template_draft(source, template)
    _record(store, model_name, previous, template.rstrip("\n"))
    return ModelDraft(model=model_name, draft_path=draft)


def write_template_draft(source: ModelSource, template: str) -> Path:
    """Write `template` into the draft of an already located model source.

    Args:
        source: Where the model class is defined.
        template: The new template text; trailing newlines are dropped.

    Returns:
        The draft path written.

    Raises:
        SLDBModelEditError: When the class or its `__template__` assignment is not found.
    """
    updated = replace_template_literal(source.editable_path, source.class_name, template.rstrip("\n"))
    source.draft_path.write_text(updated, encoding="utf-8")
    return source.draft_path


def _record(store: str | Path | None, model_name: str, previous: str, new: str) -> None:
    """Record a template edit; it writes only the `.py.temp`, so `hash_a` is unchanged."""
    sp = open_store(store).store_path
    h = store_hash(sp)
    record(sp, {"operation": "edit_model_template", "address": model_name, "field": "__template__", "previous_value": previous, "new_value": new, "hash_a_before": h, "hash_a_after": h})
