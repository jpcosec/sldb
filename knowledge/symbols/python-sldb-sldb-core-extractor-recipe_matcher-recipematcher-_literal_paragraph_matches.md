---
id: python-sldb-sldb-core-extractor-recipe_matcher-recipematcher-_literal_paragraph_matches
system: sldb
module: sldb.core.extractor.recipe_matcher
qualname: RecipeMatcher._literal_paragraph_matches
kind: FunctionDef
source_path: sldb/core/extractor/recipe_matcher.py
source_span: '34:41'
source_sha256: 81108664ed5ec0f46db303dab40c65681fd1b8939a0f39c40ccd44f3b3765711
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.extractor.recipe_matcher:RecipeMatcher._literal_paragraph_matches;
  contract-sha256:26822c51e7d58661e76d45c6cfd8ad47e53a06c96e521a55e7539a8c0d5ff6a9
---

# RecipeMatcher._literal_paragraph_matches

## Signature

_literal_paragraph_matches(self, block: SLDBNode, recipe: dict[str, Any])

## Docstring

A template's literal paragraph (`_Describe the message._`) anchors only a paragraph
with that text. Matching any paragraph by position swallowed the first real paragraph
of a document that lacked the literal, and every rewrite then deleted it.

## Imports

["sldb.core.node", "sldb.core.node_handler", "typing"]

## Purpose

A template's literal paragraph (`_Describe the message._`) anchors only a paragraph with that text. Matching any paragraph by position swallowed the first real paragraph of a document that lacked the literal, and every rewrite then deleted it.

## Architecture

Not documented.
