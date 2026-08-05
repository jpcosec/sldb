---
id: track-first-slice-foundation
status: proposed
summary: Bundle the first implementation promotion lane around Rust kernel authority, Lisp-authored control/data, Markdown roundtrip, CLI exposure, and conformance proof.
tags:
- workspace:desk
- artifact:track
- system:sldb
history:
- "2026-07-29: drafted as interstitial planning layer between features and promotable tasks."
references:
- also_core.md
- core_README.md
- plan_core.md
- docs/architecture/target-system-overview.md
items:
- desk/drawer/features/feature-rust-kernel-foundation-first-slice.md
- desk/drawer/features/feature-lisp-control-and-data-surface-first-slice.md
- desk/drawer/features/feature-markdown-roundtrip-first-slice.md
- desk/drawer/features/feature-cli-surface-implementation.md
- desk/drawer/features/feature-conformance-harness-and-fixtures.md
---

# First slice foundation track

## Goal

Group the first implementation wave into one coherent promotion track before it is broken into active tasks.

## Why this layer exists

- features are still too large to promote directly
- the board should promote bounded task sets, not raw macrotasks
- this track defines the first execution package and its dependency order

## Promotion order inside the track

1. Rust kernel foundation
2. Lisp control/data surface
3. Markdown roundtrip
4. CLI surface implementation
5. Conformance harness and fixtures

## Needs design or grounding before promotion

- exact task decomposition per feature
- exact inter-feature dependency cuts
- exact first CLI subset that proves the slice
- exact closure evidence required before Phase 1 packaging
