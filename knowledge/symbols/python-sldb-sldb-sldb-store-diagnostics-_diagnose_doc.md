---
id: python-sldb-sldb-sldb-store-diagnostics-_diagnose_doc
system: sldb
module: sldb.sldb.store.diagnostics
qualname: _diagnose_doc
kind: FunctionDef
source_path: sldb/store/diagnostics.py
source_span: '38:58'
source_sha256: 8df97842ce8ae42fe7bd7d412973d2a760e684bbcde8e00f0b22146d56f8bab7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.diagnostics:_diagnose_doc; contract-sha256:57101e99edc0c71c51e2b95633277f0ead4967251456dcadca76d977be7234d6
---

# _diagnose_doc

## Signature

_diagnose_doc(doc, root: Path, model_type: Any, contract_ok: bool=True)

## Docstring

Compare the document on disk against what the store recorded for it.

`content` is the markdown text; `fields` is the payload extracted under the
model's contract. Text moving while fields hold still is an expected mutation,
so the two are reported separately rather than as one "mismatch".

A model that cannot be imported here (`model_type` None) cannot re-extract the fields; an
intact text then stands for intact fields, instead of reading as a data mutation that sends
the operator to restore a file nobody touched. The model is named as unresolved.

## Imports

["__future__", "pathlib", "sldb.store.diagnostics_models", "sldb.store.diagnostics_models.text_history", "sldb.store.field_set_drift", "sldb.store.hashing", "sldb.store.io", "sldb.store.layout", "sldb.store.legacy_contract", "sldb.store.model_node", "sldb.store.model_origin", "sldb.store.models", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
