---
# routine-xxx
id: routine-task-specify-sldb-target-documents-spec
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-specify-sldb-target-documents-spec-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-specify-sldb-target-documents-spec-execution-ready
- operator-task-specify-sldb-target-documents-spec-activate
- checklist-task-specify-sldb-target-documents-spec-testing-ready
- operator-task-specify-sldb-target-documents-spec-ready-for-testing
- checklist-task-specify-sldb-target-documents-spec-closeout-ready
- operator-task-specify-sldb-target-documents-spec-close
# Edge identifiers composing the graph
edges:
- edge-task-specify-sldb-target-documents-spec-execution-to-activate
- edge-task-specify-sldb-target-documents-spec-activate-to-testing
- edge-task-specify-sldb-target-documents-spec-testing-to-ready
- edge-task-specify-sldb-target-documents-spec-ready-to-closeout
- edge-task-specify-sldb-target-documents-spec-closeout-to-close
- edge-task-specify-sldb-target-documents-spec-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Specify sldb.target.documents spec

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Specify sldb.target.documents spec.
