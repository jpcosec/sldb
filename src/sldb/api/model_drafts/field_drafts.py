"""Add or remove a field in a model's draft contract."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.data_values import parse_data_value
from sldb.api.model_drafts.field_blocks import field_block, insert_field_block, remove_field_block
from sldb.api.model_drafts.model_draft import ModelDraft
from sldb.api.model_drafts.source_location import locate_model_source


def add_model_field(store: str | Path | None, model_name: str, field_name: str, field_type: str = "str", description: str = "", default: str | None = None, pythonpath: str | None = None) -> ModelDraft:
    """Declare a new field in the model's draft (created from the active source if absent).

    Args:
        store: The store registering the model (path, alias, or None to discover it).
        model_name: Registered model name.
        field_name: Name of the new field.
        field_type: Python annotation of the field, as source text (e.g. `int`, `list[str]`).
        description: The field's description.
        default: Default value written as JSON or YAML text (e.g. `5`, `"Pending"`);
            None declares the field without a default, i.e. required.
        pythonpath: Directory to import re-export modules from.

    Returns:
        The draft the field was added to.

    Raises:
        SLDBModelError: When the model is not registered.
        SLDBModelEditError: When the class is not found or already declares the field.
    """
    source = locate_model_source(store, model_name, pythonpath)
    default_value = parse_data_value(default) if default is not None else None
    block = field_block(field_name, field_type, description, default is not None, default_value)
    updated = insert_field_block(source.editable_path, source.class_name, field_name, block)
    source.draft_path.write_text(updated, encoding="utf-8")
    return ModelDraft(model=model_name, draft_path=source.draft_path)


def remove_model_field(store: str | Path | None, model_name: str, field_name: str, pythonpath: str | None = None) -> ModelDraft:
    """Remove a field's declaration from the model's draft (created from the active source if absent).

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
    updated = remove_field_block(source.editable_path, source.class_name, field_name)
    source.draft_path.write_text(updated, encoding="utf-8")
    return ModelDraft(model=model_name, draft_path=source.draft_path)
