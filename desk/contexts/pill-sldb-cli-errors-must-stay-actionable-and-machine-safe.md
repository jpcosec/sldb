---
# pill-xxx
id: pill-sldb-cli-errors-must-stay-actionable-and-machine-safe
status: active
# e.g., language:python, library:pydantic
tags:
- system:sldb
- topic:failure-mode
- topic:serialization
- language:python
---

# SLDB CLI errors must stay actionable and machine-safe

## What

_Define the context or guardrail this pill carries._

User-input failures should become actionable diagnostics while machine-readable outputs and document semantics remain intact.

## Why

_Explain why this context matters for safe execution._

Raw file errors, datetime serialization crashes, confusing empty-input messages, and location-dependent output create avoidable operator confusion and downstream automation drift.

## When

_Describe when an agent should apply this pill._

Apply this pill when changing FAQ, inbox JSON, extract/render/validate, docs, fields, stores, query, help, version, or empty-input validation behavior.

## Where

_Name the files, surfaces, or scope this pill applies to._

- `src/sldb/cli/main.py`
- `src/sldb/cli/parser.py`
- `src/sldb/cli/commands/`
- serialization-sensitive tests

## How

_Describe the correct way to apply this guidance._

Normalize output only at the presentation boundary, verify exit codes and stderr, and test both human-facing and machine-facing command behavior where relevant.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not catch every exception as a user error, degrade stored data just to satisfy JSON output, or let help text and parser behavior drift apart.
