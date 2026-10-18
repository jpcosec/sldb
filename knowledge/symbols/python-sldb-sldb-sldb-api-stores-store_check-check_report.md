---
id: python-sldb-sldb-sldb-api-stores-store_check-check_report
system: sldb
module: sldb.sldb.api.stores.store_check
qualname: check_report
kind: FunctionDef
source_path: sldb/api/stores/store_check.py
source_span: '46:54'
source_sha256: ae685aaf2819655d86bdc81c2ef092ed5403833ebacc062e01469191d3deeac5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.store_check:check_report; contract-sha256:46db7d572edbae1fd02fdaca84c8afa225e08c8a0a4911db35a7fa11443c3ff5
---

# check_report

## Signature

check_report(diagnosis: Any, noise: list[dict[str, Any]])

## Docstring

The compact `{ok, valid, damaged, ..., checked, mismatched, structural_noise}` view of one diagnosis.

Args:
    diagnosis: The store diagnosis to project.
    noise: The tracked documents with undeclared headings (see ``structural_noise``).

## Imports

["__future__", "pathlib", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
