---
layer: shared
id: threat-model
title: Threat model
five_wh_one_plus: why
tags:
- system:sldb
- domain:security-capabilities
provenance: source docs/core/also_core.md
---

# Threat model

## Answer

The threat model names the adversaries, abuse cases, and failure pressures that the kernel must resist or contain across documents, plugins, hooks, agents, effects, and external integrations.

## Supporting points

- It should cover malicious Lisp, untrusted plugins, path traversal, prompt injection in documents, resource exhaustion, recursive hooks, and data leakage.
- Threat modeling gives the capability system concrete adversaries instead of abstract permissions only.
- Security claims without an explicit threat model are underspecified.

## Related atoms

### Depends on

- [depends_on:: [[capability-model]]]
- [depends_on:: [[hook-runtime]]]

### Supports

- [supports:: [[agent-provider]]]
- [supports:: [[effect-outbox]]]
- [supports:: [[semantic-provider]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
