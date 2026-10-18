---
id: python-sldb-sldb-models-cli_command_doc-clicommanddoc
system: sldb
module: sldb.models.cli_command_doc
qualname: CliCommandDoc
kind: ClassDef
source_path: sldb/models/cli_command_doc.py
source_span: 9:88
source_sha256: 3407b12785a6a98e85b4233ca5b27b6edba1cfe991a27ad2fa36a5b1ca02ac6e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.models.cli_command_doc:CliCommandDoc; contract-sha256:f18990adfce9693aeea7de8c218b81632a8e2d789f343906739aac27f525a599
---

# CliCommandDoc

## Signature

Not applicable.

## Docstring

A single leaf CLI command as a self-describing knowledge entity.

In the selfdoc workflow, the parser owns identity, synopsis, arguments, and
provenance. Authors own purpose, how_it_works, usage examples, and tags.
Regeneration preserves those authored fields instead of deriving semantics
from option names. This contract does not itself populate argparse help.

## Imports

[".knowledge_tag", "__future__", "pydantic", "sldb.models.structured_doc"]

## Purpose

A single leaf CLI command as a self-describing knowledge entity.

## Architecture

Not documented.
