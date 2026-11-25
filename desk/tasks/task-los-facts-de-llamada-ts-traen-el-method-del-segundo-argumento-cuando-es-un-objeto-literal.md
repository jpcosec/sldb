---
sldb:
  by: agent
  at: '2026-11-25T05:32:46Z'
  authority: generated
  via: create_document
id: task-los-facts-de-llamada-ts-traen-el-method-del-segundo-argumento-cuando-es-un-objeto-literal
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

# Los facts de llamada TS traen el method del segundo argumento cuando es un objeto literal

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de IR 20261125-022841-suggestion-code-facts-ts-tsx-atributos-estaticos-del-elemento-con-handler-llamadas-por-handler-en-linea-y-metodo-del-segundo-argumento (T4 del plan graph_ui de IR, medido sobre graph_ui 36adfbb): specIR solo lee code_facts y necesita esto para el diccionario de componentes; desbloquea T5/T6 de IR.

## Goal

_Describe the concrete result this task must produce._

Que una llamada request(path, {method: 'POST'}) o fetch(path, {method: 'POST'}) exponga method en su fact.

## Scope

_State what is in scope and what is out of scope._

Solo ts_calls.py (o donde se arma el fact de llamada TS) y un test. Fuera: handlers JSX.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/sldb. Los handlers JSX salen de src/sldb/code/ts_jsx.py (jsx_handlers da {element, attribute, handler}) y se arman en facts en src/sldb/code/lang_ts.py; las llamadas en ts_calls.py/ts_callee.py. Agnostico de framework, como el resto de ts_jsx. Campo nuevo aditivo: los consumidores existentes no cambian. Hoy el fact de llamada da solo el primer argumento. Agregar 'options': dict con las claves de string literal del segundo argumento cuando es un object literal (al menos method; tambien headers no, solo valores string literales planos), vacio si no hay o no es literal. Sin semantica de HTTP: no se asume fetch. Test nuevo tests/code/test_ts_call_options.py: fetch('/api/x', {method: 'POST'}) da options {method: POST}; request('/y') da {}; fetch(u, opts) da {}.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/code/test_ts_call_options.py tests/selfdoc/test_treesitter_symbols.py

## Done When

_Name the observable condition that makes the task complete._

Los facts de llamada TS traen options literales del segundo argumento y el test nuevo pasa con tests/selfdoc/test_treesitter_symbols.py.
