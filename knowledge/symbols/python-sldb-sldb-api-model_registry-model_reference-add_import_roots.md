---
id: python-sldb-sldb-api-model_registry-model_reference-add_import_roots
system: sldb
module: sldb.api.model_registry.model_reference
qualname: add_import_roots
kind: FunctionDef
source_path: sldb/api/model_registry/model_reference.py
source_span: '27:32'
source_sha256: 0625ce8c4bde65eac0438f8ffc40cef6c63d88666e334386598ca12b89707406
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_registry.model_reference:add_import_roots;
  contract-sha256:1141725357d544bb1cb9d37ce569e504770c84f9916d72a0814de9afca950743
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

Put each project root on `sys.path`, once each, so an inherited model imports from the repo that owns it without a `--pythonpath`. A path given explicitly still goes in front.

## Architecture

Not documented.
