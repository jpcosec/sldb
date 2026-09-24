---
# routine-xxx
id: routine-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-execution-ready
- operator-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-activate
- checklist-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-testing-ready
- operator-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-ready-for-testing
- checklist-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-closeout-ready
- operator-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-close
# Edge identifiers composing the graph
edges:
- edge-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-execution-to-activate
- edge-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-activate-to-testing
- edge-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-testing-to-ready
- edge-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-ready-to-closeout
- edge-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-closeout-to-close
- edge-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Comando de porte sldb stores migrate-legacy-edges y error de migracion

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Comando de porte sldb stores migrate-legacy-edges y error de migracion.
