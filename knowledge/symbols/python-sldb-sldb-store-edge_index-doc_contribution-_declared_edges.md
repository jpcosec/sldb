---
id: python-sldb-sldb-store-edge_index-doc_contribution-_declared_edges
system: sldb
module: sldb.store.edge_index.doc_contribution
qualname: _declared_edges
kind: FunctionDef
source_path: sldb/store/edge_index/doc_contribution.py
source_span: '41:55'
source_sha256: 2b167942c5eb3d35e4065601b06f477a96839ba8685bb4d0b6af2161d3889296
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_index.doc_contribution:_declared_edges;
  contract-sha256:02783ac0f08e28469321498c134149015782ef7ff30f5266c27130fbcc935243
---

# _declared_edges

## Signature

_declared_edges(model_name: str, doc: DocumentEntry, model_type: Any | None, payload_of: Callable[[], dict[str, Any] | None], is_special: bool)

## Docstring

The model's declared references, read only when it declares any: the payload is a file
read per document, and most models declare none.

A relation, relation type or anchor document is skipped: its id fields are the edge it
already contributes (`RelationDoc.__references__` names the ends of that very edge), so
reading them again would assert a second, untyped edge beside it.

## Imports

["__future__", "sldb.store.edge_index.composition_edges", "sldb.store.edge_index.declared_references", "sldb.store.edge_index.doc_kinds", "sldb.store.edge_index.doc_structure", "sldb.store.edge_index.node_ids", "sldb.store.edge_index.records", "sldb.store.models", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
