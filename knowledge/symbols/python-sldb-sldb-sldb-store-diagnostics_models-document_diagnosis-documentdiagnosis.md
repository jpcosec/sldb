---
id: python-sldb-sldb-sldb-store-diagnostics_models-document_diagnosis-documentdiagnosis
system: sldb
module: sldb.sldb.store.diagnostics_models.document_diagnosis
qualname: DocumentDiagnosis
kind: ClassDef
source_path: sldb/store/diagnostics_models/document_diagnosis.py
source_span: 9:107
source_sha256: 495c8577669797ba3d5b4038632959a0e53fa36e35c6a2df01e728132f574758
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.diagnostics_models.document_diagnosis:DocumentDiagnosis;
  contract-sha256:31125f9f404939c3969a82574c4d0a565c9ad7300400ba341d338eaba3d08546
---

# DocumentDiagnosis

## Signature

Not applicable.

## Docstring

Diagnostic state for a single document.

The hashes are named for what they sign, not for their position in the chain
(`docs/versionado-y-colaboracion.md`):

- ``content`` — `hash_c`, SHA-256 of the markdown TEXT. Moves on any rewrite of
  the file, including one that changes nothing a model can read.
- ``fields`` — `hash_d`, SHA-256 of the EXTRACTED PAYLOAD under the model's
  contract. Moves only when a field's value actually changes.

That split is the whole basis of the verdict: text moving while fields hold
still is an expected mutation (reformatting, a trailing newline); fields moving
is a real change to the data.

The two sides of a comparison are named for WHERE they were read, not for which
is "right" — neither is authoritative alone. ``*_on_disk`` is recomputed from the
file now; ``*_in_index`` is what the store recorded at the last write. Which one
is stale is exactly what the caller is trying to find out.

The letter aliases (`hash_c_ok`, …) remain because the store's PERSISTED keys are
still `hash_c`/`hash_d`: renaming those would invalidate every store on disk.

## Imports

["__future__", "dataclasses", "sldb.store.diagnostics_models.diagnosis_note", "sldb.store.diagnostics_models.document_verdicts"]

## Purpose

Not documented.

## Architecture

Not documented.
