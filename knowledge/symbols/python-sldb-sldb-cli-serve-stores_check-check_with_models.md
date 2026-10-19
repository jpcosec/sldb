---
id: python-sldb-sldb-cli-serve-stores_check-check_with_models
system: sldb
module: sldb.cli.serve.stores_check
qualname: check_with_models
kind: FunctionDef
source_path: sldb/cli/serve/stores_check.py
source_span: '16:27'
source_sha256: 53f7109c2d1537c0b93dd1c1d0d0138853d43c7059383be4bec108a0be487c4d
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.serve.stores_check:check_with_models; contract-sha256:91a8342a26ecd8d48ea5efe651c3aa1f6bf40483253e4155219b143279b8462a
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

One diagnosis, two views: the existing keys untouched, and `root_ok`, `hash_a_ok`, `summary` and `models[]` exactly as `sldb stores check --format json` prints them.

## Architecture

Not documented.
