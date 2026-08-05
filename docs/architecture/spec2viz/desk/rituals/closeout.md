---
id: ritual-closeout
steps:
- confirm the task `files:` list includes the produced artifact (spec, vista, contract, or tooling change)
- confirm `python3 ../../../scripts/validate_spec_traceability.py` passes with zero errors
- confirm the vistas HTML was regenerated in the same change if `../vistas/` or any spec changed
- confirm new coverage warnings are either intentional backlog (drawer task exists) or resolved
- confirm task status, summary, and board notes match the delivered change
- close only when the change is commit-ready
tags:
- workspace:desk
---

# Closeout ritual

Close a spec2viz task only after validation passes, the board is updated, and the final change is ready to commit.
