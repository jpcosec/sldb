# Procedures and Rituals

This file captures the operating procedures for working in the SLDB codebase.

## Pills (Context)

A pill is a wiki-compiler query result. It is the context needed to understand a task.

- Pills are derived, not stored.
- If a pill is wrong, fix the source wiki node, not the query result.

## Session Initialization Ritual

Before starting any work:

```
1. READ SELF-DOCS  → Read WhoAmI, WhatAmI, HowAmI, WhereAmI, WhenAmI, WhyAmI
2. CHECK STATUS    → git status --short
3. CLEAN IF NEEDED → Commit or stash before starting (OP-6)
```

## Task Closing Ritual (OP-4)

When a task is done:

```
1. TEST    → Run relevant tests. All must pass.
2. LOG     → Update changelog.md.
3. DELETE  → Remove task file.
4. BOARD   → Update desk/tasks/Board.md.
5. COMMIT  → Atomic commit naming the task.
```

## Self-Healing Ritual

When energy is high or drift is detected:

```
1. SENSE   → Run wiki-compiler energy to measure entropy.
2. QUERY   → wiki-compiler query <question> to find relevant nodes.
3. REVISE  → Update stale nodes, add missing edges, generate facets.
4. CLEANSE → wiki-compiler cleanse --scan to propose structural fixes.
5. APPLY   → wiki-compiler cleanse --apply to accept beneficial changes.
6. AUDIT   → wiki-compiler audit to verify compliance.
7. BUILD   → wiki-compiler build to synchronize graph.
8. COMMIT  → Atomic commit documenting the healing cycle.
```

## Pre-Completion Audit

Before marking a task done:

```
1. GIT    → Does git history confirm the change?
2. TESTS  → Do they pass?
3. TREE   → Is the tree clean?
```

## Commit Triggers

| Situation               | Commit? |
|--------------------------|---------|
| Task closed              | Yes     |
| Self-healing cycle       | Yes     |
| Structural wiki change   | Yes     |
| Session ended            | Yes (trail collect) |
| Half-written work        | No      |

## What NOT to Do

- Edit with a dirty tree (OP-6)
- Trust task files over git history
- Fix query results instead of source nodes
- Reference zones above current layer