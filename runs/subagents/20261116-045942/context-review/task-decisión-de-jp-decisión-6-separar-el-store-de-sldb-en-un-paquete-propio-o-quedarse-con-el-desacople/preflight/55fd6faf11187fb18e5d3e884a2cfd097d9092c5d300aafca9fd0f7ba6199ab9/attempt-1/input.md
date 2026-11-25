FILE:desk/tasks/task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio-o-quedarse-con-el-desacople.md
---
sldb:
  by: agent
  at: '2026-11-16T04:18:00Z'
  authority: generated
  via: create_document
id: task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio-o-quedarse-con-el-desacople
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
files:
- docs/architecture/store-extraction-proposal.md
- desk/STANDARDS.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-separar-el-store-en-un-paquete-propio-espera-la-decisi-n-6.md
---

# Decisión de JP (decisión 6): separar el store de sldb en un paquete propio o quedarse con el desacople interno

## Rationale

_Explain why this task exists or the business driver behind it._

El desacople del store dentro de sldb está hecho (beb8a99c): el store depende del resto de sldb solo por tres costuras (src/sldb/store/exceptions.py, src/sldb/store/runtime_codec.py, src/sldb/store/model_contract.py) y tests/test_store_seams.py lo hace cumplir. Separarlo en un paquete propio solo tiene sentido si el dueño decide que el store sea un motor genérico de documentos tipados para sldb, deskops, knowledge y repopackage. Esa es la decisión 6, pendiente según desk/STANDARDS.md:19. Spec: docs/architecture/store-extraction-proposal.md. Origen: drawer desk/drawer/tasks/task-separar-el-store-en-un-paquete-propio-espera-la-decisi-n-6.md.

## Goal

_Describe the concrete result this task must produce._

JP toma la decisión 6: (a) separar: se crea la tarea de refactor que inyecta las tres costuras y crea el paquete con su pyproject y su suite; o (b) quedarse con el desacople interno. La decisión queda escrita en docs/architecture/store-extraction-proposal.md, sección "Decisión 6", con fecha, y desk/STANDARDS.md:19 deja de decir que está pendiente (vía la CLI que corresponda o en el commit del doc si STANDARDS.md no es un documento modelado).

## Scope

_State what is in scope and what is out of scope._

Entra: presentar la decisión con el estado (costuras listas, test verde) y la recomendación del coordinador: (b) hasta que un segundo consumidor necesite el store sin sldb. Registrar el recibo owner (dispose accepted de JP), escribir la sección y crear la tarea si es (a). No entra: mover código.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer docs/architecture/store-extraction-proposal.md y desk/STANDARDS.md. 2) Pedir la decisión. 3) Escribir la sección y actualizar STANDARDS.md. 4) Crear la tarea de refactor si es (a).

## Validation

_List the checks required before this task can close._

- grep -n 'Decisión 6' docs/architecture/store-extraction-proposal.md
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la decisión y la fecha; STANDARDS.md ya no la da por pendiente; recibo owner aceptado por JP; tarea de refactor creada si es (a); commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio-o-quedarse-con-el-desacople: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

