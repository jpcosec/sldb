---
id: python-sldb-sldb-store-diagnostics_models-model_diagnosis-modeldiagnosis
system: sldb
module: sldb.store.diagnostics_models.model_diagnosis
qualname: ModelDiagnosis
kind: ClassDef
source_path: sldb/store/diagnostics_models/model_diagnosis.py
source_span: 32:88
source_sha256: e67122e7080feac6559fd9d0c2c921e4f1badeb274ae2e9f4ae2f870397b2947
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.diagnostics_models.model_diagnosis:ModelDiagnosis;
  contract-sha256:b15c27ad6c36086721a51c6ead1471e5a5da72fb6b53527ec3bfef3a1c71c17e
---

# ModelDiagnosis

## Signature

Not applicable.

## Docstring

Diagnostic state for a model and its documents.

``roster_ok`` is `hash_b`: the model's index signs `[{name, hash_c, hash_d}]`
over its whole document list, so it moves when any document is written AND when
a document joins or leaves the roster. It is a statement about the LIST, which is
why it can fail while every document present is individually fine.

## Imports

["__future__", "dataclasses", "sldb.store.diagnostics_models.diagnosis_note", "sldb.store.diagnostics_models.document_diagnosis"]

## Purpose

Not documented.

## Architecture

Not documented.
