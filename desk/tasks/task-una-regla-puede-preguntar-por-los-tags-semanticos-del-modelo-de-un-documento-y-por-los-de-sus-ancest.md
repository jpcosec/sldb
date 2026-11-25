---
sldb:
  by: agent
  at: '2026-11-25T23:18:32Z'
  authority: generated
  via: save_document_payload
id: task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
pointers: []
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

Aclaraciones de la revisión: Dirección: el predicado casa un documento cuyo modelo declara el tag Q o un tag que desciende de Q (Q es ancestro); es decir, pedir el tag padre casa modelos con tags hijos, no al revés. Equivalencia = las equivalencias de tags que ya resuelve el DAG (sldb semantic, docs/architecture/tags.md); un tag equivalente a Q cuenta como Q. Un tag que no existe en el DAG es un error al validar la regla, con el nombre del tag. Docs en sldb/docs/architecture/ (rules-language.md, rules.md, tags.md). Nombre y sintaxis del predicado siguiendo los predicados existentes del lenguaje de reglas, documentado en rules-language.md. Alcance: predicado, validación y tests; ninguna RuleDoc real. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_rules_semantic_tag_predicate.py
- python -m pytest -q tests -k rules

## Done When

_Name the observable condition that makes the task complete._

Una RuleDoc con el predicado casa un documento cuyo modelo declara el tag, casa otro cuyo modelo declara un tag hijo, y no casa uno sin relación. Un tag que no existe en el DAG se informa al validar la regla. rules-language.md describe el predicado con un ejemplo.
