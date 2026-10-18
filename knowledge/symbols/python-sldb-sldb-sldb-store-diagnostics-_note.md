---
id: python-sldb-sldb-sldb-store-diagnostics-_note
system: sldb
module: sldb.sldb.store.diagnostics
qualname: _note
kind: FunctionDef
source_path: sldb/store/diagnostics.py
source_span: 81:96
source_sha256: 8df97842ce8ae42fe7bd7d412973d2a760e684bbcde8e00f0b22146d56f8bab7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.diagnostics:_note; contract-sha256:6a6f5495afe8b59103437b5e2c440aecd5f6e85d94cd5090d45a3773f8d749a3
---

# _note

## Signature

_note(content_ok: bool, fields_ok: bool, contract_ok: bool)

## Docstring

Which verdict the two hashes earn — and who to blame when the fields disagree.

Fields differing while the text stands still is not the document's doing when the model's
contract moved: the same text extracts to something else now. Blaming the document there
sent the reader to inspect a file nobody had edited.

The contract only excuses the document while its TEXT is intact (`content_ok`). A moved
contract on a file that was also edited is still a data mutation and still needs a human:
letting the contract absolve it would hide a hand edit behind a safe-to-run verdict.

## Imports

["__future__", "pathlib", "sldb.store.diagnostics_models", "sldb.store.diagnostics_models.text_history", "sldb.store.field_set_drift", "sldb.store.hashing", "sldb.store.io", "sldb.store.layout", "sldb.store.legacy_contract", "sldb.store.model_node", "sldb.store.model_origin", "sldb.store.models", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
