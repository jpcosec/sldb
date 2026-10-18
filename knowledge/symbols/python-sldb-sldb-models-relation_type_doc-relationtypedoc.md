---
id: python-sldb-sldb-models-relation_type_doc-relationtypedoc
system: sldb
module: sldb.models.relation_type_doc
qualname: RelationTypeDoc
kind: ClassDef
source_path: sldb/models/relation_type_doc.py
source_span: 12:75
source_sha256: 473af22f56bae5c6ca75891afe43a8ea3a5d5f99ed9ec72b07e4276319db14d3
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.models.relation_type_doc:RelationTypeDoc; contract-sha256:515cb8041c25bac892c19586bbef1676483c0033245bb9be974048c480e7b9f9
---

# RelationTypeDoc

## Signature

Not applicable.

## Docstring

Declares one relation type: its name, which node classes it connects, its
direction and cardinality, the predicate axis it answers, and a default
condition every edge of this type inherits.

The edge index reports any edge whose ``relation_type`` has no tracked
RelationTypeDoc. The structural relations the index itself produces are shipped
as RelationTypeDocs too (see ``sldb.models.builtin_relation_types``), so the
graph is described entirely by documents.

## Imports

["__future__", "pydantic", "sldb.models.structured_doc", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
