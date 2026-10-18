---
id: python-sldb-sldb-sldb-store-io-documents_index-documentsindexio
system: sldb
module: sldb.sldb.store.io.documents_index
qualname: DocumentsIndexIO
kind: ClassDef
source_path: sldb/store/io/documents_index.py
source_span: '28:56'
source_sha256: 8aa37bb0441e9cb89b92e28cc541512f833104dc7c976ee3f717260f27108a71
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.io.documents_index:DocumentsIndexIO;
  contract-sha256:1ef38d5ba75b49288d31e26f654522ab4272ea654433a26ea6ed26cf20ba3da0
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

Not documented.

## Architecture

Not documented.
