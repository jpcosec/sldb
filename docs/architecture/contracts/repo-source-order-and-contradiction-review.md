# Repo Source Order and Contradiction Review

## Purpose and governing sources

This contract orders the authoritative sources in this planning workspace and records the current contradictions that must not be allowed to override frozen Phase 1 contract truth.

Governing atoms:
- `desk/atoms/canonical-ast.md`
- `desk/atoms/decision-v1-parity-before-scope-expansion.md`
- `desk/atoms/decision-rust-core-with-minimal-python.md`
- `desk/atoms/decision-graph-store-over-yaml-indexes.md`
- `desk/atoms/decision-links-and-anchors-are-canonical.md`

Target architecture docs:
- `docs/architecture/target-system-overview.md`
- `docs/architecture/spec2viz/target-components.yml`
- `docs/architecture/spec2viz/target-runtime.yml`

## In-scope

- define source-authority order for the current planning worktree
- classify which documents are binding, derived, or historical
- record contradictions that could misroute planning

## Explicit non-goals

- no runtime implementation claims
- no repo file moves
- no parity attestation from code
- no Phase 2 scope expansion

## Source-authority order

Use this order when sources disagree.

1. `also_core.md`
2. `core_README.md`
3. `diagramas_core.md`
4. `interfaces.md`
5. `libraries_core.md`
6. `plan_core.md`
   - These six files define the primary kernel/core architecture direction.
7. `desk/atoms/`
   - Durable concept truth after the core docs.
8. `AGENTS.md`, `README.md`, `docs/faq.md`
   - Workspace guardrails and planning-only scope.
9. `docs/architecture/contracts/`
   - Lower-authority contract materializations that must align upward.
10. `docs/architecture/target-system-overview.md` and `docs/architecture/spec2viz/target-*.yml`
   - Summary/projection documents.
11. `desk/tasks/Board.md`, task docs, pills, rituals
   - Workflow routing and validation rules.
12. `docs/architecture/phase-1-resolution-pack.md` and `docs/architecture/phase-1-macro-implementation-plan.md`
   - Historical planning inputs.
13. `docs/reports/`
   - Historical audits only.

## Repo order by function

- root core docs = primary architecture authority
- `desk/atoms/` = durable concept truth after the core docs
- `docs/architecture/contracts/` = aligned contract materializations
- `docs/architecture/spec2viz/` = diagram projections
- `docs/architecture/target-system-overview.md` = concise target summary
- `desk/tasks/` + `desk/contexts/` + `desk/rituals/` = workflow harness state
- superseded historical analysis should live in Git history rather than in the live KB

## Contradiction review

### 1. `docs/README.md` vs actual `docs/` contents

- Resolved.
- `docs/README.md` now reflects `contracts/`, planning packs, and `reports/`.

### 2. Planning-only workspace vs prior historical review material

- Resolved by KB policy.
- Superseded review material belongs in Git history, not in the live planning workspace.

### 3. Current board state vs prior historical audit material

- Resolved by KB policy.
- Board and task files remain current workflow truth; stale audit material should not remain in the live KB.

### 4. Phase 1 family scope: `phase-1-parity-contract.md` vs `rust-canonical-core-contract.md`

- Resolved.
- `rust-canonical-core-contract.md` now states Markdown parity is the Phase 1 requirement and HTML/JSON are optional later projections.

### 5. Long-term family overview vs Phase 1 scope lock

- Resolved.
- `target-system-overview.md` now distinguishes kernel direction from narrower Phase 1 obligation.

### 6. Open architectural gaps in `phase-1-resolution-pack.md` vs closed contract board

- Resolved by authority classification.
- The closed board and existing contract artifacts win; the resolution pack is historical planning context.

## Normalization rules

- Treat the six root core docs as primary architecture authority.
- Treat atoms as durable concept truth after those core docs.
- Treat contract docs as lower-authority materializations that must align upward.
- Treat overview/spec2viz as summary/projection documents.
- Treat board/task/pill/ritual files as workflow truth, not architecture truth.
- Treat superseded reports as Git-retained history, not as live KB material.
- Treat older planning packs as historical unless re-anchored by an active task or a current contract.

## Downstream constraints

- No future planning task may cite deleted historical reports as authority over atoms, contracts, board state, or workspace guardrails.
- Any future doc that summarizes `docs/` contents must include `contracts/`, `reports/`, and planning packs or explicitly mark itself partial.
- Any Phase 1 work that mentions non-Markdown emitters or non-reversible families must state whether it is long-term direction or Phase 1 obligation.
- Any new contradiction review must use this precedence order unless replaced by a newer contract.
