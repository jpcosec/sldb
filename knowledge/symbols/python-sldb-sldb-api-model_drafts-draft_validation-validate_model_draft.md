---
id: python-sldb-sldb-api-model_drafts-draft_validation-validate_model_draft
system: sldb
module: sldb.api.model_drafts.draft_validation
qualname: validate_model_draft
kind: FunctionDef
source_path: sldb/api/model_drafts/draft_validation.py
source_span: '23:33'
source_sha256: d049ed57d4c2347b4f75bee2034d88b861928f3fd6a62724592cef037ef2ddf4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_drafts.draft_validation:validate_model_draft;
  contract-sha256:d3b751868a6cfb81d71ec945b03b73fc2bfed192d8051e7698a71ec4119840ed
---

# validate_model_draft

## Signature

validate_model_draft(store: str | Path | None, model_name: str, pythonpath: str | None=None)

## Docstring

Check the draft (or the active model when there is no draft) without installing it.

The report's `backfill` names the tracked documents a backfill promote would rewrite.

Raises:
    SLDBModelError: When the model is not registered.
    SLDBModelEditError: When the template references unknown fields or the draft is broken.
    SLDBValidationError: When a tracked document does not round-trip under the contract.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.model_drafts.backfill", "sldb.api.model_drafts.draft_checks", "sldb.api.model_drafts.draft_loading", "sldb.api.model_drafts.draft_restore", "sldb.api.model_drafts.draft_validation_report", "sldb.api.model_drafts.model_source", "sldb.api.model_drafts.source_location", "sldb.api.model_registry.reindex_model", "sldb.api.schema.describe_field", "sldb.api.stores.open_store", "sldb.core.exceptions", "sldb.store.io", "sys"]

## Purpose

Not documented.

## Architecture

Not documented.
