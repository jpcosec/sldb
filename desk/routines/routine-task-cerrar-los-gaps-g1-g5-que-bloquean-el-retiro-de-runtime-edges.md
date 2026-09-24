---
# routine-xxx
id: routine-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-execution-ready
- operator-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-activate
- checklist-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-testing-ready
- operator-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-ready-for-testing
- checklist-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-closeout-ready
- operator-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-close
# Edge identifiers composing the graph
edges:
- edge-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-execution-to-activate
- edge-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-activate-to-testing
- edge-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-testing-to-ready
- edge-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-ready-to-closeout
- edge-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-closeout-to-close
- edge-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Cerrar los gaps G1-G5 que bloquean el retiro de runtime/edges

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Cerrar los gaps G1-G5 que bloquean el retiro de runtime/edges.
