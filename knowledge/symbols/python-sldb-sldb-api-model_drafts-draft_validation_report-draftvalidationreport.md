---
id: python-sldb-sldb-api-model_drafts-draft_validation_report-draftvalidationreport
system: sldb
module: sldb.api.model_drafts.draft_validation_report
qualname: DraftValidationReport
kind: ClassDef
source_path: sldb/api/model_drafts/draft_validation_report.py
source_span: '12:26'
source_sha256: 3e5666da3ead23f8ef62386dc50cefe188b52f37351ab56c6e24cc25af4bd8b2
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_drafts.draft_validation_report:DraftValidationReport;
  contract-sha256:fc93bf6e36f34237e6eb9f91db446830d385480f7d81cb2110fa645da5521d34
---

# DraftValidationReport

## Signature

Not applicable.

## Docstring

What was validated, against which documents, and whether it was installed.

A draft that fails validation raises instead of producing a report, so `valid` is
always True; it is kept so the report reads like `sldb models validate --format json`.

## Imports

["__future__", "pathlib", "pydantic", "sldb.api.model_drafts.draft_document_check"]

## Purpose

Not documented.

## Architecture

Not documented.
