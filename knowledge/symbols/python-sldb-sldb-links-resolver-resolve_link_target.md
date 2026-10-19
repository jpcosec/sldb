---
id: python-sldb-sldb-links-resolver-resolve_link_target
system: sldb
module: sldb.links.resolver
qualname: resolve_link_target
kind: FunctionDef
source_path: sldb/links/resolver.py
source_span: '24:30'
source_sha256: a85168b7c7ee58118d6f2f0f6908065cd44f60092ceff34c051fc0f73c6d2379
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.links.resolver:resolve_link_target; contract-sha256:22528f128a0f8a2dd9eba49baf329bf43b59d6063411801ddadccb6d93e75943
---

# resolve_link_target

## Signature

resolve_link_target(tgt: str, cur_doc: Path, store_path: Path | None, predicate: str | None=None, w5h1_type: str | None=None)

## Docstring

Resolve `doc` or `doc#Section`; the section itself is checked by recovery/compose.

## Imports

[".resolved_link", ".sections", "__future__", "pathlib", "sldb.store.io", "sldb.store.layout"]

## Purpose

Resolve `doc` or `doc#Section`; the section itself is checked by recovery/compose.

## Architecture

Not documented.
