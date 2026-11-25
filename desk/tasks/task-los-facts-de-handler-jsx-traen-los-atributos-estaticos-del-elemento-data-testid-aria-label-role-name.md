---
sldb:
  by: agent
  at: '2026-11-25T05:30:44Z'
  authority: generated
  via: create_document
id: task-los-facts-de-handler-jsx-traen-los-atributos-estaticos-del-elemento-data-testid-aria-label-role-name
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

# Los facts de handler JSX traen los atributos estaticos del elemento: data-testid, aria-label, role, name y type

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de IR 20261125-022841-suggestion-code-facts-ts-tsx-atributos-estaticos-del-elemento-con-handler-llamadas-por-handler-en-linea-y-metodo-del-segundo-argumento (T4 del plan graph_ui de IR, medido sobre graph_ui 36adfbb): specIR solo lee code_facts y necesita esto para el diccionario de componentes; desbloquea T5/T6 de IR.

## Goal

_Describe the concrete result this task must produce._

Que cada handler JSX de code_facts lleve los atributos literales de su elemento, para derivar un localizador.

## Scope

_State what is in scope and what is out of scope._

Solo ts_jsx.py/lang_ts.py y un test. Fuera: llamadas por handler y segundo argumento (tareas hermanas).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/sldb. Los handlers JSX salen de src/sldb/code/ts_jsx.py (jsx_handlers da {element, attribute, handler}) y se arman en facts en src/sldb/code/lang_ts.py; las llamadas en ts_calls.py/ts_callee.py. Agnostico de framework, como el resto de ts_jsx. Campo nuevo aditivo: los consumidores existentes no cambian. En jsx_handlers, agregar 'attributes': dict con los atributos del mismo elemento (jsx_opening_element o self_closing) cuyo nombre sea data-testid, aria-label, role, name, type, id o title y cuyo valor sea un string literal ("x" o {'x'}); los no literales se omiten. Propagar al fact del handler. Test nuevo tests/code/test_ts_handler_attributes.py (o junto a los tests TS existentes si hay carpeta) sobre un TSX en tmp_path: <button data-testid="save" aria-label="Guardar" onClick={save}/> da attributes {data-testid: save, aria-label: Guardar}; un aria-label={label} no literal no aparece; un elemento sin esos atributos da {}.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/code/test_ts_handler_attributes.py tests/selfdoc/test_treesitter_symbols.py

## Done When

_Name the observable condition that makes the task complete._

code_facts de un .tsx da attributes literales por handler y el test nuevo pasa con tests/selfdoc/test_treesitter_symbols.py.
