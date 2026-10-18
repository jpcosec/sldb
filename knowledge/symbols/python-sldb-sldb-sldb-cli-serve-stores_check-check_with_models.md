---
id: python-sldb-sldb-sldb-cli-serve-stores_check-check_with_models
system: sldb
module: sldb.sldb.cli.serve.stores_check
qualname: check_with_models
kind: FunctionDef
source_path: sldb/cli/serve/stores_check.py
source_span: '16:27'
source_sha256: 53f7109c2d1537c0b93dd1c1d0d0138853d43c7059383be4bec108a0be487c4d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.cli.serve.stores_check:check_with_models;
  contract-sha256:81048c3e3619966f4db7f31b82c2c865643bca59fe0529906d7c01c76fc3a80f
---

# check_with_models

## Signature

check_with_models(store_path: Path, root: Path, pythonpath: str | None)

## Docstring

One diagnosis, two views: the existing keys untouched, and `root_ok`, `hash_a_ok`,
`summary` and `models[]` exactly as `sldb stores check --format json` prints them.

Each `models[]` entry has `roster_ok`, `contract_ok` and `documents[]` with `path`,
`path_exists`, `content_ok`, `fields_ok`, `note` and `explain` for every document,
not only the damaged ones.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.model_reference", "sldb.api.stores.store_check", "sldb.cli.commands.store_check", "sldb.store.diagnostics", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
