---
id: python-sldb-sldb-store-diagnostics_models-store_diagnosis-storediagnosis
system: sldb
module: sldb.store.diagnostics_models.store_diagnosis
qualname: StoreDiagnosis
kind: ClassDef
source_path: sldb/store/diagnostics_models/store_diagnosis.py
source_span: 10:67
source_sha256: b1c227d5fcfcdbdf563ce0d37904a50b43d97653eca621a5cee5984b67969f98
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.diagnostics_models.store_diagnosis:StoreDiagnosis;
  contract-sha256:4ba5625addecac5b46378b9d830ce075152acf5d5900709657e754f18ac49429
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

Full diagnostic state for the entire store.

## Architecture

Not documented.
