---
id: python-sldb-sldb-store-diagnostics_models-document_diagnosis-documentdiagnosis-needs_decision
system: sldb
module: sldb.store.diagnostics_models.document_diagnosis
qualname: DocumentDiagnosis.needs_decision
kind: FunctionDef
source_path: sldb/store/diagnostics_models/document_diagnosis.py
source_span: 88:94
source_sha256: 495c8577669797ba3d5b4038632959a0e53fa36e35c6a2df01e728132f574758
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.diagnostics_models.document_diagnosis:DocumentDiagnosis.needs_decision;
  contract-sha256:20841ca8768945afbfe19fe43986713639d5a961e2d297220242aec232224978
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

Whether a human must look before anything is run.

## Architecture

Not documented.
