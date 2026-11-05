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

# Keep SLDB generic: it evaluates rules over documents, edges and hashes; deskops authors them

## What

_Define the context or guardrail this pill carries._

SLDB owns structured Markdown contracts, stores, validation, generic navigation/query surfaces, and the generic evaluation of declared rules over documents, edges and content hashes (predicates with quantifiers over relations, rule documents, hash-pinned document anchors, transitions as edge data). Which rules exist, what a task type is, and what a workflow gate means is authored by deskops as documents; SLDB only evaluates them. Owner decision 2026-11-04: operativizar lo más posible en sldb, modificándolo a fondo si hace falta (desk/drawer/plans/grafo-operable/decisiones.md, D1).

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

Keep SLDB text-first: the graph and every evaluated rule are derived from documents and rebuildable. Add generic capabilities (rule evaluation, predicate language, document anchors, state machine over edges) only in a form any consumer can author with its own documents. Route desk-specific lifecycle content (which states, which gates, which task types) toward deskops documents.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not hard-code desk-specific lifecycle rules, task types, inbox staging semantics or orchestration as SLDB behavior. Do not refuse a generic rule-evaluation capability on the ground that deskops is its first consumer: the boundary is 'generic evaluator in sldb, specific rules authored outside', not 'no rules in sldb'. Do not build actor authentication into SLDB: identity comes from git and the execution layer.
