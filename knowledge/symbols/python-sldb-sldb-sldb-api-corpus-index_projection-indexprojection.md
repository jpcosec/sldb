---
id: python-sldb-sldb-sldb-api-corpus-index_projection-indexprojection
system: sldb
module: sldb.sldb.api.corpus.index_projection
qualname: IndexProjection
kind: ClassDef
source_path: sldb/api/corpus/index_projection.py
source_span: 31:68
source_sha256: d5c0a6175ce5476bcd78e6644ca3510cae6e573c36b3645ca2b693358a41ac73
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.corpus.index_projection:IndexProjection;
  contract-sha256:879e8a35e95d29f556179986e8ced35e960f1342fbc62e8ce0b09aa34f11d224
---

# IndexProjection

## Signature

Not applicable.

## Docstring

What a consumer declares about its corpus: which documents it admits and how it
reads the text of one.

`models` is the allowed set (None: every model); `exclude_models` drops from it. `text`
maps a payload to its representative text; a document whose text is empty stays out,
and `text_id` names the mapping so a change of representation invalidates the index
the same way a change of embedder does.

## Imports

["__future__", "dataclasses", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
