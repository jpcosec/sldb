---
id: python-sldb-sldb-sldb-models-relation_doc-relationdoc
system: sldb
module: sldb.sldb.models.relation_doc
qualname: RelationDoc
kind: ClassDef
source_path: sldb/models/relation_doc.py
source_span: 12:71
source_sha256: 09c8b0358963a32620cf8ff01a7f7e42322dbabe6afaea62d2c15d586d9e49e8
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.models.relation_doc:RelationDoc; contract-sha256:f10174351190a1df04b0d93cc9512e3fde9226c3db3412f3a161c9578d0c54bf
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

Not documented.

## Architecture

Not documented.
