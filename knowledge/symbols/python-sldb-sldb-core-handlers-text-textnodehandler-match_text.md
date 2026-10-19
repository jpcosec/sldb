---
id: python-sldb-sldb-core-handlers-text-textnodehandler-match_text
system: sldb
module: sldb.core.handlers.text
qualname: TextNodeHandler.match_text
kind: FunctionDef
source_path: sldb/core/handlers/text.py
source_span: 74:82
source_sha256: 2f53dfb96ef90c9eeef26f51acaaf2765e3dfbcd80425e6cd03ae0db3c8e37db
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.handlers.text:TextNodeHandler.match_text;
  contract-sha256:0f8a88c907bb8369e0217e07063f7506ef4c97f55236fa5c1412974e8a1d1e14
---

# TextNodeHandler.match_text

## Signature

match_text(self, text: str, recipe: dict[str, Any])

## Docstring

The single executor of the recipe regex, deliberately WITHOUT `re.S`.

This path is only for inline markers, which are single-line; a lone
marker never reaches it because it captures by block range instead.
`re.S` is absent on purpose: with DOTALL a lone `^(.*?)$` would swallow
the next section, which is worse than losing a field.

## Imports

["__future__", "re", "sldb.core.handlers.base", "sldb.core.handlers.utils", "sldb.core.node", "typing"]

## Purpose

The single executor of the recipe regex, deliberately WITHOUT `re.S`.

## Architecture

Not documented.
