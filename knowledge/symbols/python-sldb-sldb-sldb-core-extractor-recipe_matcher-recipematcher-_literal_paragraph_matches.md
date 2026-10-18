---
id: python-sldb-sldb-sldb-core-extractor-recipe_matcher-recipematcher-_literal_paragraph_matches
system: sldb
module: sldb.sldb.core.extractor.recipe_matcher
qualname: RecipeMatcher._literal_paragraph_matches
kind: FunctionDef
source_path: sldb/core/extractor/recipe_matcher.py
source_span: '34:41'
source_sha256: 81108664ed5ec0f46db303dab40c65681fd1b8939a0f39c40ccd44f3b3765711
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.extractor.recipe_matcher:RecipeMatcher._literal_paragraph_matches;
  contract-sha256:075e498a5e56c1078543c52b6c763f9b94642bc754622ae0a62fc8593ce5065f
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

Not documented.

## Architecture

Not documented.
