"""Keep a draft's template in step with the compositions an edit adds or removes."""

from __future__ import annotations

from pathlib import Path

from sldb.api.model_drafts.metadata_literals import read_metadata_literal
from sldb.api.model_drafts.template_literals import (
    declares_template,
    insert_template_assignment,
    read_template_literal,
    replace_template_literal,
)
from sldb.api.model_drafts.template_sections import append_section, remove_field_section
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.stores.open_store import open_store


def composition_delta(source, store: str | Path | None, model_name: str, pythonpath: str | None, compositions: dict | None) -> tuple[set[str], set[str]]:
    """Composition names (added, removed) by replacing the draft's compositions."""
    if compositions is None:
        return set(), set()
    old = read_metadata_literal(source.editable_path, source.class_name, "__compositions__")
    if old is None:
        old = _registered_attr(store, model_name, pythonpath, "__compositions__", {})
    old_keys = set(old.keys()) if isinstance(old, dict) else set()
    return set(compositions) - old_keys, old_keys - set(compositions)


def _registered_attr(store, model_name: str, pythonpath: str | None, attr: str, default):
    """A class attribute of the registered model, or `default` when it cannot be loaded."""
    try:
        cls = load_registered_model(open_store(store).store_path, model_name, pythonpath).model_type
        return getattr(cls, attr, default) or default
    except Exception:
        return default


def _edited_template(tpl: str, added: set[str], removed: set[str]) -> str:
    """The template without the removed compositions' sections and with the added ones'."""
    for c in sorted(removed):
        tpl = remove_field_section(tpl, c)
    for c in sorted(added):
        if f"⸢render•{c}⸥" not in tpl:
            tpl = append_section(tpl, f"## {c.replace('_', ' ').capitalize()}\n\n⸢render•{c}⸥")
    return tpl


def sync_compositions_template(source, store: str | Path | None, model_name: str, pythonpath: str | None, added: set[str], removed: set[str]) -> None:
    """Rewrite the draft's template literal, or declare one from the inherited template."""
    path = source.draft_path
    if declares_template(path, source.class_name):
        tpl = _edited_template(read_template_literal(path, source.class_name), added, removed)
        path.write_text(replace_template_literal(path, source.class_name, tpl), encoding="utf-8")
        return
    tpl = _edited_template(_registered_attr(store, model_name, pythonpath, "__template__", ""), added, removed)
    path.write_text(insert_template_assignment(path, source.class_name, tpl), encoding="utf-8")
