---
id: python-sldb-sldb-sldb-core-renderer_engine-list-listrenderer-_render_item
system: sldb
module: sldb.sldb.core.renderer_engine.list
qualname: ListRenderer._render_item
kind: FunctionDef
source_path: sldb/core/renderer_engine/list.py
source_span: '33:48'
source_sha256: 101ba951069266d9837b705dafc777e18bbd370f6f749fcbcacd7ef2aa38c859
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.renderer_engine.list:ListRenderer._render_item;
  contract-sha256:96edc71b0cbf003973e8d81b572ff468fca26efc455c098063655c4d2185b40d
---

# ListRenderer._render_item

## Signature

_render_item(self, item_text: str, data: dict[str, Any], prefix: str, scalar_root: str | None)

## Docstring

One list item, with every recorded path scoped under its index.

Args:
    item_text: The template of a single item.
    data: The item's payload mapping.
    prefix: Path of the item, such as ``steps/2``.
    scalar_root: Root property name when the item is a scalar, else None.

Returns:
    The rendered item.

## Imports

["__future__", "re", "sldb.core.handlers.list_escape", "sldb.core.renderer_engine.base", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
