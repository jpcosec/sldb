---
id: python-sldb-sldb-sldb-api-model_registry-model_reference-add_import_roots
system: sldb
module: sldb.sldb.api.model_registry.model_reference
qualname: add_import_roots
kind: FunctionDef
source_path: sldb/api/model_registry/model_reference.py
source_span: '27:32'
source_sha256: 0625ce8c4bde65eac0438f8ffc40cef6c63d88666e334386598ca12b89707406
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_registry.model_reference:add_import_roots;
  contract-sha256:bbf2cd56cca819f9cdb35deac9547b175d21aca35eedb717028b680a8ad2cc4b
---

# add_import_roots

## Signature

add_import_roots(roots: list[Path])

## Docstring

Put each project root on `sys.path`, once each, so an inherited model imports from the
repo that owns it without a `--pythonpath`. A path given explicitly still goes in front.

## Imports

["__future__", "importlib", "pathlib", "sldb.core.exceptions", "sldb.models.structured_doc", "sys", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
