---
id: python-sldb-sldb-sldb-models-cli_command_doc-clicommanddoc
system: sldb
module: sldb.sldb.models.cli_command_doc
qualname: CliCommandDoc
kind: ClassDef
source_path: sldb/models/cli_command_doc.py
source_span: 9:88
source_sha256: 5fe3fe878161a4ba892b97098351c628ded65868fd622f06440e4ee1da242949
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.sldb.models.cli_command_doc:CliCommandDoc; contract-sha256:515f7401b09df84a6df2d5c25d40918988f194bec421e320f0935dcc1c7c516c
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
