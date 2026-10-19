---
id: python-sldb-sldb-api-edges-builtin_relation_writes-_refresh_outdated
system: sldb
module: sldb.api.edges.builtin_relation_writes
qualname: _refresh_outdated
kind: FunctionDef
source_path: sldb/api/edges/builtin_relation_writes.py
source_span: '43:55'
source_sha256: dac7dd73866d52ed3012baf66f64df8b7bf2a7d369493aa94bc72ff68a86adf1
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.edges.builtin_relation_writes:_refresh_outdated;
  contract-sha256:efca33b6a8b1f975fa8085c9fe2605ba04c3a2aeefae6a4b0804485f60b7373a
---

# _refresh_outdated

## Signature

_refresh_outdated(root: Path, model_type, tracked: dict[str, str], report: RelationsInitReport)

## Docstring

Rewrite a tracked builtin whose spec moved (`has_model` became many-to-many when stores
began sharing models): the index produces those edges, so sldb owns their type. Compared
on the payload, so a builtin that only reads differently is left alone.

## Imports

["__future__", "pathlib", "sldb.api.edges.relations_init_report", "sldb.api.model_registry.load_registered_model", "sldb.api.model_registry.model_reference", "sldb.models.builtin_relation_types", "sldb.runtime.validation", "sldb.store", "sldb.store.io", "sldb.store.models", "sldb.store.ops"]

## Purpose

Rewrite a tracked builtin whose spec moved (`has_model` became many-to-many when stores began sharing models): the index produces those edges, so sldb owns their type. Compared on the payload, so a builtin that only reads differently is left alone.

## Architecture

Not documented.
