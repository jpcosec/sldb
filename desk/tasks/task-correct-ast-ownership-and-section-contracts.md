---
id: task-correct-ast-ownership-and-section-contracts
status: open
tags: [system:sldb, workspace:desk, topic:ast]
references: [docs/documentation-review.md, docs/ast_query_primitives.md, desk/tasks/task-design-sldb-ast-query-primitives.md]
pills: [desk/pills/pill-015-self-documentation-boundaries.md]
---

# Correct AST ownership and section contracts

## Rationale

_Explain why this task exists or the business driver behind it._

SLDBGuide demonstrates incorrect field ownership when rendered lines differ from template lines. Section spans currently identify headings, and persisted and fallback outputs differ.

## Goal

_Describe the concrete result this task must produce._

Make field ownership and section boundaries reliable enough for structural queries and documentation provenance.

## Scope

_State what is in scope and what is out of scope._

Field-to-heading identity mapping, nested field ownership, heading versus body spans, persisted/fallback schema parity, and regression examples. This follows up the historical AST design task; it does not introduce the old hardcoded get_block/get_section API.

## Implementation Path

_Outline the expected implementation route or affected surface._

Inspect cli/graph_ops/map_fields.py, extract.py, build_ir.py, and section persistence. Map structural identities rather than comparing line offsets in different texts.

## Validation

_List the checks required before this task can close._

- Reproduce and fix SLDBGuide ownership with frontmatter and expanded lists.
- Verify full section boundaries, nested headings, and repeated titles.
- Assert the same section schema before and after index rebuild.

## Done When

_Name the observable condition that makes the task complete._

Ownership now follows template heading order rather than rendered line offsets, and section spans cover the complete body. Regression coverage covers expanded lists and nested boundaries. Stable addressing for repeated sibling headings remains a design gap; keep this task open until it is decided and the delivery audit is complete.
