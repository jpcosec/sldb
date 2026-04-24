# Current System Overview

This document captures how SLDB works today, not the proposed future features in the temporary `desk/` notes.

## What Exists Now

- A Python library for reversible Markdown <-> Pydantic model workflows
- A CLI with direct commands: `extract`, `render`, `validate`, `init`, `example`
- A store subsystem under `.sldb/` for model registration, document tracking, and hash-based integrity checks
- Local store discovery, with a placeholder global store path concept via `~/.sldb/`
- No implemented tree indexing (`st`), semantic indexing (`se`), `recover`, or `compose` yet

## Core Runtime Layers

1. `StructuredNLDoc` models define the document contract and enforce per-field descriptions.
2. The Markdown engine parses templates and Markdown, extracts typed values, and renders Markdown back.
3. Validation helpers perform roundtrip/idempotency checks.
4. The CLI exposes library and store workflows.
5. The store subsystem writes YAML indexes and Merkle-style hashes.

## Store Shape Today

```text
.sldb/
  store_index.yaml
  models/<Model>.yaml
  documents/<Model>.yaml
```

Hash chain:

- `hash_c`: raw markdown content hash
- `hash_d`: extracted field payload hash
- `hash_b`: per-model documents index hash
- `hash_a`: top-level store models layer hash

## Current Constraints

- Model fields must have non-empty Pydantic descriptions
- Registered models are identified by import ref and class name
- Tracked documents are grouped by registered model
- Diagnostics treat missing documents and changed extracted payloads as failures
- Federation today is only linked-store registration in `store_index.yaml`; there is no global store-of-stores implementation yet

## Diagrams

- `docs/architecture/spec2viz/current-components.yml`
- `docs/architecture/spec2viz/current-store-lifecycle.yml`
- `docs/architecture/spec2viz/current-runtime.yml`

Rendered Mermaid outputs are in `docs/architecture/spec2viz/rendered/`.
