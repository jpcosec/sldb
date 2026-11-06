"""Edit class-level metadata (__containment__, __references__, __compositions__, __semantics__, __authority__) in a model draft."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_drafts.metadata_composition_sync import composition_delta, sync_compositions_template
from sldb.api.model_drafts.metadata_literals import replace_or_insert_metadata
from sldb.api.model_drafts.model_draft import ModelDraft
from sldb.api.model_drafts.source_location import locate_model_source


def edit_model_metadata(
    store: str | Path | None,
    model_name: str,
    *,
    containment: dict[str, list[str]] | None = None,
    references: list[str] | None = None,
    compositions: dict[str, dict] | None = None,
    semantics: dict[str, list[str]] | None = None,
    authority: str | None = None,
    pythonpath: str | None = None,
) -> ModelDraft:
    """Insert or replace class metadata attributes on a registered model's draft contract.

    Args:
        store: The store registering the model (path, alias, or None to discover it).
        model_name: Registered model name.
        containment: Optional dict for __containment__.
        references: Optional list for __references__.
        compositions: Optional dict for __compositions__.
        semantics: Optional dict for __semantics__.
        authority: Optional str for __authority__.
        pythonpath: Directory to import re-export modules from.

    Returns:
        The draft holding the edited metadata.
    """
    source = locate_model_source(store, model_name, pythonpath)
    editable = source.editable_path
    added, removed = composition_delta(source, store, model_name, pythonpath, compositions)
    values = {"__authority__": authority, "__semantics__": semantics, "__containment__": containment, "__references__": references, "__compositions__": compositions}
    source.draft_path.write_text(_apply_metadata(editable.read_text(encoding="utf-8"), source.class_name, editable, values), encoding="utf-8")
    if added or removed:
        sync_compositions_template(source, store, model_name, pythonpath, added, removed)
    return ModelDraft(model=model_name, draft_path=source.draft_path)


def _apply_metadata(text: str, class_name: str, editable: Path, values: dict[str, Any]) -> str:
    """The source with every given (not None) attribute replaced or inserted, in order."""
    for attr, value in values.items():
        if value is not None:
            text = replace_or_insert_metadata(text, class_name, editable, attr, value)
    return text
