# SLDB Store Workspace

## Purpose

`.sldb/` is the project-local SLDB workspace. It keeps the repo's queryable store state close to the codebase while separating durable shared knowledge from ephemeral runtime state and machine-local configuration.

The store itself is part of the repo's operating surface, not a second codebase. Durable knowledge should become versioned models, tracked documents, and explicit policy. Runtime noise should stay rebuildable.

## Layout Summary

The target layout keeps one `.sldb/` root and splits responsibilities by role:

```text
.sldb/
  README.md
  core/
    models/
    documents/
    semantics/
    routines/
  runtime/
    indexes/
    locks/
    temp/
    drafts/
  .config/
    local.yaml
    pythonpath
```

`README.md` is the human and typed entrypoint for the store contract. `core/` is the durable shared layer. `runtime/` is disposable execution state. `.config/` is local override state that should not be required for another contributor to understand or rebuild the store.

## Durable Core (`.sldb/core`)

Put versioned shared store artifacts under `.sldb/core`. This layer is the durable contract other contributors should be able to pull, inspect, and rebuild without needing your machine-local state.

Typical `core/` contents include:

- model registrations and their indexes
- tracked durable document indexes
- store-owned policy docs and durable contract metadata
- reusable routines, policy packs, and store-owned metadata that define behavior rather than one execution session

Do not place locks, temp drafts, machine-local overrides, or cache-like rebuild products in `core/`.

## Runtime State (`.sldb/runtime`)

Put ephemeral execution-time state under `.sldb/runtime`. This subtree exists to support commands, rebuilds, validations, and active editing sessions without polluting the durable contract.

Typical `runtime/` contents include:

- lock files
- rebuildable semantic indexes, semantic DAGs, and section indexes
- temp drafts and scratch materializations
- active session outputs, transient caches, and other files safe to delete and regenerate

Anything under `runtime/` must be safe to recreate from the durable repo state plus local command execution.

## Local Config (`.sldb/.config`)

Put machine-local override state under `.sldb/.config`. This is where contributor-specific settings live when they should affect local behavior without changing the shared store contract.

Typical `.config/` contents include:

- local python path overrides
- editor or shell integration hints
- machine-specific store settings
- personal defaults that should not be required in CI or for other contributors

`.config/` is local by default. If a setting becomes required for everyone, promote it into code, docs, or a durable store artifact under `core/`.

## Promotion Rules

Only promote information into `.sldb/core` when it becomes part of the shared durable contract. Drafts, experiments, temp extracts, and session-specific notes begin in runtime surfaces and move into durable tracked documents only after validation.

Promotion follows this rule of thumb:

- if another contributor should pull it and rely on it, it belongs in `core/`
- if it only helps the current session run, it belongs in `runtime/`
- if it only affects one machine or one operator, it belongs in `.config/`

When runtime output reveals a stable policy or reusable model, rewrite or promote that result as a durable artifact instead of committing the raw runtime byproduct.

## Git Policy

Commit `.sldb/core` because it is the shared durable store contract. Ignore `.sldb/runtime` because it is ephemeral and rebuildable. Ignore `.sldb/.config` because it is local override state unless a specific file is explicitly declared shareable later.

The root `.sldb/README.md` is versioned because it explains the contract for the whole store. Model or document contract changes should land in normal git commits together with the code or docs they govern. Runtime cleanup should happen by deletion or rebuild, not by preserving transient files in history.

## Command Map

Common flows for the store are:

- register a model: `python -m sldb models add <module:Model> --store .sldb --pythonpath .`
- track a document: `python -m sldb docs track <path> --model <ModelName> --name <doc-name> --store .sldb --pythonpath .`
- rebuild indexes: `python -m sldb stores update --store .sldb --pythonpath .`
- remove a tracked document before deleting it: `python -m sldb docs untrack <doc-name> --store .sldb --pythonpath .`

Prefer the smallest command that updates the durable contract you actually changed. Use `stores update` after bulk edits or when tracked store metadata needs to be rebuilt coherently.

## Migration Status

The repo is currently in a transitional state: some store indexes still live at the `.sldb/` root while task-017 has not yet moved the implementation to explicit `core/`, `runtime/`, and `.config/` routing.

This README defines the target architecture now so the next migration work can route each file intentionally instead of preserving the old flat layout by accident.
