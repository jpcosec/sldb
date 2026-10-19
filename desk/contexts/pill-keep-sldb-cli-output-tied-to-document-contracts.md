---
# pill-xxx
id: pill-keep-sldb-cli-output-tied-to-document-contracts
status: active
# e.g., language:python, library:pydantic
tags:
- system:sldb
- topic:cli
- topic:documents
- language:python
---

# Keep SLDB CLI output tied to document contracts

## What

_Define the context or guardrail this pill carries._

CLI handlers should present document-model state faithfully instead of inventing alternate semantics at the presentation layer.

## Why

_Explain why this context matters for safe execution._

Crashes around FAQ lookup, inbox serialization, stores, fields, and help text often come from mismatches between document shape and command presentation.

## When

_Describe when an agent should apply this pill._

Apply this pill to tasks that touch FAQ, inbox, stores, fields, docs, help/version output, query warnings, or template-marker detection.

## Where

_Name the files, surfaces, or scope this pill applies to._

- `src/sldb/cli/parser.py`
- `src/sldb/cli/main.py`
- `src/sldb/cli/commands/`
- relevant tests and document models

## How

_Describe the correct way to apply this guidance._

Keep document models authoritative. Validate from realistic caller locations when path handling matters, and make JSON/help output reflect the actual contract instead of ad hoc shortcuts.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not paper over parsing or validation problems with broad exception handlers, and do not make output prettier by breaking machine-readable semantics.
