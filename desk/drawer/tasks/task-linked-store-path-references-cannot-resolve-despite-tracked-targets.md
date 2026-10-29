---
id: task-linked-store-path-references-cannot-resolve-despite-tracked-targets
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Linked store path references cannot resolve despite tracked targets

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261021-033635-unclear-linked-store-path-references-cannot-resolve-despite-tracked-targets.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261021-033635-unclear-linked-store-path-references-cannot-resolve-despite-tracked-targets.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

While resolving MEPU reports in deskops, reproduced sldb edges unresolved showing the 11 Board pills/ritual paths as unknown_path only through a linked store. All targets exist and are tracked; local edges unresolved is empty. Root cause: declared_resolution._resolve only uses owners when store is None; composition_targets._owners_by_path excludes linked docs. Expected: resolve relative paths within the source store namespace, preserving isolation when consumer/provider paths collide. Reproduction without MEPU: compose deskops .sldb as linked alias deskops and inspect source deskops:BoardDoc:Board. Deskops will use existing supported bare tracked document names for its Board pills/rituals, with federation regression tests; no SLDB runtime workaround planned.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
