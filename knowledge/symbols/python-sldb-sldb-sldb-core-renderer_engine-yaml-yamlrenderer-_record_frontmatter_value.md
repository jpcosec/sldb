---
id: python-sldb-sldb-sldb-core-renderer_engine-yaml-yamlrenderer-_record_frontmatter_value
system: sldb
module: sldb.sldb.core.renderer_engine.yaml
qualname: YamlRenderer._record_frontmatter_value
kind: FunctionDef
source_path: sldb/core/renderer_engine/yaml.py
source_span: 69:85
source_sha256: 04be636440ea839f16e888cdb899ebe59568b79ca13e6c807cb8bbb727e3be7f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.renderer_engine.yaml:YamlRenderer._record_frontmatter_value;
  contract-sha256:67377bda0373c968d8fd075e5ec06fc0bf988a49bbb60c16fa9ab6be69e5ddeb
---

# YamlRenderer._record_frontmatter_value

## Signature

_record_frontmatter_value(self, dumped: str, key: str, marker: Any)

## Docstring

Wrap what follows ``key:`` in a dumped front-matter line, if recording.

Args:
    dumped: The already-dumped ``key: value`` line (may be multi-line).
    key: The front-matter key.
    marker: The parsed marker that owns the value.

Returns:
    The line with its value span recorded, or unchanged without a recorder.

## Imports

["__future__", "re", "sldb.core.handlers.utils", "sldb.core.renderer_engine.base", "typing", "yaml"]

## Purpose

Not documented.

## Architecture

Not documented.
