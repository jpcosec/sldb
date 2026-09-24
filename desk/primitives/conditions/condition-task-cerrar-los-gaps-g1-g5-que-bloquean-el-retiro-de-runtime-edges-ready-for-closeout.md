---
# condition-xxx
id: condition-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-ready-for-closeout
# active | archived
status: active
# Payload path the condition reads
subject: status
# Predicate applied to the value (e.g., eq, contains)
predicate: equals
# Expected value used by the predicate
expected: ready_for_testing
# e.g., system:deskops
tags:
- primitive:condition
---

# Ready for closeout

## Summary

_Summarize the predicate this condition checks._

Task must be in ready_for_testing before closeout.
