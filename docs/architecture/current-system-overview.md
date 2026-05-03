# Current System Overview

This document captures how SLDB works today, not the proposed future features in the temporary `desk/` notes.

## What Exists Now

- A Python library for reversible Markdown <-> Pydantic model workflows
- A CLI with direct commands for extract/render/validate, link recovery/composition, and store navigation
- A store subsystem under `.sldb/` for model registration, document tracking, hash-based integrity checks, semantic indexes, and linked-store federation
- Structural store navigation rooted at `st`
- Store-local semantic navigation rooted at `se`
- Federated semantic navigation rooted at `gse`
- Explicit Markdown links with `[[...]]` and transclusions with `![[...]]`

## Core Runtime Layers

1. `StructuredNLDoc` models define the document contract and enforce per-field descriptions.
2. The Markdown engine parses templates and Markdown, extracts typed values, and renders Markdown back.
3. Validation helpers perform roundtrip/idempotency checks.
4. The CLI exposes library, store, link, and query workflows.
5. The store subsystem writes YAML indexes, semantic artifacts, and Merkle-style hashes.

## Store Shape Today

```text
.sldb/
  store_index.yaml
  models/<Model>.yaml
  documents/<Model>.yaml
  semantic_dag.yaml
  semantic_index.yaml
```

Hash chain:

- `hash_c`: raw markdown content hash
- `hash_d`: extracted field payload hash
- `hash_b`: per-model documents index hash
- `hash_a`: top-level store models layer hash

Semantic artifacts:

- `semantic_dag.yaml`: store-local semantic node graph plus explicit equivalence mappings
- `semantic_index.yaml`: document-to-semantic-tag materialization

## Current Constraints

- Model fields must have non-empty Pydantic descriptions
- Registered models are identified by import ref and class name
- Tracked documents are grouped by registered model
- Diagnostics treat missing documents and changed extracted payloads as failures
- Global semantic federation remains explicit through linked stores and semantic equivalence mappings
- Structural queries are intentionally small-surface: `ls`, `get`, `glob`, and `find --where`
- Semantic tags are explicit model/document metadata, not inferred from prose

## Diagrams

- `docs/architecture/spec2viz/current-components.yml`
- `docs/architecture/spec2viz/current-store-lifecycle.yml`
- `docs/architecture/spec2viz/current-runtime.yml`

Rendered Mermaid outputs are in `docs/architecture/spec2viz/rendered/`.
