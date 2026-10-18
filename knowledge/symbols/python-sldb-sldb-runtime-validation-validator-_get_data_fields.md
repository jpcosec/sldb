---
id: python-sldb-sldb-runtime-validation-validator-_get_data_fields
system: sldb
module: sldb.runtime.validation
qualname: Validator._get_data_fields
kind: FunctionDef
source_path: sldb/runtime/validation.py
source_span: '29:45'
source_sha256: 2b2918b574091442a8d3d9b4cbf95a30da6261a2050927062ccc86077dec60bb
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.runtime.validation:Validator._get_data_fields;
  contract-sha256:9d380067a679fb871eaf0907654a139e7faafb1a64557a140ee3de7751e41f29
---

# Validator._get_data_fields

## Signature

_get_data_fields(self)

## Docstring

The fields that must roundtrip: `rev` always, `optrev` when present.

`render`/`py` markers are display-only and stay out. The contract for
`optrev` ("if present, it should still extract and render symmetrically")
is what this set enforces: validate used to collect `rev` only, so an
`optrev` field could lose its content and still report PASS.

## Imports

["__future__", "functools", "pathlib", "sldb.core.ast", "sldb.core.data_extractor", "sldb.core.renderer", "sldb.core.template_extractor", "sldb.models.structured_doc", "typing"]

## Purpose

The fields that must roundtrip: `rev` always, `optrev` when present.

## Architecture

Not documented.
