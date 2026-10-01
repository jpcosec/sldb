---
id: pill-006-model-registration-is-queryable
tags:
- system:sldb
- system:deskops
- topic:models
- topic:query
---

# Model registration must be queryable

## What

_Define the context or guardrail this pill carries._

Registered model state should be inspectable through explicit SLDB commands and APIs rather than by forcing downstream tools to read store files directly.

## Why

_Explain why this context matters for safe execution._

Deskops and operators need to detect missing, stale, or incompatible model registrations without coupling to raw store layout.

## When

_Describe when an agent should apply this pill._

Apply this pill when changing model registration, list/check surfaces, or recovery tooling.

## Where

_Name the files, surfaces, or scope this pill applies to._

- `src/sldb/cli/commands/models.py`
- store model indexes
- deskops recovery and health integrations

## How

_Describe the correct way to apply this guidance._

Expose model registration state through supported CLI/API surfaces and preserve enough metadata for downstream consumers to reason about compatibility.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not require callers to scrape YAML indexes directly or infer registration state from incidental filesystem details.

