---
id: python-sldb-sldb-sldb-store-diagnostics_models-store_diagnosis-storediagnosis
system: sldb
module: sldb.sldb.store.diagnostics_models.store_diagnosis
qualname: StoreDiagnosis
kind: ClassDef
source_path: sldb/store/diagnostics_models/store_diagnosis.py
source_span: 10:67
source_sha256: b1c227d5fcfcdbdf563ce0d37904a50b43d97653eca621a5cee5984b67969f98
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.diagnostics_models.store_diagnosis:StoreDiagnosis;
  contract-sha256:d24c949bf72f9211609f7bfdb24aa675050e1bd66ec0e552ac9e0d228e0bb069
---

# StoreDiagnosis

## Signature

Not applicable.

## Docstring

Full diagnostic state for the entire store.

``root_ok`` is `hash_a`: the store index signs `[{name, hash_b}]` over every
registered model, so it is the Merkle root of the whole store.

## Imports

["__future__", "dataclasses", "sldb.store.diagnostics_models.diagnosis_note", "sldb.store.diagnostics_models.model_diagnosis"]

## Purpose

Not documented.

## Architecture

Not documented.
