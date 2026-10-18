---
id: python-sldb-sldb-api-model_drafts-draft_validation-promote_model_draft
system: sldb
module: sldb.api.model_drafts.draft_validation
qualname: promote_model_draft
kind: FunctionDef
source_path: sldb/api/model_drafts/draft_validation.py
source_span: '36:48'
source_sha256: d049ed57d4c2347b4f75bee2034d88b861928f3fd6a62724592cef037ef2ddf4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_drafts.draft_validation:promote_model_draft;
  contract-sha256:d63d34b716f1844389d85ced90f119888e9a5996ee070b429a1c68165a712c94
---

# promote_model_draft

## Signature

promote_model_draft(store: str | Path | None, model_name: str, pythonpath: str | None=None, actor: str | None=None, backfill: bool=False)

## Docstring

Validate the draft, install it, reindex, and bump the version.

With `backfill=True`, tracked documents missing a new field's default are re-rendered
under the new contract and each gets its own journal entry; the report lists them, so
nothing is rewritten without the caller asking for it. On reindex failure the active
model, the draft and the store indexes are put back.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.model_drafts.backfill", "sldb.api.model_drafts.draft_checks", "sldb.api.model_drafts.draft_loading", "sldb.api.model_drafts.draft_restore", "sldb.api.model_drafts.draft_validation_report", "sldb.api.model_drafts.model_source", "sldb.api.model_drafts.source_location", "sldb.api.model_registry.reindex_model", "sldb.api.schema.describe_field", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store.io", "sys"]

## Purpose

Validate the draft, install it, reindex, and bump the version.

## Architecture

Not documented.
