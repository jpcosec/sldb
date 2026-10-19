---
id: python-sldb-sldb-core-ast-markdown_ast_handler-_token_metadata
system: sldb
module: sldb.core.ast.markdown_ast_handler
qualname: _token_metadata
kind: FunctionDef
source_path: sldb/core/ast/markdown_ast_handler.py
source_span: '30:35'
source_sha256: c008382f68385f2ecae45e4a6da3797f202bc15a99d23d5d581875bc7503a280
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.ast.markdown_ast_handler:_token_metadata;
  contract-sha256:65c564cb1260e294fe3fb9f9057c5e2fb9318d07749fc3de06c3bcb6f51cbba8
---

# _token_metadata

## Signature

_token_metadata(node: SyntaxTreeNode)

## Docstring

What the token carries beyond its text: a fence's language (`info`), the markup that
opened it (`markup`: ``` or ~~~, `-` or `*`) and its attributes; only what is present.

## Imports

[".base_ast_handler", "markdown_it", "markdown_it.tree", "sldb.core.node", "typing"]

## Purpose

What the token carries beyond its text: a fence's language (`info`), the markup that opened it (`markup`: ``` or ~~~, `-` or `*`) and its attributes; only what is present.

## Architecture

Not documented.
