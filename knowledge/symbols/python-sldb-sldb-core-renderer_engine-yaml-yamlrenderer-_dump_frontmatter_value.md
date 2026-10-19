---
id: python-sldb-sldb-core-renderer_engine-yaml-yamlrenderer-_dump_frontmatter_value
system: sldb
module: sldb.core.renderer_engine.yaml
qualname: YamlRenderer._dump_frontmatter_value
kind: FunctionDef
source_path: sldb/core/renderer_engine/yaml.py
source_span: 55:67
source_sha256: 04be636440ea839f16e888cdb899ebe59568b79ca13e6c807cb8bbb727e3be7f
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.yaml:YamlRenderer._dump_frontmatter_value;
  contract-sha256:249eb5bc871adeb58b08f4ff870d793b9c4553bef04da2a1cf9ec5b13c6073ae
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

Dump one front-matter pair to YAML and record its value span.

## Architecture

Not documented.
