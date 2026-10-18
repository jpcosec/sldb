---
id: python-sldb-sldb-cli-commands-doc-doccli-delete
system: sldb
module: sldb.cli.commands.doc
qualname: DocCLI.delete
kind: FunctionDef
source_path: sldb/cli/commands/doc.py
source_span: 94:101
source_sha256: 6e6844bf3019af4fd3b4655fb340006d29811ce6c27ed1f22c4f7a0ac135eaab
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.commands.doc:DocCLI.delete; contract-sha256:3b8e30236c34d6728c32ac2b6d655c7d6faa70c0aa88b89f3cae380ee0ad5ddf
---

# DocCLI.delete

## Signature

delete(self, args: Any)

## Docstring

Untrack a document and delete its Markdown file, asking first unless --yes.

## Imports

["__future__", "pathlib", "sldb.api.documents.create_document", "sldb.api.documents.delete_document", "sldb.api.documents.track_document_file", "sldb.api.documents.untrack_document", "sldb.cli.commands.doc_lookup", "sldb.cli.commands.docs_batch", "sldb.cli.model_utils", "sldb.cli.output_format", "sldb.cli.store_context", "sldb.core.exceptions", "sldb.runtime.validation", "sldb.store", "sldb.store.derived_rebuild", "sldb.store.hashing", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.model_node", "sldb.store.ops", "typing", "yaml"]

## Purpose

Untrack a document and delete its Markdown file, asking first unless --yes.

## Architecture

Not documented.
