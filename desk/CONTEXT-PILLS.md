# Context Pills

This file defines the minimum structure and usage rules for context pills in SLDB.

## Purpose

Context pills are pre-drafted rationale that make a task unambiguous before execution.

- Code is truth.
- Docs are index.
- Pills contain only the reasoning/context subset needed for execution.
- Pills are temporary and must be audited for staleness.

## Minimum Content Categories

Every pill should cover these categories:

- Why - why this approach over alternatives
- What - constraints and guardrails
- Where - where in the codebase it applies
- How - pattern or model that informs implementation
- Language - terminology, naming, and vocabulary rules
- Scope - context boundary vs implementation artifact

## Minimum Classification Dimensions

Every pill should be classified by:

- Type - `guardrail`, `decision`, `pattern`, `model`
- Scope - `global`, `domain`, `component`
- Language - `en`, `es`, `python`, `typescript`, or other applicable language/domain label
- Nature - `context` or `implementation`

## Lifecycle

Pill lifecycle:

1. Drafted during planning.
2. Bound to an active task.
3. Audited after each implementation step.
4. Kept only while still necessary.
5. Deleted once redundant with code/docs or once the task is complete.

## Pre-Execution Gate

Before starting a task, ask:

> Is there any ambiguous or unclear aspect not covered by the context machine?

- If no, proceed.
- If yes, create or bind the missing pills before execution.

## Non-Redundancy Rule

- Do not use pills as history logs.
- Do not restate code behavior already obvious in source.
- Do not restate stable documentation verbatim.
- Do not keep pills after their knowledge has flowed into code or docs.
