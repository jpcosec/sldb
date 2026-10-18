---
id: python-sldb-sldb-api-documents-rewrite_loss-rewrite_loss
system: sldb
module: sldb.api.documents.rewrite_loss
qualname: rewrite_loss
kind: FunctionDef
source_path: sldb/api/documents/rewrite_loss.py
source_span: '17:27'
source_sha256: 936c08fb605d4b09ab923c9e6ed51f25178bd66526dc1c9d71a99dc48c1aa2bd
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.rewrite_loss:rewrite_loss; contract-sha256:d26cfdd4843228e7dd2b7828b9c881a210910fa404922b9677f638cc4597d039
---

# rewrite_loss

## Signature

rewrite_loss(model_type: Any, markdown: str, payload: dict | None=None)

## Docstring

The source of each body block a rewrite would drop, in document order; [] when none
(or when the document does not extract at all: that is reported elsewhere). `payload` is
the document's extraction when the caller already has it.

## Imports

["__future__", "re", "typing"]

## Purpose

The source of each body block a rewrite would drop, in document order; [] when none (or when the document does not extract at all: that is reported elsewhere). `payload` is the document's extraction when the caller already has it.

## Architecture

Not documented.
