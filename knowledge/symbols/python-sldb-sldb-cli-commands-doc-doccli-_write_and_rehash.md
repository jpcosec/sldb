---
id: python-sldb-sldb-cli-commands-doc-doccli-_write_and_rehash
system: sldb
module: sldb.cli.commands.doc
qualname: DocCLI._write_and_rehash
kind: FunctionDef
source_path: sldb/cli/commands/doc.py
source_span: 57:62
source_sha256: 6e6844bf3019af4fd3b4655fb340006d29811ce6c27ed1f22c4f7a0ac135eaab
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.commands.doc:DocCLI._write_and_rehash; contract-sha256:60e43830af300ab105e9117844744daeca101bcb5067e8a8c49a4772605d03d3
---

# DocCLI._write_and_rehash

## Signature

_write_and_rehash(root: Any, doc: Any, model_type: Any, rendered: str)

## Docstring

Write the rendered Markdown and record both hashes plus the per-field map.

## Imports

["__future__", "pathlib", "sldb.api.documents.create_document", "sldb.api.documents.delete_document", "sldb.api.documents.track_document_file", "sldb.api.documents.untrack_document", "sldb.cli.commands.doc_lookup", "sldb.cli.commands.docs_batch", "sldb.cli.model_utils", "sldb.cli.output_format", "sldb.cli.store_context", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store", "sldb.store.derived_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.model_node", "sldb.store.ops", "typing", "yaml"]

## Purpose

Write the rendered Markdown and record both hashes plus the per-field map.

## Architecture

Not documented.
