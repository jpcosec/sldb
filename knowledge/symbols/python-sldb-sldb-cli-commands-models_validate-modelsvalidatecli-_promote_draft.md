---
id: python-sldb-sldb-cli-commands-models_validate-modelsvalidatecli-_promote_draft
system: sldb
module: sldb.cli.commands.models_validate
qualname: ModelsValidateCLI._promote_draft
kind: FunctionDef
source_path: sldb/cli/commands/models_validate.py
source_span: 51:60
source_sha256: 4e1ff2b38cdb6ce7cdc7f12d753ae26ebbe9595cfacfa79bf07e65ba70042c10
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.commands.models_validate:ModelsValidateCLI._promote_draft;
  contract-sha256:ba6d4fb4c56717d4fa0ec2a1ff7adab8bbc8a34f245d09873270e119d7b655d2
---

# ModelsValidateCLI._promote_draft

## Signature

_promote_draft(self, args: Any, path: Path, draft_path: Path, details: dict[str, Any], model_cli: Any)

## Docstring

Install the draft and reindex. If the reindex fails, the active model, the draft and the
indexes are put back, so the store stays consistent and the promote can be retried.

## Imports

["__future__", "contextlib", "json", "pathlib", "sldb.cli.commands.models_utils", "sldb.cli.commands.models_validate_utils", "sldb.core.exceptions", "sldb.runtime.validation", "sys", "typing", "yaml"]

## Purpose

Not documented.

## Architecture

Not documented.
