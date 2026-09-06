---
kind: suggestion
sender_project: deskops
created_at: 2026-09-04T12:00:00
status: open
---

# Move .sldb gitignore core/runtime policy into sldb

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
