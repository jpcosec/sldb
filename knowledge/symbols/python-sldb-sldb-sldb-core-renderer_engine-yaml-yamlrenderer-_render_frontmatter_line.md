---
id: python-sldb-sldb-sldb-core-renderer_engine-yaml-yamlrenderer-_render_frontmatter_line
system: sldb
module: sldb.sldb.core.renderer_engine.yaml
qualname: YamlRenderer._render_frontmatter_line
kind: FunctionDef
source_path: sldb/core/renderer_engine/yaml.py
source_span: '38:53'
source_sha256: 04be636440ea839f16e888cdb899ebe59568b79ca13e6c807cb8bbb727e3be7f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.renderer_engine.yaml:YamlRenderer._render_frontmatter_line;
  contract-sha256:e81b33927e6aa006190f018026a75f9abc6f51b827a2c04bd3bcfaf476792e25
---

# YamlRenderer._render_frontmatter_line

## Signature

_render_frontmatter_line(self, line: str, data: dict[str, Any])

## Docstring

One front-matter line. An unused optrev field omits the whole line,
so the front matter reads exactly as if the field were never declared:
a None mapping/list VALUE means absent, while `{}`/`[]` are present and
still dump below. kind == 'render' markers are display-only, so their
None keeps the historical `null` dump.

## Imports

["__future__", "re", "sldb.core.handlers.utils", "sldb.core.renderer_engine.base", "typing", "yaml"]

## Purpose

Not documented.

## Architecture

Not documented.
