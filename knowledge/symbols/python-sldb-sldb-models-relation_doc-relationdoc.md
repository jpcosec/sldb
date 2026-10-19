---
id: python-sldb-sldb-models-relation_doc-relationdoc
system: sldb
module: sldb.models.relation_doc
qualname: RelationDoc
kind: ClassDef
source_path: sldb/models/relation_doc.py
source_span: 12:71
source_sha256: d5a32d8b5a9343b45ccfd8ff1accc04dc7578d892e753b84047335c74acb13a1
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.models.relation_doc:RelationDoc; contract-sha256:08736d70fe9b0f6a9e46833288161e2495599ca701cbd86a9e75aadb1f3bcf47
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
