---
id: python-sldb-sldb-api-documents-frontmatter_keys-undeclared_frontmatter_keys
system: sldb
module: sldb.api.documents.frontmatter_keys
qualname: undeclared_frontmatter_keys
kind: FunctionDef
source_path: sldb/api/documents/frontmatter_keys.py
source_span: '26:35'
source_sha256: 4b4453f6242653a65855e4a18152278b1b5009fa18c0c96796d4ad10b911d50f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.frontmatter_keys:undeclared_frontmatter_keys;
  contract-sha256:64b10cf2852d68564e89cdeab57b519928f854495a7f86660af9869b04deaee5
---

# undeclared_frontmatter_keys

## Signature

undeclared_frontmatter_keys(model_type: type, markdown: str)

## Docstring

The document's top-level frontmatter keys the model's template never declares.

None when the template's frontmatter is a single dict placeholder: that dict carries any
key through extraction and back on re-render, so nothing is lost (deskops' TaskDoc).

## Imports

["__future__", "re", "sldb.core.ast", "sldb.core.exceptions", "yaml"]

## Purpose

Not documented.

## Architecture

Not documented.
