---
id: python-sldb-sldb-cli-commands-model-modelcli-_save_new_model
system: sldb
module: sldb.cli.commands.model
qualname: ModelCLI._save_new_model
kind: FunctionDef
source_path: sldb/cli/commands/model.py
source_span: '45:48'
source_sha256: 3f5eccd786ef8457b65fff6857405b55911ea6f428ccf096e8259a774507dfcd
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.commands.model:ModelCLI._save_new_model; contract-sha256:15e5a7ac01dfbdbcb24ceab0eb7cb76954ed5e9164ec290cd14ffc552ee0f54f
---

# ModelCLI._save_new_model

## Signature

_save_new_model(self, sp: Any, root: Path, idx: Any, args: Any, model_type: Any, m_path: str, mi_rel: str, di_rel: str)

## Docstring

roster_hash starts as hash_documents_index of the empty index, not "" --
an unhashed empty string fails `stores check` until `models update` runs.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.add_model", "sldb.api.model_registry.model_index_writes", "sldb.cli.model_utils", "sldb.cli.store_context", "sldb.core.exceptions", "sldb.store", "sldb.store.derived_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.layout", "sldb.store.model_node", "sldb.store.ops", "sys", "typing"]

## Purpose

roster_hash starts as hash_documents_index of the empty index, not "" -- an unhashed empty string fails `stores check` until `models update` runs.

## Architecture

Not documented.
