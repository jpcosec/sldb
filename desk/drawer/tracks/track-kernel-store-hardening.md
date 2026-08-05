---
id: track-kernel-store-hardening
status: proposed
summary: Bundle store hardening, compatibility, retention, backup, observability, and failure-mode work after the first slice foundation exists.
tags:
- workspace:desk
- artifact:track
- system:sldb
history:
- "2026-07-29: drafted as interstitial planning layer between features and promotable tasks."
references:
- core_README.md
- libraries_core.md
- plan_core.md
items:
- desk/drawer/features/feature-canonical-graph-store-hardening.md
- desk/drawer/features/feature-migrations-and-compatibility.md
- desk/drawer/features/feature-garbage-collection-and-retention.md
- desk/drawer/features/feature-backup-export-import.md
- desk/drawer/features/feature-observability-and-diagnostics.md
- desk/drawer/features/feature-failure-model-and-operational-modes.md
---

# Kernel and store hardening track

## Goal

Group the operational hardening work needed to move from first-slice functionality to robust product behavior.

## Promotion order inside the track

1. Canonical graph-store hardening
2. Migrations and compatibility
3. Garbage collection and retention
4. Backup export import
5. Observability and diagnostics
6. Failure model and operational modes

## Needs design or grounding before promotion

- hardening vs new-feature sequencing
- minimum safe-store bar before retention or backup work
- exact operator surfaces for verify/recover/diagnose flows
