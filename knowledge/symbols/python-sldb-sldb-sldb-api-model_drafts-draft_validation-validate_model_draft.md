---
id: python-sldb-sldb-sldb-api-model_drafts-draft_validation-validate_model_draft
system: sldb
module: sldb.sldb.api.model_drafts.draft_validation
qualname: validate_model_draft
kind: FunctionDef
source_path: sldb/api/model_drafts/draft_validation.py
source_span: '23:33'
source_sha256: d049ed57d4c2347b4f75bee2034d88b861928f3fd6a62724592cef037ef2ddf4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_drafts.draft_validation:validate_model_draft;
  contract-sha256:a415f73a3ecd8681c7422d6badb242f27b82d871a6d268ad9c9d1da351ee333b
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
