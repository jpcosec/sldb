---
id: python-sldb-sldb-core-data_extractor-dataextractor-_handle_section_body
system: sldb
module: sldb.core.data_extractor
qualname: DataExtractor._handle_section_body
kind: FunctionDef
source_path: sldb/core/data_extractor.py
source_span: 59:75
source_sha256: 0743434351f23ade474b8b134b7d283fdfa7df7641101188657110a9b05e9faa
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.data_extractor:DataExtractor._handle_section_body;
  contract-sha256:664c0ed23099b17a51cc7d55f14eb8da5b3a46a963e83f79f08127a26cc0e039
---

# DataExtractor._handle_section_body

## Signature

_handle_section_body(self, data_blocks: list[SLDBNode], recipes: list[dict[str, Any]], r_idx: int, raw_markdown: str | None, state: dict[str, Any])

## Docstring

Capture the blocks up to the next recipe's boundary.

curr_block is boundary_idx - 1, never max(search, boundary_idx - 1):
an empty section has boundary_idx == search, and claiming search as
consumed would skip the boundary block itself -- which belongs to the
NEXT recipe. That made one empty section shift every later section up
by one and silently destroy content. For a non-empty capture both
expressions agree, since boundary_idx - 1 >= search.

## Imports

["sldb.core.contracts.marker", "sldb.core.extractor.recipe_matcher", "sldb.core.extractor.section_boundary", "sldb.core.node", "sldb.core.node_handler", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
