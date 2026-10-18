---
id: python-sldb-sldb-api-corpus-field_entries-_field_hashes
system: sldb
module: sldb.api.corpus.field_entries
qualname: _field_hashes
kind: FunctionDef
source_path: sldb/api/corpus/field_entries.py
source_span: 57:69
source_sha256: f1c6c3fd6209973de2a471da239e1e6861b4a0a1f036438a86b432b08d1d529c
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.corpus.field_entries:_field_hashes; contract-sha256:ac26c067821e505a75847ba9ebed155a4ac280b71ecacb954dcceea5cd11e1c0
---

# _field_hashes

## Signature

_field_hashes(record: Any)

## Docstring

The record's per-field hashes, recomputed when the store never recorded them.

An empty map means the store predates `field_hashes` (or the document no longer
extracts), never that no field has a hash. Falling back to hashing the payload in
memory keeps a per-field index usable against an un-migrated store — at the cost of
hashing on read — instead of leaving every entry unhashed and re-embedding everything
on every refresh.

## Imports

["__future__", "sldb.api.corpus.corpus_entries", "sldb.api.corpus.document_context", "sldb.api.corpus.field_entry", "sldb.api.corpus.field_hit", "sldb.api.model_registry.model_reference", "sldb.store.hashing", "sldb.store.query", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
