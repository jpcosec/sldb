"""Register the two relation models in a store, or re-point them when kgdb registered them."""

from __future__ import annotations

import inspect
from pathlib import Path

from sldb.api.edges.relations_init_report import RelationsInitReport
from sldb.api.model_registry.add_model import add_model
from sldb.api.model_registry.model_index_writes import relative_model_path
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.store.io import load_models_index, load_store_index, save_models_index, save_store_index, store_lock

RELATION_MODEL_REFS = ("sldb.models.relation_type_doc:RelationTypeDoc", "sldb.models.relation_doc:RelationDoc")


def register_relation_models(sp: Path, root: Path, pythonpath: str | None, report: RelationsInitReport) -> None:
    """RelationTypeDoc and RelationDoc registered from `sldb.models`, whatever was there."""
    for ref in RELATION_MODEL_REFS:
        name = ref.split(":", 1)[1]
        entry = next((m for m in load_store_index(sp).models if m.name == name), None)
        if entry is None:
            add_model(sp, ref, pythonpath)
            report.models_added.append(ref)
        elif entry.model_ref != ref:
            _repoint(sp, root, name, ref)
            report.models_repointed.append(name)


def _repoint(sp: Path, root: Path, name: str, ref: str) -> None:
    """The same class under its new home: only `model_ref` and `path` move (neither is hashed)."""
    path = relative_model_path(Path(inspect.getfile(resolve_model_ref(ref))), root)
    with store_lock(sp):
        idx = load_store_index(sp)
        entry = next(m for m in idx.models if m.name == name)
        m_idx = load_models_index(root / entry.models_index)
        entry.model_ref, entry.path = ref, path
        m_idx.model_ref, m_idx.path = ref, path
        save_models_index(root / entry.models_index, m_idx)
        save_store_index(sp, idx)
