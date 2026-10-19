---
id: python-sldb-sldb-api-documents-frontmatter_keys-refuse_undeclared_frontmatter
system: sldb
module: sldb.api.documents.frontmatter_keys
qualname: refuse_undeclared_frontmatter
kind: FunctionDef
source_path: sldb/api/documents/frontmatter_keys.py
source_span: '38:49'
source_sha256: 4b4453f6242653a65855e4a18152278b1b5009fa18c0c96796d4ad10b911d50f
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.documents.frontmatter_keys:refuse_undeclared_frontmatter;
  contract-sha256:39778e49551d7feb0f7ed63dfa34447e650f0ff56204c58b6cabb5b2ed889f30
---

# refuse_undeclared_frontmatter

## Signature

refuse_undeclared_frontmatter(model_type: type, markdown: str, name: str)

## Docstring

Raise unless every top-level frontmatter key is declared by the model.

## Imports

["__future__", "re", "sldb.core.ast", "sldb.core.exceptions", "yaml"]

## Purpose

Raise unless every top-level frontmatter key is declared by the model.

## Architecture

Not documented.
