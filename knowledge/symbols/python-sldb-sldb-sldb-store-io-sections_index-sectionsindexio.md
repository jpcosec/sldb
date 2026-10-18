---
id: python-sldb-sldb-sldb-store-io-sections_index-sectionsindexio
system: sldb
module: sldb.sldb.store.io.sections_index
qualname: SectionsIndexIO
kind: ClassDef
source_path: sldb/store/io/sections_index.py
source_span: '28:55'
source_sha256: 017cba80c8f30b34e2a7d70dbefc806218653a5e99f49f9576d7ca3ca2b3b73d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.io.sections_index:SectionsIndexIO; contract-sha256:55416371436424fb5dbf5d326b472c253d69d8b41599c9a4ff3ebeec4c01a045
---

# SectionsIndexIO

## Signature

Not applicable.

## Docstring

`path` is `<store>/runtime/sections/<model>.yaml` — no longer written to (PLAN 15 capa
5), still the key every caller already has: three parents up is the store, the stem is
the model name, and that is enough to find or make `<store>/runtime/sections/<model>/`.

## Imports

["contextlib", "fcntl", "os", "pathlib", "sldb.store.io.utils", "sldb.store.layout", "sldb.store.models", "tempfile", "yaml"]

## Purpose

Not documented.

## Architecture

Not documented.
