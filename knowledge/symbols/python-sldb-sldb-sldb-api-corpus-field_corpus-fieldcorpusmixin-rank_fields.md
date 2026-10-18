---
id: python-sldb-sldb-sldb-api-corpus-field_corpus-fieldcorpusmixin-rank_fields
system: sldb
module: sldb.sldb.api.corpus.field_corpus
qualname: FieldCorpusMixin.rank_fields
kind: FunctionDef
source_path: sldb/api/corpus/field_corpus.py
source_span: 48:66
source_sha256: 6dad5eafe1767da90b9e420917c11bc7dbab62d21ad4ea07269b470864063218
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.corpus.field_corpus:FieldCorpusMixin.rank_fields;
  contract-sha256:36aa12fd60c17e52c4d29b6094c75d70a991a8bca950c8dc67591a98e3eedf9d
---

# FieldCorpusMixin.rank_fields

## Signature

rank_fields(self, query: str, k: int | None=None, threshold: float=0.0, among: Sequence[str] | None=None, refresh: bool=True)

## Docstring

The fields closest to `query`, best first.

`among` filters by field id (`Model:doc#field`) or by document id: naming a document
admits every one of its fields, which is what a caller narrowing to a document means.

## Imports

["__future__", "pathlib", "sldb.api.corpus.corpus_audit", "sldb.api.corpus.field_entries", "sldb.api.corpus.field_hit", "sldb.api.matching.document_index", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
