---
id: python-sldb-sldb-sldb-core-renderer_engine-yaml-yamlrenderer-_dump_frontmatter_value
system: sldb
module: sldb.sldb.core.renderer_engine.yaml
qualname: YamlRenderer._dump_frontmatter_value
kind: FunctionDef
source_path: sldb/core/renderer_engine/yaml.py
source_span: 55:67
source_sha256: 04be636440ea839f16e888cdb899ebe59568b79ca13e6c807cb8bbb727e3be7f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.renderer_engine.yaml:YamlRenderer._dump_frontmatter_value;
  contract-sha256:0dcaae8b5b25cb276a43c6d86231b700a71791f789d9bea5d12bfb2bb8469222
---

# YamlRenderer._dump_frontmatter_value

## Signature

_dump_frontmatter_value(self, key: str, value: Any, marker: Any)

## Docstring

Dump one front-matter pair to YAML and record its value span.

Args:
    key: The front-matter key.
    value: The value to dump.
    marker: The parsed marker that owns the value.

Returns:
    The stripped ``key: value`` YAML line, sentinel-wrapped when recording.

## Imports

["__future__", "re", "sldb.core.handlers.utils", "sldb.core.renderer_engine.base", "typing", "yaml"]

## Purpose

Not documented.

## Architecture

Not documented.
