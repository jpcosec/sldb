---
id: python-sldb-sldb-models-relation_type_doc-relationtypedoc
system: sldb
module: sldb.models.relation_type_doc
qualname: RelationTypeDoc
kind: ClassDef
source_path: sldb/models/relation_type_doc.py
source_span: 12:75
source_sha256: f99ab9c832caebf6816133f6848f77f9a533126f75a07ff8fae52cf9ce734d02
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.models.relation_type_doc:RelationTypeDoc; contract-sha256:d0643e605240da8c5034775bc93277d71696bb62aea4103d812b1da631aa695c
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

Declares one relation type: its name, which node classes it connects, its direction and cardinality, the predicate axis it answers, and a default condition every edge of this type inherits.

## Architecture

Not documented.
