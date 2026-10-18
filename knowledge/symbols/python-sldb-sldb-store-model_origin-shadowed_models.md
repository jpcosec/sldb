---
id: python-sldb-sldb-store-model_origin-shadowed_models
system: sldb
module: sldb.store.model_origin
qualname: shadowed_models
kind: FunctionDef
source_path: sldb/store/model_origin.py
source_span: 61:71
source_sha256: 50c763d3d5219d878aa05edd93543ec59204335bd82b37fa28b50be71676f29e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.model_origin:shadowed_models; contract-sha256:9b23e6a4fc001d74dad6f1783e75b4918b75b0284a7a1c1578a28e4d439e76bb
---

# shadowed_models

## Signature

shadowed_models(store_path: Path, same_class=lambda a, b: a == b)

## Docstring

Models this store owns under a name a linked store also owns.

The graph has one node per model name, so two classes behind one name merge there. A
copy (the same class, compared by `same_class`; by reference string unless the caller can
import) can become inherited; a different class is an override that
should extend the owner's under a name of its own. Reported, never refused; sldb's own
models are left out.

## Imports

["__future__", "pathlib", "sldb.store.io", "sldb.store.layout", "sys", "typing"]

## Purpose

Models this store owns under a name a linked store also owns.

## Architecture

Not documented.
