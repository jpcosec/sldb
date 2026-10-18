---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-04T12:00:00'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T13:45:01'
---

# Move .sldb gitignore core/runtime policy into sldb

_Describe the incoming message with enough evidence to triage._

## Issue

The `.sldb` gitignore policy is being linted locally in deskops, but the rule belongs at the `sldb` layer.

## Why

`sldb` owns the core/runtime split:

- `.sldb/core/` is durable and should be trackable.
- `.sldb/runtime/` is local runtime state and should be ignored.

Deskops can enforce this for its repo, but the reusable policy and lint behavior should be defined by `sldb` so other projects do not reimplement it.

## Required Follow-Up

Add this to the `sldb` inbox as a requested improvement: provide a first-class lint/check that verifies `.sldb/core` is versionable and `.sldb/runtime` is ignored.

## Local Context

Deskops currently has `tests/test_gitignore_policy.py` as a local guard for this behavior.

## Tags

- system:sldb
- system:deskops
- topic:gitignore-policy
- topic:core-runtime-split

## Resolución

Resuelto (2026-10-18, sldb-04). f9c0babfb6: `stores check` anota cuando las reglas de ignore del repo dejan `.sldb/core` ignorado o `.sldb/runtime` sin ignorar (evaluadas con `git check-ignore --no-index`), y `check_store` lo devuelve en `gitignore_policy`. deskops puede reemplazar su tests/test_gitignore_policy.py por eso. Test: tests/api/test_gitignore_policy.py.
