---
id: python-sldb-sldb-sldb-api-model_drafts-template_drafts-edit_model_template
system: sldb
module: sldb.sldb.api.model_drafts.template_drafts
qualname: edit_model_template
kind: FunctionDef
source_path: sldb/api/model_drafts/template_drafts.py
source_span: '15:35'
source_sha256: 2dc3dcd5ff106176457674fffaccc7fe75d9b3e5c31c4de27c62c5d3334bf448
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_drafts.template_drafts:edit_model_template;
  contract-sha256:124adb578e830e6b0dd0457d49d0fc953c3826823a55388cf1480bf997aade50
---

# edit_model_template

## Signature

edit_model_template(store: str | Path | None, model_name: str, template: str, pythonpath: str | None=None)

## Docstring

Write `template` as the draft template of a registered model.

Args:
    store: The store registering the model (path, alias, or None to discover it).
    model_name: Registered model name.
    template: The new template text; trailing newlines are dropped.
    pythonpath: Directory to import re-export modules from.

Returns:
    The draft holding the new template.

Raises:
    SLDBModelError: When the model is not registered.
    SLDBModelEditError: When the class or its `__template__` assignment is not found.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.model_drafts.model_draft", "sldb.api.model_drafts.model_source", "sldb.api.model_drafts.source_location", "sldb.api.model_drafts.template_literals", "sldb.api.stores.open_store"]

## Purpose

Not documented.

## Architecture

Not documented.
