---
id: python-sldb-sldb-sldb-api-model_drafts-backfill-check_and_plan
system: sldb
module: sldb.sldb.api.model_drafts.backfill
qualname: check_and_plan
kind: FunctionDef
source_path: sldb/api/model_drafts/backfill.py
source_span: '42:49'
source_sha256: 2d50a8e235b6f4d23db522c72e334767e0ae992d11812096d7e27fd2dd325c65
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_drafts.backfill:check_and_plan;
  contract-sha256:86c1c2b7e8c8ab8c7d8c0c1d576ac318fa93dfb793bb88ff71162d7badb082cb
---

# check_and_plan

## Signature

check_and_plan(store: str | Path | None, model_name: str, old_type: type, new_type: type)

## Docstring

Check every document under the new contract and return the backfill plan.

## Imports

["__future__", "dataclasses", "pathlib", "pydantic", "sldb.api.documents.payload_diff", "sldb.api.journal", "sldb.api.model_drafts.draft_contract", "sldb.api.model_drafts.draft_document_check", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store.facade", "sldb.store.hashing", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
