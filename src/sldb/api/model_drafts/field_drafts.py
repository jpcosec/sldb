"""Add or remove a field in a model's draft contract.

A field edit also edits the model's template: the field must have a marker in
`__template__` or it would never render nor extract — a phantom field.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.data_values import parse_data_value
from sldb.api.journal import record, store_hash
from sldb.api.model_drafts.field_blocks import (
    field_block,
    field_block_source,
    insert_field_block,
    remove_field_block,
)
from sldb.api.model_drafts.model_draft import ModelDraft
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_drafts.template_literals import read_template_literal, replace_template_literal
from sldb.api.model_drafts.template_sections import append_section, remove_field_section, section_for_field
from sldb.api.stores.open_store import open_store


def add_model_field(store: str | Path | None, model_name: str, field_name: str, field_type: str = "str", description: str = "", default: str | None = None, pythonpath: str | None = None) -> ModelDraft:
    """Declare a new field in the model's draft, plus its template section.

    Args:
        store: The store registering the model (path, alias, or None to discover it).
        model_name: Registered model name.
        field_name: Name of the new field.
        field_type: Python annotation of the field, as source text (e.g. `int`, `list[str]`).
        description: The field's description.
        default: Default value written as JSON or YAML text (e.g. `5`, `"Pending"`);
            None declares the field without a default, i.e. required. An empty string
            is the empty-string default, not "no default".
        pythonpath: Directory to import re-export modules from.

    Returns:
        The draft the field was added to.

    Raises:
        SLDBModelError: When the model is not registered.
        SLDBModelEditError: When the class is not found or already declares the field.
    """
    source = locate_model_source(store, model_name, pythonpath)
    default_value = _default_value(default)
    block = field_block(field_name, field_type, description, default is not None, default_value)
    updated = insert_field_block(source.editable_path, source.class_name, field_name, block)
    source.draft_path.write_text(updated, encoding="utf-8")
    _append_template(source, field_name, field_type, default is not None)
    _record(store, "add_model_field", model_name, field_name, None, block)
    return ModelDraft(model=model_name, draft_path=source.draft_path)


def remove_model_field(store: str | Path | None, model_name: str, field_name: str, pythonpath: str | None = None) -> ModelDraft:
    """Remove a field's declaration and template section from the model's draft.

    Args:
        store: The store registering the model (path, alias, or None to discover it).
        model_name: Registered model name.
        field_name: Name of the field to remove.
        pythonpath: Directory to import re-export modules from.

    Returns:
        The draft the field was removed from.

    Raises:
        SLDBModelError: When the model is not registered.
        SLDBModelEditError: When the class is not found or does not declare the field.
    """
    source = locate_model_source(store, model_name, pythonpath)
    removed = field_block_source(source.editable_path, source.class_name, field_name)
    updated = remove_field_block(source.editable_path, source.class_name, field_name)
    source.draft_path.write_text(updated, encoding="utf-8")
    _remove_template(source, field_name)
    _record(store, "remove_model_field", model_name, field_name, removed, None)
    return ModelDraft(model=model_name, draft_path=source.draft_path)


def _append_template(source, field_name: str, field_type: str, optional: bool) -> None:
    template = read_template_literal(source.draft_path, source.class_name)
    section = section_for_field(field_name, field_type, optional)
    updated = replace_template_literal(source.draft_path, source.class_name, append_section(template, section))
    source.draft_path.write_text(updated, encoding="utf-8")


def _remove_template(source, field_name: str) -> None:
    template = read_template_literal(source.draft_path, source.class_name)
    updated = replace_template_literal(source.draft_path, source.class_name, remove_field_section(template, field_name))
    source.draft_path.write_text(updated, encoding="utf-8")


def _default_value(default: str | None):
    """The parsed default: an explicit empty string stays "", anything else parses as JSON/YAML."""
    if default is None:
        return None
    if default == "":
        return ""
    return parse_data_value(default)


def _record(store: str | Path | None, operation: str, model_name: str, field: str, previous, new) -> None:
    """Record a draft edit; it writes only the `.py.temp`, so `hash_a` is unchanged."""
    sp = open_store(store).store_path
    h = store_hash(sp)
    record(sp, {"operation": operation, "address": model_name, "field": field, "previous_value": previous, "new_value": new, "hash_a_before": h, "hash_a_after": h})
