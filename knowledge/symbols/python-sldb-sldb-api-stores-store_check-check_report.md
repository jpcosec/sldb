---
id: python-sldb-sldb-api-stores-store_check-check_report
system: sldb
module: sldb.api.stores.store_check
qualname: check_report
kind: FunctionDef
source_path: sldb/api/stores/store_check.py
source_span: '46:54'
source_sha256: ae685aaf2819655d86bdc81c2ef092ed5403833ebacc062e01469191d3deeac5
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.stores.store_check:check_report; contract-sha256:ee80a6c00b5d25670aba7687d77dc734458d5f9e3b29863d930fc8cbde21b2a6
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

The compact `{ok, valid, damaged, ..., checked, mismatched, structural_noise}` view of one diagnosis.

## Architecture

Not documented.
