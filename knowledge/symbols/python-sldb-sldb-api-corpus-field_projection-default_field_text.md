---
id: python-sldb-sldb-api-corpus-field_projection-default_field_text
system: sldb
module: sldb.api.corpus.field_projection
qualname: default_field_text
kind: FunctionDef
source_path: sldb/api/corpus/field_projection.py
source_span: 50:60
source_sha256: 12b805b729ee9e80e1d3924b72db118bb702cd532a050ded986479ca9ebdce97
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.corpus.field_projection:default_field_text;
  contract-sha256:122ac339424bdb47abf22bd1174d49b7f8114f89a98b25e1013ada26f6025c8e
---

# default_field_text

## Signature

default_field_text(value: Any)

## Docstring

The indexable text of a field value, or empty when there is nothing to rank.

Lists of strings are joined: a list field is one semantic unit, and indexing its items
separately would need ids the store cannot address.

## Imports

["__future__", "dataclasses", "typing"]

## Purpose

The indexable text of a field value, or empty when there is nothing to rank.

## Architecture

Not documented.
