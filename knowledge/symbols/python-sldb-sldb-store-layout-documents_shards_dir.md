---
id: python-sldb-sldb-store-layout-documents_shards_dir
system: sldb
module: sldb.store.layout
qualname: documents_shards_dir
kind: FunctionDef
source_path: sldb/store/layout.py
source_span: 119:122
source_sha256: 5426bd05eb9d838ff5b7575a37c92ebc23b4da123ed19302fe13e0158dd44cdf
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.layout:documents_shards_dir; contract-sha256:c34f3de60c2835cd24860bbb796e0d625cf3ea7931857aee5fac25d5424e1be4
---

# documents_shards_dir

## Signature

documents_shards_dir(store_path: Path, model_name: str)

## Docstring

One document's index entry per file (PLAN 15 capa 7) — the Merkle tree's own leaf
level, next to the (now legacy-shaped, still used as a key) per-model documents_index.

## Imports

["__future__", "pathlib"]

## Purpose

One document's index entry per file (PLAN 15 capa 7) — the Merkle tree's own leaf level, next to the (now legacy-shaped, still used as a key) per-model documents_index.

## Architecture

Not documented.
