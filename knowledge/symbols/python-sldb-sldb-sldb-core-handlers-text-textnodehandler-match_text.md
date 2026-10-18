---
id: python-sldb-sldb-sldb-core-handlers-text-textnodehandler-match_text
system: sldb
module: sldb.sldb.core.handlers.text
qualname: TextNodeHandler.match_text
kind: FunctionDef
source_path: sldb/core/handlers/text.py
source_span: 74:82
source_sha256: 2f53dfb96ef90c9eeef26f51acaaf2765e3dfbcd80425e6cd03ae0db3c8e37db
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.handlers.text:TextNodeHandler.match_text;
  contract-sha256:115aecf8db3a83a90b905f6d189b1e22e5aab3861f8bdf3da2c46c9013ccf77a
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

Not documented.

## Architecture

Not documented.
