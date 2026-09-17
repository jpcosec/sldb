"""Prepare a store for typed relations (what `kgdb init` / `kgdb.world.init_world` did)."""

from __future__ import annotations

from pathlib import Path

from sldb.api.edges.rebuild_edges import rebuild_edges
from sldb.api.edges.builtin_relation_writes import register_builtin_predicates, write_builtin_relation_types
from sldb.api.edges.relation_models import register_relation_models
from sldb.api.edges.relations_init_report import RelationsInitReport
from sldb.api.stores.open_store import open_store


def init_relations(store: str | Path | None, pythonpath: str | None = None) -> RelationsInitReport:
    """Register RelationTypeDoc and RelationDoc, track the builtin relation types as
    documents, and register each relation name as a predicate. Idempotent.

    Args:
        store: The store to prepare (path, alias, or None to discover it).
        pythonpath: Directory the store's own model modules import from.

    Returns:
        What this call added; every list is empty when the store was already prepared.

    Raises:
        SLDBModelError: When a relation model cannot be registered.
    """
    location = open_store(store)
    report = RelationsInitReport()
    register_relation_models(location.store_path, location.project_root, pythonpath, report)
    write_builtin_relation_types(location.store_path, location.project_root, pythonpath, report)
    register_builtin_predicates(location.store_path, report)
    if report.models_repointed:
        rebuild_edges(location.store_path, pythonpath)  # the model nodes carry their model_ref
    return report
