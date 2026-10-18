---
id: python-sldb-sldb-sldb-api-model_create-create_model-create_model
system: sldb
module: sldb.sldb.api.model_create.create_model
qualname: create_model
kind: FunctionDef
source_path: sldb/api/model_create/create_model.py
source_span: '28:52'
source_sha256: 0bd54b0bb70f70280fc7b52ad98d77a7e45d29e4e93ac612b024b212fa211055
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_create.create_model:create_model;
  contract-sha256:a3ef23ec8007285386f636595fc290e617b59a58ed0cefe8e8da3ba4135613ab
---

# create_model

## Signature

create_model(store: str | Path | None, name: str, fields: list, template: str | None=None, base: str | None=None, target_package: str=DEFAULT_PACKAGE, pythonpath: str | None=None, actor: str | None=None)

## Docstring

Generate, check, write and register a model declared as JSON fields.

Args:
    store: The store to register the model in (path, alias, or None to discover it).
    name: CamelCase model name; the class and file name derive from it.
    fields: List of `{name, type, description, required?, default?, enum?}` dicts.
    template: The model's Markdown template; None renders one section per field.
    base: A registered model name the new model extends; None extends StructuredNLDoc.
    target_package: Package under `pythonpath` to write the generated module into.
    pythonpath: Directory importing the module from; defaults to the store's project root.
    actor: Optional label recorded in the store journal for this write.

Returns:
    The new registry record (version 1).

Raises:
    SLDBModelError: When the declaration is invalid or the generated module fails its check.

## Imports

["__future__", "importlib", "pathlib", "sldb.api.journal", "sldb.api.model_create.field_decl", "sldb.api.model_create.model_check", "sldb.api.model_create.model_source", "sldb.api.model_registry.add_model", "sldb.api.model_registry.load_registered_model", "sldb.api.model_registry.model_registration", "sldb.api.stores.open_store", "sldb.core.exceptions", "sys"]

## Purpose

Not documented.

## Architecture

Not documented.
