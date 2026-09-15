---
id: python-sldb-sldb-sldb-core-data_extractor-dataextractor-_handle_section_body
system: sldb
module: sldb.sldb.core.data_extractor
qualname: DataExtractor._handle_section_body
kind: FunctionDef
source_path: sldb/core/data_extractor.py
source_span: 57:69
source_sha256: 67626e17ce20edeb1bd04e488a778becc67db6f4cb29fbddea501d0d7b3e0d49
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.sldb.core.data_extractor:DataExtractor._handle_section_body;
  contract-sha256:971ff63fb893e0eff02b49e99425ea07cc23a69a5137c0f1eccd1a9a05a2e149
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

["sldb.core.extractor.recipe_matcher", "sldb.core.node", "sldb.core.node_handler", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
