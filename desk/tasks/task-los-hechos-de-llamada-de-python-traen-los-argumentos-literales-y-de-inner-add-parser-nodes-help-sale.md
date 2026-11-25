---
sldb:
  by: agent
  at: '2026-11-25T22:42:16Z'
  authority: generated
  via: save_document_payload
id: task-los-hechos-de-llamada-de-python-traen-los-argumentos-literales-y-de-inner-add-parser-nodes-help-sale
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references:
- docs/architecture/code-anchoring.md
- src/sldb/code/py_calls.py
- tests/code/test_py_call_args.py
- tests/selfdoc/test_treesitter_symbols.py
- c2ee73402e7b7a775b11036058ce2669fb304a28
depends_on: []
pills: []
files:
- docs/architecture/code-anchoring.md
- src/sldb/code/py_calls.py
- tests/code/test_py_call_args.py
- tests/selfdoc/test_treesitter_symbols.py
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-layout-de-una-notationdoc-acepta-partition-lanes-con-by
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

Leer docs/architecture/code-anchoring.md. Hoy src/sldb/code/py_calls.py call_parts ya da {func, args, kwargs} con los argumentos como texto normalizado (py_norm); la relación calls del cuerpo de una función lleva solo el texto de la llamada. Forma nueva, la misma para args y kwargs: cada argumento es {"text": <texto py_norm>, "value": <valor de ast.literal_eval>} si es literal (str, número, bool, None, y tuplas, listas o dicts de literales), o {"text": <texto>, "literal": false} si no lo es (variable, llamada, *x, **x, f-string). args es la lista de posicionales en orden; kwargs, un dict nombre -> objeto. 1) Cambiar call_parts a esa forma y ajustar los que la usan (decorators y _decorator), para que todas las llamadas usen la misma. 2) Que cada entrada de la relación calls de una función lleve además args y kwargs con esa forma, sin cambiar la clave por la que se identifica la llamada. 3) No tocar src/sldb/code/fingerprints.py: las huellas no dependen de estos campos. 4) Documentar la forma en docs/architecture/code-anchoring.md, en la sección de hechos de código de Python. 5) Tests en tests/code/test_py_call_args.py (archivo nuevo; si tests/code no existe, crearlo con lo mínimo): add_parser de src/sldb/cli/parsers/graph_project.py trae args[0] == {text: '"nodes"', value: 'nodes'} y kwargs['help'] con value el texto de ayuda; f(x) da {text: 'x', literal: false}; un decorador con argumentos usa la misma forma. 6) Commit con prefijo feat:, sin trailer Task-Id. Correr el test nuevo, tests/selfdoc/test_fingerprints.py y los tests existentes que importen py_calls (grep -rl py_calls tests); la suite completa la corre el host.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/code/test_py_call_args.py tests/selfdoc/test_fingerprints.py

## Done When

_Name the observable condition that makes the task complete._

Sobre src/sldb/cli/parsers/graph_project.py, la llamada a add_parser trae "nodes" como primer argumento posicional y el texto de help como argumento nombrado. Una llamada con una variable como argumento la marca como no literal. Los hechos que no son llamadas no cambian, y las huellas de las anclas existentes siguen intactas.
