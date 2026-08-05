---
id: ritual-closeout
steps:
- confirm the task `files:` list includes the produced contract artifact
- confirm the task `pills:` list includes the planning-contract guardrail
- confirm task status, summary, and board notes match the delivered artifact
- confirm downstream tasks can consume the closed contract without reopening scope
- if the task touches `docs/architecture/spec2viz/`, `docs/architecture/vistas/`, or `docs/architecture/core-diagrams/`: confirm `scripts/validate_spec_traceability.py` passes and the vistas HTML was regenerated in the same change
- close only when the change is commit-ready
tags:
- workspace:desk
---

# Closeout ritual

Close a planning task only after its contract artifact, task metadata, and board state all agree.
