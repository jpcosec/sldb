---
id: python-sldb-sldb-sldb-store-diagnostics_models-model_diagnosis-modeldiagnosis-roster_only_failure
system: sldb
module: sldb.sldb.store.diagnostics_models.model_diagnosis
qualname: ModelDiagnosis.roster_only_failure
kind: FunctionDef
source_path: sldb/store/diagnostics_models/model_diagnosis.py
source_span: 60:70
source_sha256: e67122e7080feac6559fd9d0c2c921e4f1badeb274ae2e9f4ae2f870397b2947
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.diagnostics_models.model_diagnosis:ModelDiagnosis.roster_only_failure;
  contract-sha256:e9fc788a7158f9bd8e77cb8e50b1c723c674b867b1824796d8576c8336182ed2
---

# ModelDiagnosis.roster_only_failure

## Signature

roster_only_failure(self)

## Docstring

The roster hash disagrees, yet no document present is damaged.

The signature of a document list that is INCOMPLETE rather than corrupt: the
documents the index signed are not all here to be summed. Common cause is a
deliberately unversioned family (a ledger whose documents are gitignored),
where a clean clone has an index counting documents it was never meant to
contain. Nothing is damaged, and no per-document verdict can show it because
the absent documents have no verdict at all.

## Imports

["__future__", "dataclasses", "sldb.store.diagnostics_models.diagnosis_note", "sldb.store.diagnostics_models.document_diagnosis"]

## Purpose

Not documented.

## Architecture

Not documented.
