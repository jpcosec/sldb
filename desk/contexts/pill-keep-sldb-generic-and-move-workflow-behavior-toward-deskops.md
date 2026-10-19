---
# pill-xxx
id: pill-keep-sldb-generic-and-move-workflow-behavior-toward-deskops
status: active
# e.g., language:python, library:pydantic
tags:
- system:sldb
- system:deskops
- topic:boundary
- workspace:desk
---

# Keep SLDB generic and move workflow behavior toward deskops

## What

_Define the context or guardrail this pill carries._

SLDB should own structured Markdown contracts, stores, validation, and generic navigation/query surfaces. Reusable desk workflow semantics should be owned by `deskops`.

## Why

_Explain why this context matters for safe execution._

If workflow routing, inbox lifecycle, pill semantics, and close-loop automation harden into SLDB, the document substrate becomes repo-specific and drifts from its reusable role.

## When

_Describe when an agent should apply this pill._

Apply this pill when a change touches local desk surfaces, inbox behavior, task lifecycle semantics, or cross-repo workflow coordination.

## Where

_Name the files, surfaces, or scope this pill applies to._

- `desk/`
- `.sldb/` desk workflow registrations
- `src/sldb/cli/commands/inbox.py`
- architecture docs that describe SLDB vs deskops ownership

## How

_Describe the correct way to apply this guidance._

Keep SLDB text-first and generic. Use local desk docs only for SLDB-owned project state, and route reusable workflow behavior, models, and rituals toward `deskops`.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not encode desk-specific lifecycle rules, inbox staging semantics, or operational orchestration as core SLDB behavior when the owning runtime should be `deskops`.
