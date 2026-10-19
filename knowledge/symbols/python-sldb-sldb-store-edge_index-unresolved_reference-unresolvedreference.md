---
id: python-sldb-sldb-store-edge_index-unresolved_reference-unresolvedreference
system: sldb
module: sldb.store.edge_index.unresolved_reference
qualname: UnresolvedReference
kind: ClassDef
source_path: sldb/store/edge_index/unresolved_reference.py
source_span: '10:25'
source_sha256: 7cd78e09b87e460444c845a492e9cb20cf4429be9edc30ec808378cc97a6c2d3
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.edge_index.unresolved_reference:UnresolvedReference;
  contract-sha256:dfdd87df548a240a997e36852cb47b36a81baefa8425799a758f4676c1b61fc1
---

# UnresolvedReference

## Signature

Not applicable.

## Docstring

One value of a declared reference or containment field that resolves to no document.

A normal condition a caller inspects, kept apart from `EdgeIndex.problems` (which fails
authored edges). Only fields the model declared appear: a free `__references__` field
reports its unqualified values only when they look like a path.

## Imports

["__future__", "pydantic", "typing"]

## Purpose

One value of a declared reference or containment field that resolves to no document.

## Architecture

Not documented.
