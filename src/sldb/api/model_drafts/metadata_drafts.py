"""Edit class-level metadata (__containment__, __references__, __compositions__, __semantics__, __authority__) in a model draft."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_drafts.metadata_literals import read_metadata_literal, replace_or_insert_metadata
from sldb.api.model_drafts.model_draft import ModelDraft
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_drafts.template_literals import (
    declares_template,
    insert_template_assignment,
    read_template_literal,
    replace_template_literal,
)
from sldb.api.model_drafts.template_sections import append_section, remove_field_section
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.stores.open_store import open_store


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
    text = editable.read_text(encoding="utf-8")

    added_comps: set[str] = set()
    removed_comps: set[str] = set()
    if compositions is not None:
        old_comps = read_metadata_literal(editable, source.class_name, "__compositions__")
        if old_comps is None:
            try:
                cls = load_registered_model(open_store(store).store_path, model_name, pythonpath).model_type
                old_comps = getattr(cls, "__compositions__", {}) or {}
            except Exception:
                old_comps = {}
        old_keys = set(old_comps.keys()) if isinstance(old_comps, dict) else set()
        new_keys = set(compositions.keys())
        added_comps = new_keys - old_keys
        removed_comps = old_keys - new_keys

    if authority is not None:
        text = replace_or_insert_metadata(text, source.class_name, editable, "__authority__", authority)
    if semantics is not None:
        text = replace_or_insert_metadata(text, source.class_name, editable, "__semantics__", semantics)
    if containment is not None:
        text = replace_or_insert_metadata(text, source.class_name, editable, "__containment__", containment)
    if references is not None:
        text = replace_or_insert_metadata(text, source.class_name, editable, "__references__", references)
    if compositions is not None:
        text = replace_or_insert_metadata(text, source.class_name, editable, "__compositions__", compositions)

    source.draft_path.write_text(text, encoding="utf-8")

    if compositions is not None and (added_comps or removed_comps):
        _sync_compositions_template(source, store, model_name, pythonpath, added_comps, removed_comps)

    return ModelDraft(model=model_name, draft_path=source.draft_path)


def _sync_compositions_template(
    source,
    store: str | Path | None,
    model_name: str,
    pythonpath: str | None,
    added_comps: set[str],
    removed_comps: set[str],
) -> None:
    path = source.draft_path
    if declares_template(path, source.class_name):
        tpl = read_template_literal(path, source.class_name)
        for c in sorted(removed_comps):
            tpl = remove_field_section(tpl, c)
        for c in sorted(added_comps):
            if f"⸢render•{c}⸥" not in tpl:
                title = c.replace("_", " ").capitalize()
                tpl = append_section(tpl, f"## {title}\n\n⸢render•{c}⸥")
        path.write_text(replace_template_literal(path, source.class_name, tpl), encoding="utf-8")
        return

    try:
        inherited = load_registered_model(open_store(store).store_path, model_name, pythonpath).model_type.__template__
    except Exception:
        inherited = ""
    tpl = inherited
    for c in sorted(removed_comps):
        tpl = remove_field_section(tpl, c)
    for c in sorted(added_comps):
        if f"⸢render•{c}⸥" not in tpl:
            title = c.replace("_", " ").capitalize()
            tpl = append_section(tpl, f"## {title}\n\n⸢render•{c}⸥")
    path.write_text(insert_template_assignment(path, source.class_name, tpl), encoding="utf-8")
