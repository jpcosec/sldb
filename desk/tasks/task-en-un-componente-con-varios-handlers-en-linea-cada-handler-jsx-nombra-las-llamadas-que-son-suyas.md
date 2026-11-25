---
sldb:
  by: agent
  at: '2026-11-25T05:31:33Z'
  authority: generated
  via: create_document
id: task-en-un-componente-con-varios-handlers-en-linea-cada-handler-jsx-nombra-las-llamadas-que-son-suyas
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

# En un componente con varios handlers en linea, cada handler JSX nombra las llamadas que son suyas

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de IR 20261125-022841-suggestion-code-facts-ts-tsx-atributos-estaticos-del-elemento-con-handler-llamadas-por-handler-en-linea-y-metodo-del-segundo-argumento (T4 del plan graph_ui de IR, medido sobre graph_ui 36adfbb): specIR solo lee code_facts y necesita esto para el diccionario de componentes; desbloquea T5/T6 de IR.

## Goal

_Describe the concrete result this task must produce._

Que code_facts diga que llamadas pertenecen a cada handler en linea, no solo la primera.

## Scope

_State what is in scope and what is out of scope._

Solo ts_jsx.py/lang_ts.py y un test. Fuera: atributos y segundo argumento.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/sldb. Los handlers JSX salen de src/sldb/code/ts_jsx.py (jsx_handlers da {element, attribute, handler}) y se arman en facts en src/sldb/code/lang_ts.py; las llamadas en ts_calls.py/ts_callee.py. Agnostico de framework, como el resto de ts_jsx. Campo nuevo aditivo: los consumidores existentes no cambian. Hoy un handler en linea ({() => { a(); b(x); }}) da solo el callee de la primera llamada y specIR no puede atribuir las demas (84 no derivados en graph_ui). Agregar al fact del handler 'calls': lista ordenada de los callee (como ts_callee los nombra) de todas las llamadas dentro del cuerpo de esa funcion en linea; para {identifier} y {call(...)} la lista es [handler]. 'handler' sigue siendo el de hoy. Test nuevo tests/code/test_ts_handler_calls.py: un componente con onClick={() => { a(); b(1); }} y onChange={() => c()} da calls [a, b] y [c] respectivamente; onClick={save} da [save].

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/code/test_ts_handler_calls.py tests/selfdoc/test_treesitter_symbols.py

## Done When

_Name the observable condition that makes the task complete._

Cada handler JSX trae calls con sus propias llamadas y el test nuevo pasa con tests/selfdoc/test_treesitter_symbols.py.
