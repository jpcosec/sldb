---
id: task-go01-registrar-la-decision-de-frontera-y-su-atom
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- commit
- document
---

# GO01: registrar la decision de frontera y su atom

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO01 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9, D1 del 2026-11-04): la frontera sldb/deskops reencuadrada queda como atom enlazado desde la pill, el gate G_BOUNDARY cita el commit y deskops recibe la nota.

## Goal

_Describe the concrete result this task must produce._

Atom nuevo en desk/atoms que diga que sldb evalua reglas declaradas sobre documentos, aristas y hashes y que los consumidores las autoran como documentos; la pill pill-keep-sldb-generic-and-move-workflow-behavior-toward-deskops lo enlaza en how; dos commits en main (atom+pill; luego gates.G_BOUNDARY satisfied con el hash del primero); nota a deskops por message send.

## Scope

_State what is in scope and what is out of scope._

Solo desk/atoms/ (atom nuevo), desk/contexts/pill-keep-sldb-generic-and-move-workflow-behavior-toward-deskops.md (campo how), desk/drawer/plans/grafo-operable/dag.yaml (solo gates.G_BOUNDARY) y una nota al inbox de deskops por el canal entre desks. No cambia codigo.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- git log --oneline -3 muestra los dos commits; grep del id del atom en el campo how de la pill; archivo nuevo en ../deskops/desk/inbox con el titulo; gates.G_BOUNDARY state satisfied con hash de 40 caracteres

## Done When

_Name the observable condition that makes the task complete._

G_BOUNDARY satisfied en dag.yaml citando un commit alcanzable desde main que contiene el atom y la pill enlazada, y la nota existe en deskops/desk/inbox.
