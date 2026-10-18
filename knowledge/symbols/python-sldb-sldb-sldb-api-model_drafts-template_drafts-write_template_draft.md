---
id: python-sldb-sldb-sldb-api-model_drafts-template_drafts-write_template_draft
system: sldb
module: sldb.sldb.api.model_drafts.template_drafts
qualname: write_template_draft
kind: FunctionDef
source_path: sldb/api/model_drafts/template_drafts.py
source_span: '38:53'
source_sha256: 2dc3dcd5ff106176457674fffaccc7fe75d9b3e5c31c4de27c62c5d3334bf448
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.model_drafts.template_drafts:write_template_draft;
  contract-sha256:d95c55aeac48309e1ac19dc4bb48bed89d0347ed55aa0947b33f42a30d3d7904
---

# write_template_draft

## Signature

write_template_draft(source: ModelSource, template: str)

## Docstring

Write `template` into the draft of an already located model source.

Args:
    source: Where the model class is defined.
    template: The new template text; trailing newlines are dropped.

Returns:
    The draft path written.

Raises:
    SLDBModelEditError: When the class or its `__template__` assignment is not found.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.model_drafts.model_draft", "sldb.api.model_drafts.model_source", "sldb.api.model_drafts.source_location", "sldb.api.model_drafts.template_literals", "sldb.api.stores.open_store"]

## Purpose

Not documented.

## Architecture

Not documented.
