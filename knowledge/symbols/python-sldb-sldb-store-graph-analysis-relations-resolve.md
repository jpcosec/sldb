---
id: python-sldb-sldb-store-graph-analysis-relations-resolve
system: sldb
module: sldb.store.graph.analysis.relations
qualname: resolve
kind: FunctionDef
source_path: sldb/store/graph/analysis/relations.py
source_span: '34:44'
source_sha256: 259e0361c784e0966911e56752b247169a405a7713cf5a96216102d971fd9ebe
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.graph.analysis.relations:resolve; contract-sha256:68d7e550ee8b94d6d2af064148800598ba2360e1126d7aa2e878f962f2e18a7d
---

# resolve

## Signature

resolve(index, relations: object=None)

## Docstring

The relations to walk: the ones asked for, else the authored ones, else everything.

A store with no authored relations yet falls back to all of them, so the analyses say
something instead of nothing on a store that has only its structure.

## Imports

["__future__", "sldb.store.model_contract"]

## Purpose

Not documented.

## Architecture

Not documented.
