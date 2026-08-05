---
layer: shell
id: cli-invocation-contract
title: CLI invocation contract
five_wh_one_plus: how
tags:
- system:sldb
- domain:surfaces-cli-inputs-outputs
provenance: source docs/sldb-v1/README.md
---

# CLI invocation contract

## Answer

Run SLDB as `sldb ...` or `python -m sldb ...`; `bash sldb ...` is incorrect because `sldb` is an entrypoint, not a shell script.

## Supporting points

- The invocation contract is explicit in the v1 docs.
- This is a stable user-facing usage rule, not an internal implementation detail.
- The refactor should preserve the same invocation model.

## Related atoms

### Constrains

- [constrains:: [[cli-workflow-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
