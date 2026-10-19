---
id: python-sldb-sldb-api-corpus-field_projection-field_id
system: sldb
module: sldb.api.corpus.field_projection
qualname: field_id
kind: FunctionDef
source_path: sldb/api/corpus/field_projection.py
source_span: '25:37'
source_sha256: 12b805b729ee9e80e1d3924b72db118bb702cd532a050ded986479ca9ebdce97
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.corpus.field_projection:field_id; contract-sha256:e117bc284a1250b8e8ca0d002cab8e5f22c9c16d1933a2cde81149121182cf98
---

# field_id

## Signature

field_id(model: str, doc: str, field_path: str, store: str | None=None)

## Docstring

`docs/<Model>/<doc>/<field_path>` — the address `sldb fields` already takes.

One address space for fields, so an id from a ranked hit can be handed straight to
`fields update` without translation. A linked store prefixes its name (`<store>/docs/...`),
the way export ids do, because two stores of a federated world may hold the same
document name.

`field_path` is the field's path in payload space (`tags/0`, `steps/2/title`), so the id
addresses a nested value as precisely as a top-level one.

## Imports

["__future__", "dataclasses", "typing"]

## Purpose

`docs/<Model>/<doc>/<field_path>` — the address `sldb fields` already takes.

## Architecture

Not documented.
