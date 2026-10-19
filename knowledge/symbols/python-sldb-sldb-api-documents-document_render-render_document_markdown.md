---
id: python-sldb-sldb-api-documents-document_render-render_document_markdown
system: sldb
module: sldb.api.documents.document_render
qualname: render_document_markdown
kind: FunctionDef
source_path: sldb/api/documents/document_render.py
source_span: '19:28'
source_sha256: 9017518f2ae636d52fd18fa979d39d9181cf499071bc2a7332e44836dabf18b3
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.documents.document_render:render_document_markdown;
  contract-sha256:6dd1a5b0f76e32726f36d74d0728d2330ed6ac546e8df80fdf0bd1fd108f104e
---

# render_document_markdown

## Signature

render_document_markdown(store_path: Path, pythonpath: str | None, doc_ref: str)

## Docstring

The document rendered from its template, via the CLI's renderer.

Composition refs resolve against the project root, never the process CWD: a tracked
document composes the same from any directory, which is what a server needs.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_payload", "sldb.api.model_registry.load_registered_model", "sldb.store.layout", "typing"]

## Purpose

The document rendered from its template, via the CLI's renderer.

## Architecture

Not documented.
