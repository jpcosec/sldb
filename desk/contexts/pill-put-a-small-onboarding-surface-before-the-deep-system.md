---
# pill-xxx
id: pill-put-a-small-onboarding-surface-before-the-deep-system
status: active
# e.g., language:python, library:pydantic
tags:
- system:sldb
- topic:onboarding
- topic:cli
- workspace:desk
---

# Put a small onboarding surface before the deep system

## What

_Define the context or guardrail this pill carries._

The first-use layer for SLDB should stay small and legible before asking users to understand the full store, model, and workflow depth.

## Why

_Explain why this context matters for safe execution._

A broad concept stack is easier to adopt when users first see a compact entry surface such as help, FAQ, docs explore, and a small number of clear examples.

## When

_Describe when an agent should apply this pill._

Apply this pill to changes affecting help, FAQ, documentation entry points, onboarding commands, or repo-first discovery surfaces.

## Where

_Name the files, surfaces, or scope this pill applies to._

- `docs/faq.md`
- CLI help and parser surfaces
- onboarding-oriented docs and examples

## How

_Describe the correct way to apply this guidance._

Favor a minimal top layer that points users to deeper capabilities only after the first-use path is understandable.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not force first-time users to reconstruct the full internal architecture before they can discover the next useful command or document.
