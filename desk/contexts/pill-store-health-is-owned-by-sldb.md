---
# pill-xxx
id: pill-store-health-is-owned-by-sldb
status: active
# e.g., language:python, library:pydantic
tags:
- system:sldb
- system:deskops
- topic:store
- topic:health
---

# Store health is owned by SLDB

## What

_Define the context or guardrail this pill carries._

SLDB, not deskops, should define and expose what counts as a valid `.sldb/` store.

## Why

_Explain why this context matters for safe execution._

Only SLDB knows the internal store contracts. Duplicating validation logic downstream would create drift and inconsistent recovery behavior.

## When

_Describe when an agent should apply this pill._

Apply this pill when adding health checks, integrity commands, diagnostics, or recovery-related CLI/API surfaces.

## Where

_Name the files, surfaces, or scope this pill applies to._

- `src/sldb/store/diagnostics.py` and `src/sldb/store/diagnostics_models/`
- `src/sldb/cli/commands/store_check.py` (`sldb stores check`)
- downstream deskops health surfaces that call into SLDB

## How

_Describe the correct way to apply this guidance._

Add diagnostics and programmatic checks in SLDB, then let deskops consume those outputs rather than re-implementing the logic.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not make deskops parse raw store internals or duplicate validity rules that belong in SLDB.
