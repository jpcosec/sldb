---
id: python-sldb-sldb-sldb-api-model_drafts-field_drafts-remove_model_field
system: sldb
module: sldb.sldb.api.model_drafts.field_drafts
qualname: remove_model_field
kind: FunctionDef
source_path: sldb/api/model_drafts/field_drafts.py
source_span: 63:85
source_sha256: d09a980b400a4bfe3fc53d9a19eb8132fad4a902c4c4d491c706988772b70040
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_drafts.field_drafts:remove_model_field;
  contract-sha256:c5fb28c2dd12f0cbad89cdfbe8d3c167b45863090b3ca56b5014f7ebb08a37b1
---

# remove_model_field

## Signature

remove_model_field(store: str | Path | None, model_name: str, field_name: str, pythonpath: str | None=None)

## Docstring

Remove a field's declaration and template section from the model's draft.

Args:
    store: The store registering the model (path, alias, or None to discover it).
    model_name: Registered model name.
    field_name: Name of the field to remove.
    pythonpath: Directory to import re-export modules from.

Returns:
    The draft the field was removed from.

Raises:
    SLDBModelError: When the model is not registered.
    SLDBModelEditError: When the class is not found or does not declare the field.

## Imports

["__future__", "pathlib", "sldb.api.documents.data_values", "sldb.api.journal", "sldb.api.model_drafts.field_blocks", "sldb.api.model_drafts.model_draft", "sldb.api.model_drafts.source_location", "sldb.api.model_drafts.template_literals", "sldb.api.model_drafts.template_sections", "sldb.api.model_registry.load_registered_model", "sldb.api.stores.open_store"]

## Purpose

Not documented.

## Architecture

Not documented.
