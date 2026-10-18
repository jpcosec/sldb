# Migrate SLDB desk context to deskops

ID: issue-migrate-sldb-desk-context-to-deskops
Status: closed

## What

SLDB has repo-local `desk/` context and Python model files that duplicate or overlap with the deskops workflow surface.

## Why

`desk/` should be document data, while workflow implementation and reusable operational context should live in `deskops`. Keeping SLDB-specific desk context here creates drift and repeats the boundary problem fixed in deskops.

## Scope

- Review the remaining local desk context surfaces and `tools/sldb/desk/pills/`.
- Distill durable knowledge into deskops atoms or docs where it belongs.
- Remove or migrate SLDB `desk/` Python code such as `desk/models.py` if it is still active.
- Leave SLDB with only project docs that are truly owned by SLDB.

## Validation

- SLDB tests still pass.
- No required SLDB workflow context is lost.
- `deskops` remains the owner of workflow operations and desk document models.

## Tags

- system:sldb
- system:deskops
- topic:boundary

## Resolution

Closed: 2026-10-18
Reason: Resuelto: el desk de sldb lo opera deskops desde su migración de ciclo de vida (6fbb47b6); los modelos de deskops se heredan del store de deskops en vez de copiarse; desk/models.py queda solo con los dos modelos propios del desk de sldb (DeskSpecDoc, DeskStandardsDoc) y el InboxNoteDoc local pasó a ser un fixture de tests. Las pills de desk/pills son conocimiento propio de sldb y se quedan.
Refs: 6fbb47b6, b83ba53076, docs/architecture/model-federation-on-the-graph.md
