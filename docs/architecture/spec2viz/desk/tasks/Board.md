---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-specify-sldb-target-documents-spec.md
- desk/tasks/task-specify-sldb-target-crates-spec.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
- desk/contexts/pill-traceability-workflow.md
# List of ritual-xxx paths
rituals:
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb, workspace:desk
tags:
- workspace:desk
---

# spec2viz Board

## Purpose

Route active spec2viz work: specs, vistas, generators, and validators of the traceability layer.



## Notes

- Desk propio creado con `deskops init` (2026-08-04): spec2viz se gobierna como subproyecto documental dentro del repo sldb.
- Backlog = coverage warnings del validador: d05/d06 (documents spec), d03 (crates spec).
- Gate transversal: `scripts/validate_spec_traceability.py` con 0 errores antes de cualquier closeout; vistas HTML siempre regeneradas, nunca editadas a mano.
- Los atoms de esta capa viven en `desk/atoms/` local; los `atoms:` de los specs referencian atoms del repo padre.
- Specify sldb.target.documents spec [draft] - Create target-documents.yml covering StructuredNLDoc models, importers, emitters, renderers and families so vistas d05/d06 gain a governing spec.

## Task Details

_Generated from the task references above._

- Specify sldb.target.documents spec [draft] - Create target-documents.yml covering StructuredNLDoc models, importers, emitters, renderers and families so vistas d05/d06 gain a governing spec.
- Specify sldb.target.crates spec [draft] - Create target-crates.yml describing the crate partition and compile dependencies so vista d03 gains a governing spec.
