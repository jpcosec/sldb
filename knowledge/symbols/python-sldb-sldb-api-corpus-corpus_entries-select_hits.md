---
id: python-sldb-sldb-api-corpus-corpus_entries-select_hits
system: sldb
module: sldb.api.corpus.corpus_entries
qualname: select_hits
kind: FunctionDef
source_path: sldb/api/corpus/corpus_entries.py
source_span: 59:74
source_sha256: 08bedf0e6d55911edfc8240cc2d6de36408dbb7481f42752aa3ecb087fc19816
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.corpus.corpus_entries:select_hits; contract-sha256:41fd44f1b7c0e1fefcd242e07dc8d33632a0de106f0bfc7466a10ccd0b56afa2
---

# select_hits

## Signature

select_hits(ranked: list[tuple[str, float]], by_id: dict[str, CorpusEntry], allowed: set[str] | None, k: int | None)

## Docstring

The ranked entries still in the corpus (and among the allowed ones), at most k.

## Imports

["__future__", "sldb.api.corpus.corpus_entry", "sldb.api.corpus.hit", "sldb.api.journal", "sldb.api.model_registry.model_reference", "sldb.store.query", "typing"]

## Purpose

The ranked entries still in the corpus (and among the allowed ones), at most k.

## Architecture

Not documented.
