---
id: python-sldb-sldb-cli-commands-fields_save-save_payload
system: sldb
module: sldb.cli.commands.fields_save
qualname: save_payload
kind: FunctionDef
source_path: sldb/cli/commands/fields_save.py
source_span: '6:14'
source_sha256: dfa90f349fecf44915da47a16fc41cff86d780b9b9a495d819a2b57b8988240e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.commands.fields_save:save_payload; contract-sha256:6dd5fb4f69e098232d5047e1899377754b2215268092c032c15cc9129b85b69b
---

# save_payload

## Signature

save_payload(runtime_doc: Any, payload: dict[str, Any], store_arg: str | None, pythonpath: str | None)

## Docstring

Save a runtime document's new payload; an unregistered model/document or a broken
round-trip exits with the error message, as the `fields` commands always have.

## Imports

["sldb.api.documents.payload_save", "sldb.core.exceptions", "typing"]

## Purpose

Save a runtime document's new payload; an unregistered model/document or a broken round-trip exits with the error message, as the `fields` commands always have.

## Architecture

Not documented.
