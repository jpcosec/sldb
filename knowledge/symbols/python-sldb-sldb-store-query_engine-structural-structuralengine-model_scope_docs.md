---
id: python-sldb-sldb-store-query_engine-structural-structuralengine-model_scope_docs
system: sldb
module: sldb.store.query_engine.structural
qualname: StructuralEngine.model_scope_docs
kind: FunctionDef
source_path: sldb/store/query_engine/structural.py
source_span: '26:35'
source_sha256: 31245e018b0342ac6d01f2ab18a93752e26e28faea8b9379bf2021ebcfd4d5d9
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.query_engine.structural:StructuralEngine.model_scope_docs;
  contract-sha256:91dafc672b35c570d6b303956c76fda7f5bb426b0946eb062dcece001f5555c8
---

# StructuralEngine.model_scope_docs

## Signature

model_scope_docs(cls, store_path: Path, scope: str, recursive: bool, resolve_model_ref, pythonpath: str | None=None, store: str | None=None)

## Docstring

Documents in scope `{Model}` (exact model) or `{Model+}` (the model and every
subclass), of the local store or of the linked store named `store`. The family
check walks each document's model MRO by class name, so a base that is not itself
registered (an abstract `PrimitiveDoc`) still names a family.

## Imports

["__future__", "pathlib", "re", "sldb.store.io", "typing"]

## Purpose

Documents in scope `{Model}` (exact model) or `{Model+}` (the model and every subclass), of the local store or of the linked store named `store`. The family check walks each document's model MRO by class name, so a base that is not itself registered (an abstract `PrimitiveDoc`) still names a family.

## Architecture

Not documented.
