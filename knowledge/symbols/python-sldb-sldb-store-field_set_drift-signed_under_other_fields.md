---
id: python-sldb-sldb-store-field_set_drift-signed_under_other_fields
system: sldb
module: sldb.store.field_set_drift
qualname: signed_under_other_fields
kind: FunctionDef
source_path: sldb/store/field_set_drift.py
source_span: '18:32'
source_sha256: 1ad57505444177e11663cbe39b1fbccceff24a84e0316e440362a7ded430dca4
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.field_set_drift:signed_under_other_fields;
  contract-sha256:7a55e3c13231fe5e761f5fb41b472a30070a7fa468949129f3de1a555cf2da5c
---

# signed_under_other_fields

## Signature

signed_under_other_fields(field_hashes: dict[str, str] | None, model_type: Any, current: Iterable[str] | None=None)

## Docstring

True when the stored field map names a field `model_type` does not declare.

Only that direction is evidence: extraction leaves out fields that are empty or absent from
the text, so a declared field missing from the map proves nothing.

`current` is the key set today's extraction of the same document yields. A model with
`extra="allow"` promotes undeclared frontmatter keys into the payload, so an undeclared key
is not a sign of another contract when the current class still produces it; without
`current` the check stays conservative (a caller about to re-extract anyway loses nothing).

## Imports

["__future__", "pathlib", "sldb.store.hashing", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
