---
id: python-sldb-sldb-api-corpus-index_projection-indexprojection
system: sldb
module: sldb.api.corpus.index_projection
qualname: IndexProjection
kind: ClassDef
source_path: sldb/api/corpus/index_projection.py
source_span: 31:68
source_sha256: d5c0a6175ce5476bcd78e6644ca3510cae6e573c36b3645ca2b693358a41ac73
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.corpus.index_projection:IndexProjection; contract-sha256:85ad8dec6ea94516820f24b5813f606ac49ae073d38ca3fae386dd01a0cf0edd
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

What a consumer declares about its corpus: which documents it admits and how it reads the text of one.

## Architecture

Not documented.
