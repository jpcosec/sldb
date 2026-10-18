---
id: python-sldb-sldb-models-relation_doc-relationdoc
system: sldb
module: sldb.models.relation_doc
qualname: RelationDoc
kind: ClassDef
source_path: sldb/models/relation_doc.py
source_span: 12:71
source_sha256: 09c8b0358963a32620cf8ff01a7f7e42322dbabe6afaea62d2c15d586d9e49e8
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.models.relation_doc:RelationDoc; contract-sha256:4c6596d31e4b151991ddbf883600ce248146a14fed334f01914802de8bc45acc
---

# RelationDoc

## Signature

Not applicable.

## Docstring

One authored edge source -> target of a given relation type.

Content-blind: it carries ids and a type token, never the content of its
endpoints. It is a document of the store; the edge index turns it into an
edge and validates it against its RelationTypeDoc. It is not itself a node
of the index.

## Imports

["__future__", "pydantic", "sldb.models.structured_doc", "typing"]

## Purpose

One authored edge source -> target of a given relation type.

## Architecture

Not documented.
