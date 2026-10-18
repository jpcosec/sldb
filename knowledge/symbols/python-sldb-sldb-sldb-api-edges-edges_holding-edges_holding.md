---
id: python-sldb-sldb-sldb-api-edges-edges_holding-edges_holding
system: sldb
module: sldb.sldb.api.edges.edges_holding
qualname: edges_holding
kind: FunctionDef
source_path: sldb/api/edges/edges_holding.py
source_span: '13:31'
source_sha256: 54fb23c131c738eec0ea17fae99ff1f96da7ba21b2d3492c9b8539b380231d27
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.edges.edges_holding:edges_holding; contract-sha256:5561a8f2c4a371f4cc4de556401b40feb94521c130ef823d3968bd31a08d57d1
---

# edges_holding

## Signature

edges_holding(store: str | Path | None, export_id: str, subject: dict[str, Any], relation: str | None=None, include_linked: bool=True, exclude_tags: Iterable[str]=())

## Docstring

The edges leaving `export_id` whose condition holds on `subject`.

Each edge's condition (its own, else its relation type's) is a `--where` predicate read on
the subject's fields, `{field}` filled from the subject too; an edge without a condition
always holds. To test a condition on another document (an edge's target, say) with the
subject in braces, use `where_matches(condition, that_payload, subject)`.

Args:
    store: The store (path, alias, or None to discover it).
    export_id: The node the edges leave (`Model:name`), e.g. the state a task is in.
    subject: The payload the conditions read; need not be a tracked document's.
    relation, include_linked, exclude_tags: As in `edges_from`.

Raises:
    WherePredicateError: An edge's condition does not parse.

## Imports

["__future__", "pathlib", "sldb.api.edges.edge_reading", "sldb.store.models", "sldb.store.query_engine.where_subject", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
