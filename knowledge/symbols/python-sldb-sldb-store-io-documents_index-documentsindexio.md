---
id: python-sldb-sldb-store-io-documents_index-documentsindexio
system: sldb
module: sldb.store.io.documents_index
qualname: DocumentsIndexIO
kind: ClassDef
source_path: sldb/store/io/documents_index.py
source_span: '28:56'
source_sha256: 8aa37bb0441e9cb89b92e28cc541512f833104dc7c976ee3f717260f27108a71
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.io.documents_index:DocumentsIndexIO; contract-sha256:6300d7325445e8f35c3b011e49b1ed7c7a1de260702158449566027f11a857da
---

# DocumentsIndexIO

## Signature

Not applicable.

## Docstring

`path` is `<store>/core/documents/<model>.yaml` — no longer written to (PLAN 15 capa
7), still the key every caller already has: the stem is the model name, enough to find
or make `<store>/core/documents/<model>/`.

## Imports

["contextlib", "fcntl", "os", "pathlib", "sldb.store.io.utils", "sldb.store.layout", "sldb.store.models", "tempfile", "yaml"]

## Purpose

`path` is `<store>/core/documents/<model>.yaml` — no longer written to (PLAN 15 capa 7), still the key every caller already has: the stem is the model name, enough to find or make `<store>/core/documents/<model>/`.

## Architecture

Not documented.
