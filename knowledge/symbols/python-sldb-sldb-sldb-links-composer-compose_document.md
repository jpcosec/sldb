---
id: python-sldb-sldb-sldb-links-composer-compose_document
system: sldb
module: sldb.sldb.links.composer
qualname: compose_document
kind: FunctionDef
source_path: sldb/links/composer.py
source_span: '23:31'
source_sha256: 5acd2bc58cf2fca168cf5e1b96c862176219e2511e96df5a35cf80de174b1b2d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.links.composer:compose_document; contract-sha256:d12dfcf64efaf27d1c37d3caf6a62ceec564ce2b98712d086e28d353fc5a909c
---

# compose_document

## Signature

compose_document(dp: Path, sp: Path | None, s: tuple[Path, ...]=(), _root: bool=True, section: str | None=None, links_base: Path | None=None)

## Docstring

Expand `![[x]]` / `![[x#Section]]`. An included document loses its YAML frontmatter;
only the root keeps its own. `s` is the include chain (cycle guard), so a document may be included twice.

## Imports

[".parser", ".render", ".resolver", ".sections", "__future__", "pathlib", "re"]

## Purpose

Not documented.

## Architecture

Not documented.
