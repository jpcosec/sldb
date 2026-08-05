---
# board-xxx
id: board-001
scope: desk
tasks: []
pills:
- desk/contexts/pills.md
- desk/contexts/pill-planning-contracts.md
rituals:
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
tags:
- workspace:desk
- system:sldb
---

# sldb-refactor-worktree Board

## Purpose

Keep the active board clear until the first implementation promotion set is ready.

## Notes

- The contract-freezing pass is complete.
- The next promotion set is limited to the first implementation slice already agreed:
  - Rust kernel foundation
  - Lisp control/data surface
  - Markdown roundtrip first slice
- Those macrotasks are currently drafted in `desk/drawer/features/` and are not promoted yet.
- Embeddings and semantic-provider work are deferred and must not enter the first promotion set.
- No entry here claims implementation progress from this planning-only workspace.
- SpecYAML traceability layer closed (2026-08-04): specyaml is the machine-readable nexus between atoms and diagrams; vistas HTML is generated (`scripts/generate_vistas_html.py`) and drift-checked (`scripts/validate_spec_traceability.py`, 0 errors / 3 coverage warnings for vistas d03/d05/d06). See `desk/contexts/pill-specyaml-traceability.md`.

## Promotion queue

- `desk/drawer/features/feature-rust-kernel-foundation-first-slice.md`
- `desk/drawer/features/feature-lisp-control-and-data-surface-first-slice.md`
- `desk/drawer/features/feature-markdown-roundtrip-first-slice.md`
