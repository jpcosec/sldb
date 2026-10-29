---
id: task-congelar-journal-autoridad-arbol
status: active
summary: Congelar el journal; el arbol es la autoridad y el journal una vista derivada
  sobre el.
tags:
- workspace:desk
- artifact:task
- system:sldb
- topic:governance
current_node: ''
history: []
references:
- docs/architecture/journal-authority.md
- desk/inbox/20261019-011009-unclear-decisi-n-del-due-o-qu-mecanismo-guarda-el-pasado-del-rbol-del-store-journal.md
- docs/versionado-y-colaboracion.md
depends_on: []
pills: []
files:
- src/sldb/store/journal/
- src/sldb/store/hashing.py
task_type: design
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Congelar el journal y rediseñar la autoridad: el árbol guarda, el journal es una vista

## Rationale

_Explain why this task exists or the business driver behind it._

El journal hoy es un log de escrituras paralelo al árbol Merkle: guarda `previous_value`/`new_value` (los valores) Y los mismos `hash_c/hash_d/hash_a` que el árbol ya computa. Es una segunda fuente de verdad que duplica la primera, y su dueño no la conoce a fondo. Decisión tomada: **congelarlo** y rediseñar la relación.

## Goal

_Describe the concrete result this task must produce._

Dejar por escrito la dirección de diseño para cuando se retome: el **árbol es la autoridad**; el **journal es una interfaz de lectura** sobre él (como `git log`/`git diff` sobre el object database), no un segundo almacén.

## Scope

_State what is in scope and what is out of scope._

**En scope:**

- registrar el estado actual del journal (qué es, qué tiene, quién lo escribe)
- fijar la dirección: árbol = autoridad, journal = vista fina de punteros
- la consecuencia estructural: para que el journal sea una vista, el árbol tiene que guardar el pasado

**Fuera de scope (por ahora):**

- implementar nada
- mover código del journal
- decidir el formato del snapshot contenido-direccionado

## Implementation Path

_Outline the expected implementation route or affected surface._

Decisión del dueño (2026-10-29): el pasado del árbol del store se pregunta a git (historia de los shards de .sldb/core), no a snapshots propios ni al journal. El árbol versionado es la autoridad; el journal pasa a ser vista derivada y se congela. Partir de 'sldb docs history' que ya lee git.

## Validation

_List the checks required before this task can close._

- Bloqueada por decisión del dueño (nota del inbox 20261019-011009): qué mecanismo guarda el pasado del árbol del store, (a) snapshots propios, (b) historia de git de los shards o (c) descartar el journal. La propuesta está en docs/architecture/journal-authority.md y no se implementa hasta esa decisión.

## Done When

_Name the observable condition that makes the task complete._

Se retoma la task, se decide el mecanismo de snapshot del árbol, y el journal se reduce a una vista derivada (o se archiva la decisión y se descarta el journal).
