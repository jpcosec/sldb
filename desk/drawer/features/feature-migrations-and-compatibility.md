---
id: feature-migrations-and-compatibility
status: proposed
summary: Define versioning, migration units, compatibility metadata, and upgrade rules for canonical persistence and surface contracts.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- core_README.md
- libraries_core.md
- plan_core.md
- desk/atoms/compatibility-surface.md
- desk/atoms/migration-unit.md
- desk/atoms/store-infrastructure.md
- docs/architecture/spec2viz/target-store-graph.yml
depends_on:
- feature-rust-kernel-foundation-first-slice
---

# Migrations and compatibility

## Goal

Define the macrotask for persistence evolution without breaking canonical meaning, recoverability, or supported product surfaces.

## Includes

- compatibility metadata
- migration units
- format/version tracking
- upgrade rules
- downgrade or read-older-data policy

## Excludes

- unrelated feature expansion
- silent breaking schema drift

## Needs design or grounding before promotion

- migration grain and ordering
- compatibility guarantees per surface
- rollback policy
- fixture coverage for migration attestation
