FILE:desk/tasks/task-emparejamiento-de-átomos-con-elementos-de-diagrama-explícito-y-difuso-en-sldb-api-matching-d4.md
---
sldb:
  by: agent
  at: '2026-11-15T15:53:16Z'
  authority: generated
  via: create_document
id: task-emparejamiento-de-átomos-con-elementos-de-diagrama-explícito-y-difuso-en-sldb-api-matching-d4
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
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Emparejamiento de átomos con elementos de diagrama (explícito y difuso) en sldb.api.matching (D4)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: el emparejamiento de átomos con elementos de un spec es genérico y debe usar sldb.api.matching, no un matcher propio de cada consumidor.

## Goal

_Describe the concrete result this task must produce._

sldb.api.matching empareja átomos con elementos de diagrama por vínculo explícito (atoms: en el elemento) y por similitud difusa.

## Scope

_State what is in scope and what is out of scope._

SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE. Origen: el módulo deskops de spec2viz (SldbAtomResolver, parse_atoms, build_atoms_by_view, collect_explicit_atoms, build_explicit_atoms, UnknownAtomError, collect_explicit_refs, build_explicit_refs, attach_atom_edges, build_coverage_by_view, label_key) y los tests test_atoms_matching, test_explicit_atoms de spec2viz. Primero comparar con sldb.api.matching (matcher difflib, índice de documentos, protocolo de embedder): si ya cubre el emparejamiento difuso se reutiliza; migrar lo que falte (resolución explícita por id, alias por título y etiquetas, cobertura, avisos). Solo la lógica de emparejamiento y cobertura; la inyección de átomos en el HTML del catálogo se queda en la capa visual. Anotaciones del catálogo con autoguardado: servirlas con sldb serve si alcanza; si no, registrar el pedido como nota al desk de sldb. spec2viz no se retira (gate IR13).

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

Emparejamiento explícito y difuso en sldb.api.matching con los tests portados verdes y sin matcher duplicado; decisión sobre sldb serve registrada; suite de a un archivo, tools/check.sh y stores build --check.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-emparejamiento-de-átomos-con-elementos-de-diagrama-explícito-y-difuso-en-sldb-api-matching-d4: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

