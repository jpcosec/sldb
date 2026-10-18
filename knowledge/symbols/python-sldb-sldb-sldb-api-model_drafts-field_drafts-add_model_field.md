---
id: python-sldb-sldb-sldb-api-model_drafts-field_drafts-add_model_field
system: sldb
module: sldb.sldb.api.model_drafts.field_drafts
qualname: add_model_field
kind: FunctionDef
source_path: sldb/api/model_drafts/field_drafts.py
source_span: 32:60
source_sha256: d09a980b400a4bfe3fc53d9a19eb8132fad4a902c4c4d491c706988772b70040
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_drafts.field_drafts:add_model_field;
  contract-sha256:b2cd47c9ff47962309f693fcc9902721ce7e14d5e84f8f76331040416c729785
---

# add_model_field

## Signature

add_model_field(store: str | Path | None, model_name: str, field_name: str, field_type: str='str', description: str='', default: str | None=None, pythonpath: str | None=None)

## Docstring

Declare a new field in the model's draft, plus its template section.

Args:
    store: The store registering the model (path, alias, or None to discover it).
    model_name: Registered model name.
    field_name: Name of the new field.
    field_type: Python annotation of the field, as source text (e.g. `int`, `list[str]`).
    description: The field's description.
    default: Default value written as JSON or YAML text (e.g. `5`, `"Pending"`);
        None declares the field without a default, i.e. required. An empty string
        is the empty-string default, not "no default".
    pythonpath: Directory to import re-export modules from.

Returns:
    The draft the field was added to.

Raises:
    SLDBModelError: When the model is not registered.
    SLDBModelEditError: When the class is not found or already declares the field.

## Imports

["__future__", "pathlib", "sldb.api.documents.data_values", "sldb.api.journal", "sldb.api.model_drafts.field_blocks", "sldb.api.model_drafts.model_draft", "sldb.api.model_drafts.source_location", "sldb.api.model_drafts.template_literals", "sldb.api.model_drafts.template_sections", "sldb.api.model_registry.load_registered_model", "sldb.api.stores.open_store"]

## Purpose

Not documented.

## Architecture

Not documented.
