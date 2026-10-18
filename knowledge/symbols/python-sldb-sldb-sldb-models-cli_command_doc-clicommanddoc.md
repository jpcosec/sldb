---
id: python-sldb-sldb-sldb-models-cli_command_doc-clicommanddoc
system: sldb
module: sldb.sldb.models.cli_command_doc
qualname: CliCommandDoc
kind: ClassDef
source_path: sldb/models/cli_command_doc.py
source_span: 9:88
source_sha256: 3407b12785a6a98e85b4233ca5b27b6edba1cfe991a27ad2fa36a5b1ca02ac6e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.models.cli_command_doc:CliCommandDoc; contract-sha256:d276af13735ca555a59f700fcc3fa9845f3e791ace4d451ccd0d68fbaa80e662
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

Not documented.

## Architecture

Not documented.
