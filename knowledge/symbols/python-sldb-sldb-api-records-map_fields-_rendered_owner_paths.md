---
id: python-sldb-sldb-api-records-map_fields-_rendered_owner_paths
system: sldb
module: sldb.api.records.map_fields
qualname: _rendered_owner_paths
kind: FunctionDef
source_path: sldb/api/records/map_fields.py
source_span: '43:56'
source_sha256: 975914d19b94bb963a9d375850b1edd567564b470416ab3c463f250a871f3706
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.records.map_fields:_rendered_owner_paths; contract-sha256:13aeea0c050b96e4dc6d74e15ce731ce57634839d51ccfb2f6d6dfc34759f229
---

# _rendered_owner_paths

## Signature

_rendered_owner_paths(owners: dict[str, int], template_sections: list, rendered_sections: list)

## Docstring

Each template section's path in the rendered document, or {} when it cannot be told.

The counts legitimately differ: a field value can hold a whole markdown document, and
its headings are not template sections. Refusing outright lost the ownership of every
field in such a document (16 of this repo's 1550, 60 fields).

## Imports

[".extract", "logging", "re", "sldb.core.contracts"]

## Purpose

Not documented.

## Architecture

Not documented.
