---
id: python-sldb-sldb-api-edges-builtin_relation_writes-write_builtin_relation_types
system: sldb
module: sldb.api.edges.builtin_relation_writes
qualname: write_builtin_relation_types
kind: FunctionDef
source_path: sldb/api/edges/builtin_relation_writes.py
source_span: '20:30'
source_sha256: dac7dd73866d52ed3012baf66f64df8b7bf2a7d369493aa94bc72ff68a86adf1
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.edges.builtin_relation_writes:write_builtin_relation_types;
  contract-sha256:88bdb2c7024c31939a56c155eceee75f3bf051268c79ceef6a61295adfa6218e
---

# write_builtin_relation_types

## Signature

write_builtin_relation_types(sp: Path, root: Path, pythonpath: str | None, report: RelationsInitReport)

## Docstring

One RelationTypeDoc per builtin relation that is not tracked yet, under `sldb/relation_types/`.

## Imports

["__future__", "pathlib", "sldb.api.edges.relations_init_report", "sldb.api.model_registry.load_registered_model", "sldb.api.model_registry.model_reference", "sldb.models.builtin_relation_types", "sldb.runtime.validation", "sldb.store", "sldb.store.io", "sldb.store.models", "sldb.store.ops"]

## Purpose

One RelationTypeDoc per builtin relation that is not tracked yet, under `sldb/relation_types/`.

## Architecture

Not documented.
