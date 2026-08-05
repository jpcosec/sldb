---
id: feature-backup-export-import
status: proposed
summary: Define canonical export, backup, restore, and import flows for durable portability and disaster recovery.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- also_core.md
- libraries_core.md
- desk/atoms/backup-export.md
- desk/atoms/store-recovery.md
- desk/atoms/store-infrastructure.md
- docs/architecture/spec2viz/target-runtime.yml
- docs/architecture/spec2viz/target-store-graph.yml
depends_on:
- feature-canonical-graph-store-hardening
---

# Backup export import

## Goal

Define the macrotask for portable backup/export packages and restore/import flows over canonical persistence.

## Includes

- export package boundary
- backup policy
- restore/import behavior
- integrity validation on restore
- portability constraints

## Excludes

- live sync protocols
- unrelated UI work

## Needs design or grounding before promotion

- exact export package contents
- restore overwrite/merge policy
- cross-version restore guarantees
- operator workflow for disaster recovery
