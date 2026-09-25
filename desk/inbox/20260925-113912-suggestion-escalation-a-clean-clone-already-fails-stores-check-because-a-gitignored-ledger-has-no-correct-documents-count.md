---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-25T11:39:12'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Escalation: a clean clone already fails stores check because a gitignored ledger has no correct documents_count

_Describe the incoming message with enough evidence to triage._

## Escalation of 20260925-102838

Follow-up evidence on the volatile-ledger hash leak. The consequence is worse than first reported: **a fresh clone of a pristine branch fails `sldb stores check` immediately**, with no local mutation involved.

## Reproduction, from a clean clone

```
git clone <AgentsKBs> cl -b dev      # dev untouched, nothing stashed
cd cl
ls .sldb/core/documents/MoveDoc/ | wc -l   -> 0      (gitignored, as intended)
grep documents_count core/models/MoveDoc.yaml -> 398 (committed)
sldb stores check --store knowledge_antonia-cobranza/.sldb -> FAIL
```

Failure detail: `MoveDoc hash_b_ok False`, `baddocs 0`, `hash_a_ok True`. Only the model-level hash is wrong; no document is corrupt.

## Why this has no correct value

The ledger documents are correctly gitignored (session evidence, not knowledge). But `documents_count` and `hash_b` live in a versioned file and are derived from documents that, by design, are absent from every clone.

- committing `398` (current) — wrong, clone has 0
- committing `454` (after an audit) — equally wrong
- committing `0` — wrong for every working tree that has ever run a turn

There is no value that satisfies both a clone and a live tree simultaneously. The consumer cannot fix this at any layer available to it, which is why AgentsKBs `ccaeed98` deliberately leaves the stale `398` in place rather than churning it.

## Sharpened implication for the requested lint

`20260904-000000` asks for a lint asserting `core/` is versionable and `runtime/` is ignored. As things stand that lint cannot pass on any store containing a ledger model: `core/models/<Ledger>.yaml` is versioned but not reproducible from versioned inputs. The volatile-model concept appears to be a prerequisite for that lint, not an independent nice-to-have.

## Suggested acceptance test

A store with a ledger model, all its documents absent, should pass `stores check` from a clean clone.
