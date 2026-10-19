---
# pill-xxx
id: pill-context-pills-carry-reasoning-not-a-copy-of-code-or-docs
status: active
summary: Qué es una pill, cómo se clasifica y cuándo se retira.
# e.g., language:python, library:pydantic
tags:
- system:sldb
- workspace:desk
- topic:governance
---

# Context pills carry reasoning, not a copy of code or docs

## What

_Define the context or guardrail this pill carries._

A context pill is pre-drafted rationale that makes a task unambiguous. Write one before implementation when the task depends on rationale, constraints, terminology or boundaries that are not obvious from code or durable docs. Each pill captures why this approach over the alternatives, what constraints or guardrails drive the decision, where in the codebase the changes apply, how the pattern or model informs the implementation, the language (terminology conventions, naming rules), and its scope (context versus implementation artifact).

## Why

_Explain why this context matters for safe execution._

Code is truth, docs are the index, and context is reasoning: a subset of a subset. A pill that repeats code or docs drifts from them and starts saying something false.

## When

_Describe when an agent should apply this pill._

Apply when writing, binding or auditing a pill: before a task that needs unwritten rationale, after each execution step (the context audit of the execution ritual), at closeout, and when a phase ends.

## Where

_Name the files, surfaces, or scope this pill applies to._

- desk/contexts/ (pills)
- the pills field of each task and of the Board
- desk/rituals/execution.md, closeout.md and phase.md, which run the audits

## How

_Describe the correct way to apply this guidance._

Classify a pill along these dimensions:

| Dimension | Values / Meaning |
| --------- | ---------------- |
| Type | guardrail, decision, pattern, model, warning |
| Scope | global, domain, component, feature, task |
| Nature | context (rationale), implementation (artifact guidance), operational (workflow rule) |
| Language | Human language or implementation language affected by the pill |
| Bound To | Task, component, command, document, model, or workflow surface the pill applies to |
| Lifecycle | draft, current, deprecated, superseded |
| Owner | Human, agent, repo area, or downstream system responsible for keeping it accurate |
| Review Trigger | Event that should force re-audit, such as task close, API change, model change, or failed validation |

Lifecycle: drafted, bound to a task, audited after each step. Still needed: keep it. Redundant with code or docs: retire it. Complete: move its knowledge into code or docs, then retire or deprecate it (deskops retire, with the commit that holds the knowledge as ref).

## How Not

_Describe the shortcut or failure mode to avoid._

- Do not let pills drift from code or docs (redundant or stale).
- Do not keep a pill after its knowledge has been explicitly moved into code or docs.
- Do not repeat in a pill what code or docs already say.
