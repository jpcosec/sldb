---
layer: shared
id: lisp-metalanguage
title: Lisp metalanguage
five_wh_one_plus: how
tags:
- system:sldb
- domain:architecture-boundaries
- domain:architecture-integration
provenance: source docs/core/reasoning.md
---

# Lisp metalanguage

## Answer

Lisp is an authored language surface around the Rust kernel for expressing schemas, macros, queries, transforms, rules, and effects, but it is not an authority that mutates persistence directly.

## Supporting points

- Lisp expressions must compile to `TransactionPlan`, `QueryPlan`, `ProjectionPlan`, or `EffectPlan` before execution.
- Authored Lisp forms are input surfaces; any later kernel-derived Lisp output is a materialization, not the authority itself.
- The kernel validates compiled plans against types, invariants, and capabilities.
- This preserves extensibility without turning macros into a hidden privileged persistence API.

## Related atoms

### Depends on

- [depends_on:: [[primitive-operation]]]
- [depends_on:: [[kernel-api]]]
- [depends_on:: [[capability-model]]]

### Supports

- [supports:: [[transaction-plan]]]
- [supports:: [[query-plan]]]
- [supports:: [[projection-plan]]]
- [supports:: [[effect-plan]]]
- [supports:: [[query-engine]]]
- [supports:: [[hook-runtime]]]
- [supports:: [[python-cli-orchestration-layer]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
