---
id: python-sldb-sldb-store-diagnostics_models-store_diagnosis-storediagnosis-is_valid
system: sldb
module: sldb.store.diagnostics_models.store_diagnosis
qualname: StoreDiagnosis.is_valid
kind: FunctionDef
source_path: sldb/store/diagnostics_models/store_diagnosis.py
source_span: '46:54'
source_sha256: b1c227d5fcfcdbdf563ce0d37904a50b43d97653eca621a5cee5984b67969f98
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.diagnostics_models.store_diagnosis:StoreDiagnosis.is_valid;
  contract-sha256:93c1830bbd4206a305b682f8aa8da6ac06ce0e2ccd2e555ca15288524f72f302
---

# StoreDiagnosis.is_valid

## Signature

is_valid(self)

## Docstring

Whether the store is in a valid state.

A reformatted document (text moved, fields identical) is still valid, a damaged one is
not, and a disagreeing roster or root hash is not. A moved contract is not valid either:
the indexed payloads were extracted under a contract that no longer holds. Classifying
a failure is not the same as tolerating it.

## Imports

["__future__", "dataclasses", "sldb.store.diagnostics_models.diagnosis_note", "sldb.store.diagnostics_models.model_diagnosis"]

## Purpose

Whether the store is in a valid state.

## Architecture

Not documented.
