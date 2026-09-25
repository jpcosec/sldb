---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-25T10:28:38'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Volatile/ledger models still fold into hash_b and hash_a, so a read-only audit dirties versioned files

_Describe the incoming message with enough evidence to triage._

## Issue

A tracked model whose documents are pure session evidence still mutates the store's Merkle root. There is no way to declare a model as volatile, so its document count leaks into versioned files.

Concretely, `pron.models:MoveDoc` (one document per conversation turn) is tracked in `AgentsKBs/knowledge_antonia-cobranza`. Running `python3 -m worlds audit antonia-cobranza` (56 M1 queries) produced:

```
 core/models/MoveDoc.yaml
-hash_b: 3cb2e418...  documents_count: 398
+hash_b: 2e8b572a...  documents_count: 454     # +56, exactly one per turn

 core/store_index.yaml
-hash_a: 96479ae3...
+hash_a: d6224713...
```

Both files are versioned, so a read-only audit leaves the repo dirty.

## Why this is an sldb concern, not a consumer workaround

The chain is owned by sldb:

- `store/ops.py:53` — `m_idx.hash_b = documents_hash.hash_b_of(...)`, `documents_count` next to it
- `store/hashing.py:hash_models_layer` — folds **every** model's `hash_b` into `hash_a`

So `core/` vs `runtime/` today means *source identity vs derived index*, not *durable vs ephemeral*. Every tracked model lands in `core/` unconditionally.

`MoveDoc` already declares `__family__ = "ledger"` and `__semantics__` with `type.pron.move`, and `store/edge_index/shard_reading.py:30` comments that leaving pron's ledger out of the edge index "is the reader's choice". The intent that a ledger is different is already expressed — it just has no effect on placement or hashing.

Grepped for an existing escape hatch: `runtime_only`, `core_only`, `volatile`, `ephemeral`, and hash_a exclusions. None exist.

## What the consumer is forced into

A partial `.gitignore` that cannot be completed:

| Path | Ignorable | Result |
|---|---|---|
| `core/documents/MoveDoc/` | yes | the MoveDocs stay out |
| `core/models/MoveDoc.yaml` | no | `documents_count` + `hash_b` leak |
| `core/store_index.yaml` | no | `hash_a` leaks |

Ignoring the last two is not available: it would blind `sldb stores check` for the genuine models in the same store.

## Suggested direction

A first-class volatile/ledger model declaration whose documents are tracked and queryable but excluded from `hash_b` / `hash_a`, so a store's Merkle root depends only on durable knowledge. `__family__ = "ledger"` may be the natural carrier.

## Relation to an open note

`20260904-000000-suggestion-move-sldb-gitignore-policy-to-sldb` asks for a lint asserting `core/` is versionable and `runtime/` is ignored. That assumes the split is already correct. This note is the counterexample: a model for which the split itself is wrong, so the requested lint would currently codify the leak. Worth resolving together.

## Evidence

- Repo: `AntonIA/repos/AgentsKBs`, branch `dev`, KB `knowledge_antonia-cobranza`
- Reproduce: `python3 -m worlds audit antonia-cobranza && git status --short`
- `sldb stores check` PASSes both before and after — the store is not corrupt, it is correctly hashing data that should not be hashed
