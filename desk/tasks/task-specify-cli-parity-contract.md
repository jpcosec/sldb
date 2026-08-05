---
id: task-specify-cli-parity-contract
status: closed
summary: Re-anchored to high-fidelity contract in docs/architecture/contracts/cli-parity-contract.md.
tags:
- workspace:desk
- artifact:task
- system:sldb
history:
- "2026-07-29: closed with high-fidelity contract artifact."
- "2026-08-01: replaced stale `sldb_cli` artifact reference with the `cli_client` artifact defined in target-runtime.yml."
references:
- desk/atoms/cli-workflow-surface.md
- desk/atoms/docs-command-group.md
- desk/atoms/ast-command-group.md
- desk/atoms/fields-command-group.md
- desk/atoms/stores-command-group.md
- desk/atoms/models-command-group.md
- desk/atoms/sections-command-group.md
- desk/atoms/find-command-group.md
- desk/atoms/faq-command-group.md
- desk/atoms/help-command-group.md
- desk/atoms/plural-first-cli-surface.md
- desk/atoms/cli-invocation-contract.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-runtime.yml
depends_on: []
pills:
- desk/contexts/pill-planning-contracts.md
files:
- docs/architecture/contracts/cli-parity-contract.md
checklists: []
---

# Specify CLI Parity Contract

## Rationale

Anchored in `plural-first-cli-surface.md`. The CLI is the primary product surface. To minimize user friction during the refactor, we must ensure that the command tree is preserved exactly as specified in the `target-components.yml`.

## Goal

Define the exact command-group surface and mandatory flags. Ensure that the Python orchestration layer correctly maps to the Rust-backed `StoreBackedMode` and `DirectMode`.

## Scope

- **In-Scope**: 
  - All 10+ command groups from `target-components.yml`: `docs`, `ast`, `fields`, `sections`, `stores`, `models`, `find`, `faq`, `help`.
  - JSON and Text output formats for all commands.
  - Standard flags: `-r/--recursive`, `-f/--format`, `-o/--output`.
- **Out-of-Scope**: 
  - Interactive "Shell" mode.
  - Visual/GUI elements.

## Implementation Path

1. **Interface Mapping**: Align the `PythonCLI` contains list from `target-components.yml` with the FFI call patterns.
2. **Mode Definition**: Specify which commands operate in `DirectMode` vs `StoreBackedMode`.
3. **UX Constraint**: Bind `cli-invocation-contract.md` to the implementation rules.
4. **Contract Materialization**: Write the specification in `docs/architecture/contracts/cli-parity-contract.md`.

## Validation

- Does the contract match the `CommandGroups` list in `target-components.yml`?
- Does it require mandatory JSON output support?
- Does it align with the `cli_client` artifact in `target-runtime.yml`?

## Done When

The high-fidelity `cli-parity-contract.md` is committed and approved.
