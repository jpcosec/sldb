# Documentation Contradiction Map

## Purpose and governing sources

This contract records one planning-only pass over repository documentation to find and classify contradictions.

Governing sources:

- `also_core.md`
- `core_README.md`
- `diagramas_core.md`
- `interfaces.md`
- `libraries_core.md`
- `plan_core.md`
- `README.md`
- `docs/architecture/target-system-overview.md`
- `docs/architecture/contracts/repo-source-order-and-contradiction-review.md`
- `desk/atoms/rust-core.md`
- `desk/atoms/canonical-ast.md`
- `desk/atoms/projection.md`
- `desk/atoms/lisp-metalanguage.md`
- `desk/atoms/markdown-text-surface.md`
- `desk/atoms/store-infrastructure.md`

## In-scope

- contradiction discovery across documentation and atoms
- authority-aware classification of contradictions
- differentiation between real contradictions, wording drift, and historical-only mismatches
- one explicit method that combines clustering and subagent review

## Explicit non-goals

- no runtime implementation claims
- no code-derived parity proof
- no automatic rewriting of docs in this pass
- no attempt to make embeddings the final authority

## Method used in this pass

This pass used both mechanisms the repo discussion proposed:

1. **Embedding-like clustering for discovery**
   - corpus size scanned: `231` Markdown docs
   - chunk count: `1125`
   - local semantic representation: `TF-IDF + TruncatedSVD + cosine nearest-neighbors`
   - cluster shape: neighbor graph plus connected components
   - candidate contradiction pairs found: `345`
2. **Subagent review for adjudication**
   - narrowed reviews were run over the highest-value concept families:
     - Rust/Python authority and canonical model
     - AST vs graph and Phase 1 parity scope
     - Lisp/Markdown/projection semantics
     - historical reports vs current authority docs

### Environment note

This worktree did not currently have `sentence-transformers` or `hdbscan` installed, so the clustering pass used the available local `scikit-learn` stack as a discovery approximation rather than a final semantic oracle.

## Source-authority rule used for adjudication

When two docs disagreed, this order governed the decision:

1. `also_core.md`
2. `core_README.md`
3. `diagramas_core.md`
4. `interfaces.md`
5. `libraries_core.md`
6. `plan_core.md`
7. `desk/atoms/`
8. workspace guardrails and then lower-authority contracts/docs/reports

Historical reports were treated as non-authoritative when they described superseded repo state.

## Results summary

This pass found four useful classes:

1. **Aligned**
   - the docs say the same thing with compatible wording
2. **Wording drift**
   - same architecture truth, but phrased in ways that can blur boundaries
3. **Real contradiction**
   - materially different acceptance bar, scope, or source-of-truth claim
4. **Historical-only mismatch**
   - stale reports or snapshots that conflict with current authority docs but are already downgraded correctly

## Aligned concepts

### Rust owns canonical authority

Status: **aligned**

Evidence:

- `README.md`
- `docs/architecture/target-system-overview.md`
- `docs/architecture/contracts/python-rust-ownership-and-ffi-contract.md`
- `docs/architecture/contracts/rust-canonical-core-contract.md`
- `desk/atoms/rust-core.md`

Resolution:

- No contradiction.
- The repo is consistent that Rust alone owns canonical invariants, revisions, transactions, hashing, persistence, and capability-checked effects.

### Python is optional orchestration, not authority

Status: **aligned**

Evidence:

- `README.md`
- `docs/architecture/target-system-overview.md`
- `docs/architecture/contracts/python-rust-ownership-and-ffi-contract.md`

Resolution:

- No contradiction.
- Python is consistently treated as an adapter/orchestration host.

### Markdown is not canonical authority

Status: **aligned**

Evidence:

- `desk/atoms/markdown-text-surface.md`
- `desk/atoms/markdown-importer.md`
- `desk/atoms/markdown-emitter.md`
- `desk/atoms/rust-core.md`

Resolution:

- No contradiction.
- Markdown is consistently treated as text surface plus import/export path around Rust-owned meaning.

### Lisp is not canonical authority

Status: **aligned**

Evidence:

- `desk/atoms/lisp-metalanguage.md`
- `desk/atoms/lisp-schema-language.md`
- `desk/atoms/lisp-macro-language.md`
- `desk/atoms/rust-core.md`

Resolution:

- No contradiction.
- Lisp is consistently treated as schema/macro/program surface mediated by the kernel.

## Wording drift that should be normalized

### Canonical model naming drifts between graph, graph-store, and append-only database

Status: **wording drift**

Evidence:

- `README.md` says the canonical persistence model is an immutable revisioned graph
- `docs/architecture/target-system-overview.md` says append-only immutable revisioned graph / graph-store-first
- `docs/architecture/contracts/python-rust-ownership-and-ffi-contract.md` says append-only database
- `docs/architecture/contracts/rust-canonical-core-contract.md` says graph-store

Resolution wording:

> The canonical model is a revisioned graph, persisted in an append-only immutable graph store.

