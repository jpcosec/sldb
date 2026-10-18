---
id: python-sldb-sldb-core-template_extractor-templateextractor-_check_section_body
system: sldb
module: sldb.core.template_extractor
qualname: TemplateExtractor._check_section_body
kind: FunctionDef
source_path: sldb/core/template_extractor.py
source_span: '46:59'
source_sha256: 771a869da5394d801b3b55e95519bc3f75e5db7d525cb4866b17cdf5ebb8fefd
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.template_extractor:TemplateExtractor._check_section_body;
  contract-sha256:fdc38f303950345880bda9046bf046eb229c6ba497944ec9bb80c4fb146e8082
---

# TemplateExtractor._check_section_body

## Signature

_check_section_body(self, recipe: dict[str, Any], node: SLDBNode, state: dict[str, Any])

## Docstring

Lone data marker: paragraph → block range, heading → regex, else error.

A lone marker owns its section body; block range is the only capture that
keeps line breaks. Gating on `is_reversible` alone made `optrev` fall to
the regex path and lose everything past the first line break, silently.

## Imports

["re", "sldb.core.exceptions", "sldb.core.node", "sldb.core.node_handler", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
