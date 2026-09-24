---
# routine-xxx
id: routine-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-execution-ready
- operator-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-activate
- checklist-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-testing-ready
- operator-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-ready-for-testing
- checklist-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-closeout-ready
- operator-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-close
# Edge identifiers composing the graph
edges:
- edge-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-execution-to-activate
- edge-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-activate-to-testing
- edge-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-testing-to-ready
- edge-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-ready-to-closeout
- edge-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-closeout-to-close
- edge-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Borrar la capa runtime/edges y podar el surface publico

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Borrar la capa runtime/edges y podar el surface publico.
