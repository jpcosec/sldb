---
sldb:
  by: agent
  at: '2026-11-25T19:29:07Z'
  authority: generated
  via: create_document
id: task-los-hechos-de-llamada-de-python-traen-los-argumentos-literales-y-de-inner-add-parser-nodes-help-sale
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

# los hechos de llamada de Python traen los argumentos literales, y de inner.add_parser("nodes", help="...") sale el nombre del comando y su ayuda

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de specIR (desk/drawer/plans/pedidos-de-specir-y-graph-ui/). specIR va a describir librerías de Python con CLI leyendo los hechos de sldb. sldb ya lee Python con tree-sitter, pero una llamada sale solo con su destino: en src/sldb/cli/parsers/graph_project.py, la línea inner.add_parser("nodes", help="Every document and file node...") queda como la relación {type: calls, target: inner.add_parser}. Sin el argumento no se sabe qué comando declara. Es lo mismo que ya se pidió para las llamadas de TypeScript (el method del segundo argumento).

## Goal

_Describe the concrete result this task must produce._

Que una llamada de Python lleve sus argumentos cuando son literales: los posicionales en orden y los nombrados por su nombre.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/code/ (py_calls y lo que arma la relación calls) y la documentación de los hechos. Fuera: evaluar expresiones, reconocer argparse o click como tales (eso es de specIR), cambiar los hechos de otros lenguajes.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer docs/architecture/code-anchoring.md y cómo quedó resuelto el pedido equivalente de TypeScript, para usar la misma forma. Un argumento que no es literal se informa como no literal, no se omite.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_python_call_literal_arguments.py
- python -m pytest -q tests -k "code_facts or anchor"

## Done When

_Name the observable condition that makes the task complete._

Sobre src/sldb/cli/parsers/graph_project.py, la llamada a add_parser trae "nodes" como primer argumento posicional y el texto de help como argumento nombrado. Una llamada con una variable como argumento la marca como no literal. Los hechos que no son llamadas no cambian, y las huellas de las anclas existentes siguen intactas.
