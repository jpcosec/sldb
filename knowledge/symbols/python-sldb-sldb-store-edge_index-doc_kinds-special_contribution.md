---
id: python-sldb-sldb-store-edge_index-doc_kinds-special_contribution
system: sldb
module: sldb.store.edge_index.doc_kinds
qualname: special_contribution
kind: FunctionDef
source_path: sldb/store/edge_index/doc_kinds.py
source_span: '16:23'
source_sha256: b3816bd95fe92c1563ed013c1e9cb9cb6c117d12499e2ceaef2b3535ae9da70c
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.edge_index.doc_kinds:special_contribution;
  contract-sha256:1e9ead6d3716ae9a0bcddbd5b82e2242e71b06289755ca7ebb79f8f203e8878a
---

# special_contribution

## Signature

special_contribution(model_name: str, doc: DocumentEntry, payload_of: Callable[[], Payload | None])

## Docstring

The contribution of a relation type, relation or anchor document; None for a plain one
(or one whose payload cannot be read: it stays a plain document).

## Imports

["__future__", "sldb.store.edge_index.anchor_targets", "sldb.store.edge_index.node_ids", "sldb.store.edge_index.records", "sldb.store.models", "typing"]

## Purpose

The contribution of a relation type, relation or anchor document; None for a plain one (or one whose payload cannot be read: it stays a plain document).

## Architecture

Not documented.
