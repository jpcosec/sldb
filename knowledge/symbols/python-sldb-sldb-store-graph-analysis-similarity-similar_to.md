---
id: python-sldb-sldb-store-graph-analysis-similarity-similar_to
system: sldb
module: sldb.store.graph.analysis.similarity
qualname: similar_to
kind: FunctionDef
source_path: sldb/store/graph/analysis/similarity.py
source_span: '18:28'
source_sha256: 6463277a080afcc75deae4d9442216811843351215170e1281455dece4ce217a
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.graph.analysis.similarity:similar_to; contract-sha256:ea52b8d9f7bc39e9084d2804ea3d5da5e5acfcf305ecf880625b7796690ba392
---

# similar_to

## Signature

similar_to(index, node_id: str, relations: object=('tagged_as',), limit: int=10, node_types: object=None)

## Docstring

Nodes sharing the most targets with `node_id`, most shared first.

Defaults to `tagged_as`: what else is tagged the way this is. Ties break by node id.

## Imports

["__future__", "collections", "sldb.store.graph.analysis.nx_graph"]

## Purpose

Not documented.

## Architecture

Not documented.
