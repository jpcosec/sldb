---
# routine-xxx
id: routine-task-retirar-modulos-sueltos-sin-importadores
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-retirar-modulos-sueltos-sin-importadores-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-retirar-modulos-sueltos-sin-importadores-execution-ready
- operator-task-retirar-modulos-sueltos-sin-importadores-activate
- checklist-task-retirar-modulos-sueltos-sin-importadores-testing-ready
- operator-task-retirar-modulos-sueltos-sin-importadores-ready-for-testing
- checklist-task-retirar-modulos-sueltos-sin-importadores-closeout-ready
- operator-task-retirar-modulos-sueltos-sin-importadores-close
# Edge identifiers composing the graph
edges:
- edge-task-retirar-modulos-sueltos-sin-importadores-execution-to-activate
- edge-task-retirar-modulos-sueltos-sin-importadores-activate-to-testing
- edge-task-retirar-modulos-sueltos-sin-importadores-testing-to-ready
- edge-task-retirar-modulos-sueltos-sin-importadores-ready-to-closeout
- edge-task-retirar-modulos-sueltos-sin-importadores-closeout-to-close
- edge-task-retirar-modulos-sueltos-sin-importadores-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Retirar modulos sueltos sin importadores

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Retirar modulos sueltos sin importadores.
