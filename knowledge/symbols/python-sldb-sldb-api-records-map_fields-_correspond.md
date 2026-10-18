---
id: python-sldb-sldb-api-records-map_fields-_correspond
system: sldb
module: sldb.api.records.map_fields
qualname: _correspond
kind: FunctionDef
source_path: sldb/api/records/map_fields.py
source_span: 59:74
source_sha256: 975914d19b94bb963a9d375850b1edd567564b470416ab3c463f250a871f3706
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.records.map_fields:_correspond; contract-sha256:ed7393590bd8e640d11de0871ec81339fe0feddae0afe8318f937f581ca9b18e
---

# _correspond

## Signature

_correspond(template_sections: list, rendered_sections: list)

## Docstring

Whether the sections at the template's indices are the template's own sections.

With a single template section this is provable: there is one candidate owner, so
extra headings -- which can only come from a field value, rendered inside it -- cannot
displace it, and the only thing left to check is that the level is the right one.

With more sections it is not: a heading injected by a field value can take a template
slot and the mapping would be silently wrong, which is the defect this guard exists
for. There it keeps refusing instead of guessing.

## Imports

[".extract", "logging", "re", "sldb.core.contracts"]

## Purpose

Not documented.

## Architecture

Not documented.
