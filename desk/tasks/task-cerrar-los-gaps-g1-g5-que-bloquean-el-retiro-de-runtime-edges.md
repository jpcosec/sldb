---
id: task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges
current_node: checklist-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-execution-ready
history: []
references: []
depends_on:
- task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges
pills: []
files: []
checklists:
- checklist-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-execution-ready
- checklist-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-testing-ready
- checklist-task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Cerrar los gaps G1-G5 que bloquean el retiro de runtime/edges

## Rationale

_Explain why this task exists or the business driver behind it._

docs/architecture/edges-retirement-plan.md identifica 6 gaps sin equivalente en la capa nueva. G1: nodos sldb://field/ + edges has_field y extends, sin productor en la ruta semantic-export -> snapshot. G2: contribution tipada (nodos relation_type/anchor, edges relation_doc/applies_to_*). G3: reglas cross-document de resolve.py (condition/axis heredados, reverse de undirected, dangling authored). G4: validacion contra relation types, que deja sin equivalente a 'sldb edges check' y a /lint (cli/serve/lint_routes.py:62). G5: federacion de lectura (include_linked, ids calificados store:Model:name). Un gap no declarado es peor que el retiro entero.

## Goal

_Describe the concrete result this task must produce._

Que cada capacidad de runtime/edges tenga equivalente demostrado sobre el snapshot networkx/KGDB.

## Scope

_State what is in scope and what is out of scope._

IN: G1 a G5, cada uno con su test de paridad. G6 (exclude_tags en index_from_snapshot) es mecanico y va incluido. OUT: no borrar la capa vieja todavia.

## Implementation Path

_Outline the expected implementation route or affected surface._

Un gap por commit, cada uno con test que demuestre paridad contra el comportamiento actual de la capa edges ANTES de que se retire. Mientras la capa vieja siga viva, es la referencia contra la que comparar.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

Los 6 gaps cerrados con test de paridad cada uno; 'sldb edges check' y /lint tienen equivalente funcionando; pytest verde.
