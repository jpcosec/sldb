---
id: issue-sldb-model-source-path-not-portable
status: closed
tags:
- system:sldb
- topic:stores
- topic:models
- topic:bug
related_tasks:
- desk/tasks/task-unify-store-context-and-federation.md
related_issues:
- desk/issues/issue-sldb-cross-store-write-and-model-resolution.md
---

# SLDB: model source resolution by stored `path` breaks on copied or relocated stores

## Problem

`models template show` (and anything going through `registered_model_source`) locates a model's `.py` by the `path` recorded in the store, re-anchored to the *current* project root. The `model_ref` is resolved correctly and serves as a fallback, but the path lookup is attempted first.

This fails with a bare `No such file or directory` when:

- the store is copied without its model sources
- the recorded `path` is absolute and came from another machine
- the store is consumed from a different project root than the one that wrote it

Recorded in `docs/user-manual.md` §13 as friction. It is a portability defect: the store claims to be self-describing state under `core/`, but one of its fields is only valid on the filesystem that wrote it.

## Why this is a bug, not friction

`.sldb/core/` is documented as versionable state (§4 of the manual). A field in versioned state that resolves only on the originating machine violates that. The failure mode compounds it: a filesystem error with no mention of the model, the store, or the available fallback.

## Relationship to tracked work

`task-unify-store-context-and-federation` (status `open`) owns the surrounding contract:

> "Context/root resolution, FAQ and explore anchoring, ancestor alias lookup, global registration and reconciliation, federation traversal and deduplication."

and its implementation path names `store/resolver.py` and `cli/store_context.py` — the same resolution layer this bug sits in. Its validation list already includes "moved stores", which is exactly the failing case here.

Also relevant: `issue-sldb-cross-store-write-and-model-resolution` (status `closed`) covered federated model resolution. Check what it settled before designing fallback ordering, so this does not contradict a decision already made.

This issue is narrower than the task: one concrete reproducible defect. It can land independently, but the fallback-ordering decision belongs to the task's contract.

## What's needed

- Always store `path` relative to the project root; reject or normalize absolute paths on `models add`.
- On resolution failure, fall back to `model_ref` before erroring.
- If both fail, error with: model name, attempted path, resolved absolute path, and the `model_ref` that was tried.
- `stores check` should flag non-portable model paths as a store health finding.

## Files to read first

- `src/sldb/cli/commands/models_utils.py` — `registered_model_source`, the shared resolution path
- `src/sldb/cli/commands/models_template.py:25` — `registered_model_source(args)` call site
- `src/sldb/api/model_drafts/model_source.py` — the `ModelSource` shape
- `.sldb/core/store_index.yaml` — how `path` and `model_ref` are persisted today

## Design considerations

- **Fallback ordering**: `model_ref` via `--pythonpath` is the more portable identifier. Consider trying it *first* and treating `path` as a hint.
- **Migration**: existing stores hold absolute paths. `stores update` should normalize them rather than requiring a manual fix.
- **No silent divergence**: if `path` and `model_ref` resolve to *different* files, that is a real conflict and must error, not pick one.
- Store health is SLDB-owned (pill-005), so the check belongs in `stores check`, not in a consumer.

## Task list

- [ ] **First**: read `issue-sldb-cross-store-write-and-model-resolution` (closed) for decisions already made on model resolution
- [ ] Confirm with `task-unify-store-context-and-federation` whether fallback ordering is its call
- [ ] Normalize `path` to project-root-relative on `models add`
- [ ] Implement ordered resolution with `model_ref` fallback in `registered_model_source`
- [ ] Replace the raw `FileNotFoundError` with a diagnostic naming model, both candidates, and the fallback tried
- [ ] Error on `path` / `model_ref` disagreement instead of silently preferring one
- [ ] Normalize legacy absolute paths during `stores update`
- [ ] Add a `stores check` finding for non-portable model paths
- [ ] Tests: copied store without sources, absolute foreign path, differing project root, conflicting path vs model_ref
- [ ] Update `docs/user-manual.md` §13

## Pills

- `desk/pills/pill-005-store-health-is-sldb-owned.md` — store integrity findings belong to SLDB's own check surface
- `desk/pills/pill-006-model-registration-is-queryable.md` — registration state must stay resolvable through the store
- `desk/pills/pill-009-cli-error-and-serialization-failure-mode.md` — raw file errors are not acceptable operator diagnostics

## Resolution

Closed: 2026-10-18
Reason: Resuelto: la fuente de un modelo se busca importando model_ref cuando el path guardado no es un archivo aquí (store copiado, path de otra máquina, modelo heredado); si tampoco importa, el error nombra el modelo y el store.
Refs: 66ed2d40dc, tests/api/test_model_source_portable.py, task-la-fuente-de-un-modelo-se-encuentra-por-model-ref-si-el-path-guardado-no-sirve
