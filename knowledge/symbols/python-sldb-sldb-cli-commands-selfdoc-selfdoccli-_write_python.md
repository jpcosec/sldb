---
id: python-sldb-sldb-cli-commands-selfdoc-selfdoccli-_write_python
system: sldb
module: sldb.cli.commands.selfdoc
qualname: SelfdocCLI._write_python
kind: FunctionDef
source_path: sldb/cli/commands/selfdoc.py
source_span: 56:64
source_sha256: 28b865edc3806d41c2531206bae0f74b45affeaf16cd648fcc59b34b60fbff7d
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.cli.commands.selfdoc:SelfdocCLI._write_python;
  contract-sha256:f12f7d8181fa49e6230b105c5e25369b78365217fdc00ba75880dacccdb091d1
---

# SelfdocCLI._write_python

## Signature

_write_python(self, args, records, where, plans, graph, graph_output)

## Docstring

Write the documents and the graph, then report on what is on disk now (the plans made
before writing still said `missing`, so a first sync always returned 1).

## Imports

["__future__", "contextlib", "json", "pathlib", "sldb.cli.commands", "sldb.cli.selfdoc_context", "sldb.cli.selfdoc_inspect", "sldb.cli.selfdoc_write", "sldb.selfdoc.materialize", "sldb.selfdoc.parser", "sldb.selfdoc.python_materialize", "sldb.selfdoc.python_scanner", "sldb.store.resolver", "sys"]

## Purpose

Write the documents and the graph, then report on what is on disk now (the plans made before writing still said `missing`, so a first sync always returned 1).

## Architecture

Not documented.
