---
id: python-sldb-sldb-sldb-core-contracts-marker-recipe_is_optional
system: sldb
module: sldb.sldb.core.contracts.marker
qualname: recipe_is_optional
kind: FunctionDef
source_path: sldb/core/contracts/marker.py
source_span: '51:58'
source_sha256: 726f13aa6aec69fcd478d34e0c30be6efe518c5ce653f29fd53b55ddfea96897
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.contracts.marker:recipe_is_optional;
  contract-sha256:18c26292d6dec81336461819830b36e8dc1437a63129f5de616db7573cf34f82
---

# recipe_is_optional

## Signature

recipe_is_optional(recipe: dict[str, Any])

## Docstring

Whether the recipe's single field may be absent from the payload.

Lives beside `Marker` because it answers a question about the marker, not
about extraction: both capture paths ask it, and neither owns it.

## Imports

["pydantic", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
