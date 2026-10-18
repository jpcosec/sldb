---
id: python-sldb-sldb-sldb-api-edges-init_relations-init_relations
system: sldb
module: sldb.sldb.api.edges.init_relations
qualname: init_relations
kind: FunctionDef
source_path: sldb/api/edges/init_relations.py
source_span: '15:38'
source_sha256: 5352927526dbdb3b5f1ac7f4d7bd59c12a829721e13db280e23a7a1fc5d36297
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.edges.init_relations:init_relations; contract-sha256:10c930dca8ae4d3203a2460fa85a9a1c9fedd0d8002880cfabb3cd0d5cfbe7a2
---

# init_relations

## Signature

init_relations(store: str | Path | None, pythonpath: str | None=None)

## Docstring

Register RelationTypeDoc and RelationDoc, track the builtin relation types as
documents, and register each relation name as a predicate. Idempotent.

Args:
    store: The store to prepare (path, alias, or None to discover it).
    pythonpath: Directory the store's own model modules import from.

Returns:
    What this call added; every list is empty when the store was already prepared.

Raises:
    SLDBModelError: When a relation model cannot be registered.

## Imports

["__future__", "pathlib", "sldb.api.edges.builtin_relation_writes", "sldb.api.edges.rebuild_edges", "sldb.api.edges.relation_models", "sldb.api.edges.relations_init_report", "sldb.api.stores.open_store", "sldb.api.stores.update_store_indexes"]

## Purpose

Not documented.

## Architecture

Not documented.
