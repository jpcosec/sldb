---
id: python-sldb-sldb-sldb-store-diagnostics_models-document_diagnosis-documentdiagnosis-needs_decision
system: sldb
module: sldb.sldb.store.diagnostics_models.document_diagnosis
qualname: DocumentDiagnosis.needs_decision
kind: FunctionDef
source_path: sldb/store/diagnostics_models/document_diagnosis.py
source_span: 88:94
source_sha256: 495c8577669797ba3d5b4038632959a0e53fa36e35c6a2df01e728132f574758
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.diagnostics_models.document_diagnosis:DocumentDiagnosis.needs_decision;
  contract-sha256:ab6895be5f553ef2414dbaece0cb36899a295b24e014cba6d26b6729ad5dc142
---

# DocumentDiagnosis.needs_decision

## Signature

needs_decision(self)

## Docstring

Whether a human must look before anything is run.

A field value that changed, or a document that vanished, is not something a command
should paper over: the index is the only record of what the value used to be.

## Imports

["__future__", "dataclasses", "sldb.store.diagnostics_models.diagnosis_note", "sldb.store.diagnostics_models.document_verdicts"]

## Purpose

Not documented.

## Architecture

Not documented.
