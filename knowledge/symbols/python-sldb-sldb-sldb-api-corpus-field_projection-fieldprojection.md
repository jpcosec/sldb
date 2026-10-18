---
id: python-sldb-sldb-sldb-api-corpus-field_projection-fieldprojection
system: sldb
module: sldb.sldb.api.corpus.field_projection
qualname: FieldProjection
kind: ClassDef
source_path: sldb/api/corpus/field_projection.py
source_span: 64:106
source_sha256: 12b805b729ee9e80e1d3924b72db118bb702cd532a050ded986479ca9ebdce97
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.corpus.field_projection:FieldProjection;
  contract-sha256:d3a2729d2a6dc9d55911fd1c0160d63e78133aa6102f9ef146b8af81212e19f2
---

# FieldProjection

## Signature

Not applicable.

## Docstring

Which fields of which models a consumer indexes, and how it reads one.

`include` is the allowed set (None: every field the payload has); `exclude` drops from
it and defaults to identity and bookkeeping fields. `min_chars` keeps one-word fields
out, where similarity is noise.

`text_id` names the mapping for the same reason `IndexProjection.text_id` does: a change
of representation has to invalidate the index the way a change of embedder does. It is
part of the derived file's name, so two projections never share one file.

## Imports

["__future__", "dataclasses", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
