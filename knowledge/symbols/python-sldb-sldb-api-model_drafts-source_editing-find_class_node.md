---
id: python-sldb-sldb-api-model_drafts-source_editing-find_class_node
system: sldb
module: sldb.api.model_drafts.source_editing
qualname: find_class_node
kind: FunctionDef
source_path: sldb/api/model_drafts/source_editing.py
source_span: '14:23'
source_sha256: 970a724d107da69babfdd4dd34a03e90a01b2d7cc18932a84750f5f6487c14e8
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_drafts.source_editing:find_class_node;
  contract-sha256:82bfc63d31d647d54c318971917a72c5882fe8aa59790e81f26daecbffdfefa4
---

# find_class_node

## Signature

find_class_node(tree: ast.Module, class_name: str, path: Path)

## Docstring

The top-level class statement named `class_name`.

Raises:
    SLDBModelEditError: When the module defines no such class.

## Imports

["__future__", "ast", "pathlib", "sldb.core.exceptions"]

## Purpose

The top-level class statement named `class_name`.

## Architecture

Not documented.
