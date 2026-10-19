---
id: python-sldb-sldb-api-model_drafts-backfill-check_and_plan
system: sldb
module: sldb.api.model_drafts.backfill
qualname: check_and_plan
kind: FunctionDef
source_path: sldb/api/model_drafts/backfill.py
source_span: '42:49'
source_sha256: 2d50a8e235b6f4d23db522c72e334767e0ae992d11812096d7e27fd2dd325c65
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_drafts.backfill:check_and_plan; contract-sha256:36fcd32b26c52341e434753784592f36684c3426d253ae9878b87aee92b4b3b6
---

# check_and_plan

## Signature

check_and_plan(store: str | Path | None, model_name: str, old_type: type, new_type: type)

## Docstring

Check every document under the new contract and return the backfill plan.

## Imports

["__future__", "dataclasses", "pathlib", "pydantic", "sldb.api.documents.payload_diff", "sldb.api.journal", "sldb.api.model_drafts.draft_contract", "sldb.api.model_drafts.draft_document_check", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store.facade", "sldb.store.hashing", "typing"]

## Purpose

Check every document under the new contract and return the backfill plan.

## Architecture

Not documented.
