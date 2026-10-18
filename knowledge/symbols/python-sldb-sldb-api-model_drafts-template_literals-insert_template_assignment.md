---
id: python-sldb-sldb-api-model_drafts-template_literals-insert_template_assignment
system: sldb
module: sldb.api.model_drafts.template_literals
qualname: insert_template_assignment
kind: FunctionDef
source_path: sldb/api/model_drafts/template_literals.py
source_span: '39:55'
source_sha256: 10b3c690b8c11dead5617206fdad32e953e15b13a2e5a1618d861df3285e9a8d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_drafts.template_literals:insert_template_assignment;
  contract-sha256:2e8ecc6c04ae781f63a9e81309af57b3afaad1b3f07d54b24a166c07de4ad880
---

# insert_template_assignment

## Signature

insert_template_assignment(path: Path, class_name: str, template: str)

## Docstring

The source of `path` with class `class_name` declaring its own `__template__`.

The new assignment is inserted at the top of the class body, after a docstring when
one leads the class, so the class stops inheriting its template.

Raises:
    SLDBModelEditError: When the class is missing.

## Imports

["__future__", "ast", "pathlib", "sldb.api.model_drafts.source_editing", "sldb.core.exceptions"]

## Purpose

Not documented.

## Architecture

Not documented.
