---
id: task-separar-el-store-en-un-paquete-propio-espera-la-decisi-n-6
status: deferred
summary: Mover sldb.store a un paquete propio si el dueño lo decide (decisión 6);
  el desacople interno ya está hecho.
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references:
- docs/architecture/store-extraction-proposal.md
- beb8a99c04
- tests/test_store_seams.py
depends_on: []
pills: []
files: []
task_type: design
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Separar el store en un paquete propio (espera la decisión 6)

## Rationale

_Explain why this task exists or the business driver behind it._

Es la mitad pendiente de la entrada del drawer task-extract-store-into-generic-typed-document-engine-document-codec-plugins: la otra mitad, desacoplar el store dentro de sldb, está hecha (beb8a99c04). Separarlo en un paquete solo tiene sentido si el dueño decide que el store sea un motor genérico de documentos tipados que consumen sldb, deskops, knowledge y repopackage (decisión 6).

## Goal

_Describe the concrete result this task must produce._

Si la decisión 6 es separar: sldb.store vive en un paquete propio, con su pyproject y su suite, y sldb lo consume solo por su API. Si es quedarse con el desacople interno: esta entrada se retira con esa decisión como motivo.

## Scope

_State what is in scope and what is out of scope._

Dentro: reemplazar las tres costuras por las que el store depende hoy del resto de sldb (store/exceptions.py, store/runtime_codec.py, store/model_contract.py): excepciones propias del store, un codec y un contrato de modelo inyectados en vez de importados. Fuera: cambiar el formato del store o su API pública. Spec: docs/architecture/store-extraction-proposal.md.

## Implementation Path

_Outline the expected implementation route or affected surface._

Se define cuando el dueño tome la decisión 6; el punto de partida es docs/architecture/store-extraction-proposal.md y tests/test_store_seams.py.

## Validation

_List the checks required before this task can close._

- La suite del paquete separado pasa sola
- La suite de sldb pasa importando el store solo por su API
- tests/test_store_seams.py sigue verde

## Done When

_Name the observable condition that makes the task complete._

El store se instala como paquete propio y sldb lo usa por su API, o el dueño decide no separarlo y la entrada se retira.
