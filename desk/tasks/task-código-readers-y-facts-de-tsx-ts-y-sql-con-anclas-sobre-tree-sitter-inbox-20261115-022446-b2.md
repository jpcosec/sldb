---
sldb:
  by: agent
  at: '2026-11-15T15:52:44Z'
  authority: generated
  via: create_document
id: task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2
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

# Código: readers y facts de TSX/TS y SQL con anclas sobre tree-sitter (inbox 20261115-022446, B2)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR ancla cada nodo extraído a su fuente con las anclas de código de sldb y debe leer Django (Python, cubierto), SQL y React TSX/TS. Decisión de JP 2026-11-15: lo genérico va a sldb y specIR solo mapea al dominio (IR08 e IR09 quedan como mapeo sobre estos extractores).

## Goal

_Describe the concrete result this task must produce._

El paquete sldb.code lee TS/TSX y SQL, publica sus hechos de fuente y soporta anclas, con gramáticas tree-sitter como extras opcionales.

## Scope

_State what is in scope and what is out of scope._

Amplía el pedido parcial del inbox sldb 20261115-022446, que solo pedía anclas: aquí entran readers y facts, no solo anclas. Hoy el escáner recorre solo .py con tree-sitter-python (extra code); sldb.code tiene readers, facts, fingerprints, ids, imports y scan. Alcance: TS/TSX (componentes, funciones, hooks, tipos, imports) y SQL (tablas, columnas, vistas, DDL y migraciones); hechos en la misma forma que los de Python (ver el atom del inventario de código como hechos de fuente); record_anchor y check_anchors con la misma referencia code:<ruta>::<qualified_name>, fingerprints por nodo, estados y reconexión; gramáticas como extras opcionales. Reutilizar la maquinaria existente de Python, no duplicarla. Fuera de alcance: mapear a conceptos de dominio (eso es specIR).

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

Fixtures reales de TSX y de SQL producen hechos y anclas con estados intact/changed/lost verificados por test; sldb sin los extras sigue funcionando; suite de a un archivo, tools/check.sh y stores build --check.
