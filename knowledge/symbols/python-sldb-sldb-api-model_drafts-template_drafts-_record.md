---
id: python-sldb-sldb-api-model_drafts-template_drafts-_record
system: sldb
module: sldb.api.model_drafts.template_drafts
qualname: _record
kind: FunctionDef
source_path: sldb/api/model_drafts/template_drafts.py
source_span: 56:60
source_sha256: 2dc3dcd5ff106176457674fffaccc7fe75d9b3e5c31c4de27c62c5d3334bf448
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_drafts.template_drafts:_record; contract-sha256:294b979204fc6569bdea12ece59fd29cf1bcbad142c7e8a8922603968bfbe8a0
---

# _record

## Signature

_record(store: str | Path | None, model_name: str, previous: str, new: str)

## Docstring

Record a template edit; it writes only the `.py.temp`, so `store_hash` is unchanged.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.model_drafts.model_draft", "sldb.api.model_drafts.model_source", "sldb.api.model_drafts.source_location", "sldb.api.model_drafts.template_literals", "sldb.api.stores.open_store"]

## Purpose

Record a template edit; it writes only the `.py.temp`, so `store_hash` is unchanged.

## Architecture

Not documented.
