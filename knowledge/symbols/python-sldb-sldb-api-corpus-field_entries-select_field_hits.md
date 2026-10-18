---
id: python-sldb-sldb-api-corpus-field_entries-select_field_hits
system: sldb
module: sldb.api.corpus.field_entries
qualname: select_field_hits
kind: FunctionDef
source_path: sldb/api/corpus/field_entries.py
source_span: 79:93
source_sha256: f1c6c3fd6209973de2a471da239e1e6861b4a0a1f036438a86b432b08d1d529c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.corpus.field_entries:select_field_hits; contract-sha256:dc3b64c4fb5d9b30a7d4114e6adacda062847da08648ef7f0e5862471e0721a8
---

# select_field_hits

## Signature

select_field_hits(ranked, by_id, allowed: set[str] | None, k: int | None)

## Docstring

The ranked fields still in the corpus (and among the allowed ones), at most k.

`allowed` admits a field by its own id or by its document's: narrowing to a document
means every field of it, which is what a caller filtering by document intends.

## Imports

["__future__", "sldb.api.corpus.corpus_entries", "sldb.api.corpus.document_context", "sldb.api.corpus.field_entry", "sldb.api.corpus.field_hit", "sldb.api.model_registry.model_reference", "sldb.store.hashing", "sldb.store.query", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
