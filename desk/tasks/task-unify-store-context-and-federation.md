---
id: task-unify-store-context-and-federation
status: open
tags: [system:sldb, workspace:desk, topic:stores]
references: [docs/documentation-review.md]
pills: [desk/pills/pill-015-self-documentation-boundaries.md]
---

# Unify store context and federation

## Rationale

_Explain why this task exists or the business driver behind it._

Ancestor discovery exists, but FAQ, exploration, aliases, and the global registry do not share a consistent context contract.

## Goal

_Describe the concrete result this task must produce._

Resolve project operations from the nearest enclosing store and make known stores discoverable through a maintained global catalog.

## Scope

_State what is in scope and what is out of scope._

Context/root resolution, FAQ and explore anchoring, ancestor alias lookup, global registration and reconciliation, federation traversal and deduplication. Preserve explicit store overrides. No unbounded filesystem scan on each query.

## Implementation Path

_Outline the expected implementation route or affected surface._

Start from store/resolver.py and cli/store_context.py. Define parent and global catalog behavior before changing lifecycle operations; cover nested stores, aliases, collisions, moved stores, and cycles.

## Validation

_List the checks required before this task can close._

- Run resolver and federation regression tests with isolated stores.
- Verify identical project resolution from root and subdirectory.
- Verify global catalog registration, stale-path reporting, and explicit overrides.

## Done When

_Name the observable condition that makes the task complete._

Nearest non-global ancestor context, ancestor/global aliases, FAQ/explore root anchoring, explicit init registration, cycle-safe transitive federation, and explicit catalog reconciliation are implemented and tested. Keep this task open until the delivery audit is complete.