### Rust core contract can read AST-centric instead of full-model-centric

Status: **wording drift**

Evidence:

- broader docs name documents, revisions, transactions, links, anchors, and provenance as canonical kernel concerns
- `docs/architecture/contracts/rust-canonical-core-contract.md` emphasizes AST, selectors, hashes, and relations more than the whole model envelope

Resolution wording:

> The Rust core is authoritative for the full canonical model: documents, revisions, nodes, typed edges, transactions, provenance, and the structural AST persisted within the append-only revisioned graph.

### Markdown and non-authority vocabulary drifts across atoms

Status: **wording drift**

Evidence:

- `system authority`
- `sovereign model`
- `existence itself`

Resolution wording:

> Markdown never owns canonical meaning or revisions; it is an input/output surface around Rust-owned canonical state.

## Phase/scope differences

### Phase 1 parity contract is narrower than the macro plan and resolution pack

Status: **Resolved by removal (2026-07-31)**

Evidence:

- `docs/architecture/contracts/phase-1-parity-contract.md`
- `desk/atoms/decision-v1-parity-before-scope-expansion.md`

Problem:

- older deleted planning packs described a broader closure surface including store lifecycle/integrity and store-backed inspection/query surfaces
- the live parity contract names the narrower closure floor centered on the initial parity slice

Adjudication:

- the deleted planning packs no longer participate in live KB authority
- parity wording is now governed by the frozen contracts and `desk/atoms/decision-v1-parity-before-scope-expansion.md`

Resolution wording:

> Resolved by removal (2026-07-31): the packs were deleted from the live KB and survive only in Git history; parity wording is governed by the frozen contracts and `desk/atoms/decision-v1-parity-before-scope-expansion.md`.

### Phase 1 acceptance bar mixes exact rendered equality with source-byte equivalence

Status: **Resolved by removal (2026-07-31)**

Evidence:

- `README.md`
- `docs/architecture/contracts/phase-1-parity-contract.md`
- `desk/atoms/decision-v1-parity-before-scope-expansion.md`

Problem:

- older deleted planning packs had mixed broader exact-render wording with a sharper byte-level acceptance bar for the initial Markdown-only family
- the live parity contract remains the authoritative acceptance bar for the initial reversible family

Adjudication:

- the deleted planning packs no longer participate in live KB authority
- parity wording is now governed by the frozen contracts and `desk/atoms/decision-v1-parity-before-scope-expansion.md`

Resolution wording:

> Resolved by removal (2026-07-31): the packs were deleted from the live KB and survive only in Git history; parity wording is governed by the frozen contracts and `desk/atoms/decision-v1-parity-before-scope-expansion.md`.

## Terminology issue resolved by glossary freeze

### `projection.md` and neighboring atoms had mixed projection/materialization/input language

Status: **resolved by glossary normalization**

Evidence:

- `desk/atoms/projection.md`
- `desk/atoms/projection-surface.md`
- `desk/atoms/markdown-text-surface.md`
- `desk/atoms/markdown-emitter.md`
- `desk/atoms/lisp-metalanguage.md`
- `desk/atoms/lisp-schema-language.md`
- `desk/atoms/lisp-macro-language.md`
- `docs/architecture/contracts/canonical-state-derivation-glossary.md`

Problem:

- projection, materialization, and authored input were being used too loosely
- that made Markdown output, authored Markdown, authored Lisp, and specialized graph views sound like one category

Adjudication:

- this was primarily a terminology problem rather than a deep architectural conflict
- the glossary freezes the cleaner model: authored input, canonical state, render/materialization, projection, and derived index
- maximum authority remains Rust-owned canonical state persisted in the database

Resolution wording:

> Use `projection` for structured specialized views over canonical state, `render/materialization` for representation output, and `authored input` for Markdown/Lisp content before kernel canonicalization.

## Historical material policy

Status: **applied policy**

- historical reports do not belong in the live KB
- Git history is the retention layer for superseded reports and stale snapshots
- future contradiction sweeps should exclude archived-or-deleted historical reports from the live corpus by default

## Discovery artifacts from this pass

Temporary local analysis artifacts were generated during this pass under `/tmp/doc-contradictions/` for discovery only:

- `summary.json`
- `clusters.json`
- `candidate_pairs.json`

They are not authority docs and should not be treated as durable repo truth.

## Downstream constraints

- future contradiction sweeps should keep the same two-stage model: clustering for discovery, adjudication for truth
- contradiction scoring must not be treated as self-justifying; final classification stays authority-aware and text-based
- the next cleanup pass should target wording normalization against the glossary, not the already-aligned areas
- historical reports should stay out of the live KB and out of the default contradiction corpus
- the embedding/clustering stack may use `fastembed`, `hdbscan`, or equivalent as long as authority-order adjudication stays the final rule

## Validation attestation

This artifact exists at the task-declared path, cites governing atoms and target docs, distinguishes contradiction classes, and makes no implementation progress claims.
