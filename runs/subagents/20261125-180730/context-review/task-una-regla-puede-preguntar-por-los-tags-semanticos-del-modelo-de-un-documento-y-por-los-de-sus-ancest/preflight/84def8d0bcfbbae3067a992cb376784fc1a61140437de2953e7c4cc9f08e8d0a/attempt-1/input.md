FILE:desk/tasks/task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest.md
---
sldb:
  by: agent
  at: '2026-11-25T17:44:33Z'
  authority: generated
  via: create_document
id: task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest
status: draft
summary: ''
tags: []
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

# una regla puede preguntar por los tags semánticos del modelo de un documento y por los de sus ancestros en el DAG

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de specIR (desk/drawer/plans/pedidos-de-specir-y-graph-ui/). El lenguaje de reglas no puede leer los tags que salen de __semantics__ ni recorrer el DAG semántico, así que una regla se escribe por nombre de modelo. Revisar un estándar pide reglas por concepto, que valgan para todos los modelos que lo implementan.

## Goal

_Describe the concrete result this task must produce._

Un predicado del lenguaje de reglas que sea verdadero cuando el modelo del documento tiene un tag dado o uno que desciende de él en el DAG semántico.

## Scope

_State what is in scope and what is out of scope._

Dentro: el lenguaje de reglas y su evaluador. Fuera: reglas concretas de specIR, cambios al DAG semántico.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer docs/architecture/rules-language.md, rules.md y tags.md, y sldb semantic --help. El predicado usa la relación de padre y equivalencia que el DAG ya resuelve; no se calcula otra.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_rules_semantic_tag_predicate.py
- python -m pytest -q tests -k rules

## Done When

_Name the observable condition that makes the task complete._

Una RuleDoc con el predicado casa un documento cuyo modelo declara el tag, casa otro cuyo modelo declara un tag hijo, y no casa uno sin relación. Un tag que no existe en el DAG se informa al validar la regla. rules-language.md describe el predicado con un ejemplo.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

