---
id: python-sldb-sldb-api-model_drafts-draft_validation-_install_draft
system: sldb
module: sldb.api.model_drafts.draft_validation
qualname: _install_draft
kind: FunctionDef
source_path: sldb/api/model_drafts/draft_validation.py
source_span: 62:72
source_sha256: d049ed57d4c2347b4f75bee2034d88b861928f3fd6a62724592cef037ef2ddf4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_drafts.draft_validation:_install_draft;
  contract-sha256:d2848e2236c85fe3dfb5407afce0ff5c05ea016c8ea28e34785c9a5f654c690d
---

# _install_draft

## Signature

_install_draft(store: str | Path | None, model_name: str, source: ModelSource, new_type: type, plan: list[BackfillDoc], pythonpath: str | None, actor: str | None, backfill: bool)

## Docstring

Install the draft, backfill if asked, reindex, and drop the draft; returns the version.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.model_drafts.backfill", "sldb.api.model_drafts.draft_checks", "sldb.api.model_drafts.draft_loading", "sldb.api.model_drafts.draft_restore", "sldb.api.model_drafts.draft_validation_report", "sldb.api.model_drafts.model_source", "sldb.api.model_drafts.source_location", "sldb.api.model_registry.reindex_model", "sldb.api.schema.describe_field", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store.io", "sys"]

## Purpose

Not documented.

## Architecture

Not documented.
