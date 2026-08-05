---
id: task-specify-specyaml-schema-contract
status: closed
summary: Closed with contract artifact docs/architecture/contracts/specyaml-schema-contract.md plus spec2viz normalization (views + atoms fields, manifest).
tags:
- workspace:desk
- artifact:task
- system:sldb
history:
- "2026-08-04: closed with contract artifact; spec2viz ymls normalized to schema (views:, atoms:, version 0.3); manifest.yml added."
references:
- desk/atoms/concept-binding.md
- desk/atoms/ports-and-adapters.md
- desk/atoms/graph-projection.md
- docs/architecture/target-system-overview.md
- docs/architecture/contracts/atom-ontology-map.md
depends_on: []
pills:
- desk/contexts/pill-planning-contracts.md
- desk/contexts/pill-specyaml-traceability.md
files:
- docs/architecture/contracts/specyaml-schema-contract.md
- docs/architecture/spec2viz/manifest.yml
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-store-graph.yml
- docs/architecture/spec2viz/target-runtime.yml
- docs/architecture/spec2viz/target-anchoring.yml
checklists: []
---

# Specify SpecYAML Schema Contract

## Rationale

Specyaml is the documental nexus between `desk/atoms/` and the diagram
projections. Without a schema, the four `spec2viz/*.yml` diverge and the
edge to atoms stays implicit.

## Goal

Define the required shape of every specyaml document: top-level fields, node
and edge rules, the `atoms:` cross-reference rule, the `views:` coverage rule,
and the versioning policy.

## Scope

- **In-Scope**: schema shape, kind vocabulary, referential integrity, atom
  cross-refs, spec↔vista symmetry, versioning.
- **Out-of-Scope**: runtime implementation claims; node-level diagram coverage
  checks; replacing atom prose.

## Validation

- Does the contract define all required fields and the kind vocabulary?
- Does it make `atoms:` the only sanctioned spec→atom edge?
- Does `scripts/validate_spec_traceability.py` enforce it?

## Closeout attestation

Contract delivered and machine-enforced; spec2viz files normalized to it
(views + atoms fields, version 0.3) with validator green. No implementation
claims.
