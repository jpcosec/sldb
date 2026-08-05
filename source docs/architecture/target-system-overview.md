# Target System Overview

This document captures the current target architecture direction for the SLDB refactor.

## Main Direction

- **Phase 1**: replicate the required v1-visible workflows without changing kernel authority
- the kernel is Rust-owned
- the canonical persistence model is an append-only immutable revisioned graph
- canonical AST is the structural substrate for authored document families within that kernel model
- links and anchors are canonical kernel/store concepts, not late projections
- model = empty canonical graph/document state
- render round-trips for reversible document families must stay exact
- external interfaces are adapters around the kernel, not alternate authorities
- Python may remain a CLI/orchestration adapter for Git-facing flows, but it is not the architectural center
- no semantic baseline expansion now beyond existing parity needs

## Graph Store Direction

The current YAML-index-first store should evolve into an **append-only, immutable graph-store-first** local `.sldb/` workspace.

Keep from v1:

- local project store
- tracked document workflow
- integrity checks
- indexes and rebuilds
- semantic export boundary

Change internally:

- persist canonical documents, revisions, nodes, and typed edges
- persist canonical structural AST data for authored document families
- persist canonical links and anchor nodes
- treat hashes as canonical fields, not adapter-specific metadata
- allow relations to carry extensible payload structures
- materialize section/field/search/semantic views as derived indexes behind replaceable storage/query adapters

## Reversible And Non-Reversible Families

There are two broad document families.

### Reversible families

These support the strong cycle:

- AST -> render -> AST -> render

The rendered text must remain equal across the cycle.

### Non-reversible families

These may still have partial structure or family-specific addressing:

- PDF by XML/page or similar locator
- HTML by DOM-like locator
- code by tree-sitter locator
- plain text by char/paragraph/page locator

These still participate in anchoring, but not necessarily in the same reversible contract.

## Spec2viz diagrams

- `docs/architecture/spec2viz/target-components.yml`
- `docs/architecture/spec2viz/target-runtime.yml`
- `docs/architecture/spec2viz/target-store-graph.yml`
- `docs/architecture/spec2viz/target-anchoring.yml`
