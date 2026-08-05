---
id: feature-lisp-surface-expansion
status: proposed
summary: Expand Lisp-authored schema and macro surfaces beyond the minimal first slice while preserving kernel authority and plan validation.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- core_README.md
- interfaces.md
- desk/atoms/lisp-metalanguage.md
- desk/atoms/lisp-schema-language.md
- desk/atoms/lisp-macro-language.md
- desk/atoms/schema-binding.md
depends_on:
- feature-lisp-control-and-data-surface-first-slice
---

# Lisp surface expansion

## Goal

Define the macrotask for broadening the Lisp-authored surface beyond the minimum needed for the first slice.

## Includes

- richer schema forms
- richer macro/control forms
- reusable library surface
- inspection-friendly form contracts

## Excludes

- standalone Lisp authority
- bypasses around kernel validation

## Needs design or grounding before promotion

- minimal-to-expanded surface transition
- compatibility rules for Lisp forms
- inspection/serialization expectations
- how much effect/query authoring to expose directly
