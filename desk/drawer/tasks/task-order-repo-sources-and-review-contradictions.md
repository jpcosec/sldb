---
id: task-order-repo-sources-and-review-contradictions
status: open
summary: Define source-authority order for this planning workspace and record source contradictions that need normalization.
tags:
- workspace:desk
- artifact:task
- system:sldb
history: ["2026-07-29: opened for planning-only source ordering and contradiction review."]
references:
- desk/atoms/canonical-ast.md
- desk/atoms/decision-v1-parity-before-scope-expansion.md
- desk/atoms/decision-rust-core-with-minimal-python.md
- desk/atoms/decision-graph-store-over-yaml-indexes.md
- desk/atoms/decision-links-and-anchors-are-canonical.md
- docs/architecture/target-system-overview.md
pills:
- desk/contexts/pill-planning-contracts.md
files:
- docs/architecture/contracts/repo-source-order-and-contradiction-review.md
checklists: []
---

# Order repo sources and review contradictions

## Rationale

The workspace already has frozen Phase 1 contracts, target architecture notes, historical reports, and workflow artifacts. A single ordering rule is needed so planning stays deterministic and historical docs do not override current contract truth.

## Goal

Define the authority order for repo sources and identify current contradictions or stale statements between workspace docs.

## Scope

- **In-Scope**:
  - source-authority order for this planning worktree
  - contradictions between README/FAQ/desk/architecture/reports
  - Phase 1 scope ambiguities that could misroute planning
- **Out-of-Scope**:
  - runtime implementation
  - code parity claims
  - file moves or non-planning cleanup

## Implementation Path

1. Recover workspace guardrails and desk routing.
2. Compare current contract docs, architecture docs, and historical reports.
3. Write one contract artifact with precedence rules, contradictions, and normalization decisions.

## Validation

- Does the artifact cite governing atoms and target architecture docs?
- Does it define one unambiguous source order?
- Does it mark stale or lower-authority sources explicitly?
- Does it avoid implementation claims?

## Done When

The `repo-source-order-and-contradiction-review.md` contract exists and captures the authority order plus contradiction review for the current planning workspace.
