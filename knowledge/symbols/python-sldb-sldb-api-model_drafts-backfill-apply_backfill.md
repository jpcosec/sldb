---
id: python-sldb-sldb-api-model_drafts-backfill-apply_backfill
system: sldb
module: sldb.api.model_drafts.backfill
qualname: apply_backfill
kind: FunctionDef
source_path: sldb/api/model_drafts/backfill.py
source_span: 61:68
source_sha256: 2d50a8e235b6f4d23db522c72e334767e0ae992d11812096d7e27fd2dd325c65
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_drafts.backfill:apply_backfill; contract-sha256:d3a30bdc160abb397a04a9b66af9c8f8a972e0d7907c311c1915549268d90389
---

# apply_backfill

## Signature

apply_backfill(store: str | Path | None, model_name: str, new_type: type, plan: list[BackfillDoc], actor: str | None)

## Docstring

Rewrite each planned document and record its own journal entry; returns the count.

## Imports

["__future__", "dataclasses", "pathlib", "pydantic", "sldb.api.documents.payload_diff", "sldb.api.journal", "sldb.api.model_drafts.draft_contract", "sldb.api.model_drafts.draft_document_check", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store.facade", "sldb.store.hashing", "typing"]

## Purpose

Rewrite each planned document and record its own journal entry; returns the count.

## Architecture

Not documented.
