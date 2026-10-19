---
id: python-sldb-sldb-selfdoc-materialize-plan_documents
system: sldb
module: sldb.selfdoc.materialize
qualname: plan_documents
kind: FunctionDef
source_path: sldb/selfdoc/materialize.py
source_span: '13:24'
source_sha256: 9336c3677a6d9ee7e32907ba985b10a5fc52c8143411a12ebdf9489b5b753d7a
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.selfdoc.materialize:plan_documents; contract-sha256:9f56881fad93da77a8ad1d37f8f1a85c74e9c84fe6f5391613325b6a65539529
---

# plan_documents

## Signature

plan_documents(records: list[CommandRecord], system: str, factory: str, output: Path)

## Docstring

Prepare every file before sync writes any of them.

## Imports

[".command", ".planned_document", ".projection", "__future__", "pathlib", "re", "sldb.models.knowledge_surface", "sldb.runtime.validation"]

## Purpose

Prepare every file before sync writes any of them.

## Architecture

Not documented.
