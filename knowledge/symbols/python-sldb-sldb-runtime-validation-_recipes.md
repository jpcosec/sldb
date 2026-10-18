---
id: python-sldb-sldb-runtime-validation-_recipes
system: sldb
module: sldb.runtime.validation
qualname: _recipes
kind: FunctionDef
source_path: sldb/runtime/validation.py
source_span: 60:63
source_sha256: 2b2918b574091442a8d3d9b4cbf95a30da6261a2050927062ccc86077dec60bb
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.runtime.validation:_recipes; contract-sha256:5959a813ccce7e92179fbdf40347465a6f94a6f528d2429870c610d1582a18c1
---

# _recipes

## Signature

_recipes(template: str)

## Docstring

A template's extraction recipes: the template is stable per model, so it is split once
(it used to be re-parsed on every extract and every validate).

## Imports

["__future__", "functools", "pathlib", "sldb.core.ast", "sldb.core.data_extractor", "sldb.core.renderer", "sldb.core.template_extractor", "sldb.models.structured_doc", "typing"]

## Purpose

A template's extraction recipes: the template is stable per model, so it is split once (it used to be re-parsed on every extract and every validate).

## Architecture

Not documented.
