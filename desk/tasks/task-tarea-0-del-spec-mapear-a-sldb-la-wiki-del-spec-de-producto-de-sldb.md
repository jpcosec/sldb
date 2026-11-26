---
sldb:
  by: agent
  at: '2026-11-26T23:54:19Z'
  authority: generated
  via: create_document
id: task-tarea-0-del-spec-mapear-a-sldb-la-wiki-del-spec-de-producto-de-sldb
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
pointers: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Tarea 0 del spec: mapear a SLDB la wiki del spec de producto de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

JP, 2026-11-26: el spec de producto de sldb no es un solo documento sino una wiki; se escribe primero como texto en docs/spec/ y la tarea 0 es mapearla al store. Sin ese mapa no se sabe qué modelos existentes la expresan ni qué falta.

## Goal

_Describe the concrete result this task must produce._

Cada página de la wiki del spec (objeto, operación, mecanismo, plugin, decisión, abierto) tiene dicho con qué modelo, qué aristas y qué procedencia queda como documento del store de sldb, para que la wiki pase a generarse desde el store.

## Scope

_State what is in scope and what is out of scope._

Leer las páginas de docs/spec/. Decir, clase por clase, qué pieza existente la expresa (modelos de dominio de specIR: DomainOperationDoc, ApiOperationDoc, HandlerDoc, CapabilityDoc, DomainEntityDoc, PieceDoc; RuleDoc, anclas y vistas de sldb) y qué falta, con una frase de por qué nada existente lo cubre. Lo genérico que falte va a sldb y el contenido al plugin (regla de JP, 2026-11-26). No crea modelos ni carga documentos: entrega el mapa y las tareas que salen de él.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- La tabla del mapa cubre cada archivo de docs/spec/ (ls docs/spec/**/*.md contra las filas)
- Cada modelo nuevo propuesto lleva la frase de por qué ninguno existente lo cubre

## Done When

_Name the observable condition that makes the task complete._

Existe una tabla página -> modelo -> aristas que cubre todas las páginas de docs/spec/, sin página sin destino, y las tareas siguientes están creadas con deskops add task.
