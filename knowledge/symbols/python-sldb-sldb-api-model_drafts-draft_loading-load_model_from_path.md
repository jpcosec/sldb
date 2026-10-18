---
id: python-sldb-sldb-api-model_drafts-draft_loading-load_model_from_path
system: sldb
module: sldb.api.model_drafts.draft_loading
qualname: load_model_from_path
kind: FunctionDef
source_path: sldb/api/model_drafts/draft_loading.py
source_span: '17:30'
source_sha256: 49f36834d0c69fe28f85346a57d3add79dc88e88acde4c4be3189fa40e7ae639
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.model_drafts.draft_loading:load_model_from_path;
  contract-sha256:8ba50a368b795c6d05a9db717c4941eef56d028d144ae39535268fe664adb57c
---

# load_model_from_path

## Signature

load_model_from_path(path: Path, module_name: str, attr_path: str, pythonpath: str | None)

## Docstring

Execute a model source file as a `<module>__draft__` module and return the class.

Raises:
    SLDBModelDraftError: When no loader can be built for the file.

## Imports

["__future__", "importlib.machinery", "importlib.util", "pathlib", "sldb.api.model_registry.model_reference", "sldb.core.exceptions", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
