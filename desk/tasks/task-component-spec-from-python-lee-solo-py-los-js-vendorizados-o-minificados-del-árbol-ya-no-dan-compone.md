---
sldb:
  by: agent
  at: '2026-11-17T01:33:28Z'
  authority: generated
  via: create_document
id: task-component-spec-from-python-lee-solo-py-los-js-vendorizados-o-minificados-del-árbol-ya-no-dan-compone
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-213452-suggestion-regresi-n-de-b2-600b51a9-component-spec-from-python-recorre-js-vendorizados-minificados-y-da-component-spec-syntax-error-rompe-2-pruebas-de-ir.md
depends_on: []
pills: []
files:
- src/sldb/api/notations/component_spec_python.py
- tests/notations/test_component_spec_python.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# component_spec_from_python lee solo .py: los .js vendorizados o minificados del árbol ya no dan component-spec/syntax-error (regresión de B2)

## Rationale

_Explain why this task exists or the business driver behind it._

Desde 600b51a9 (B2, sldb.code lee TS, TSX, JS y JSX), scan_tree recorre también .ts/.tsx/.js/.jsx, y component_spec_from_python (src/sldb/api/notations/component_spec_python.py) usa scan_tree. En IR, un .js vendorizado y minificado (bpmn-js production.min.js) produce un hallazgo component-spec/syntax-error y fallan, de forma determinista, dos pruebas de paridad de IR que exigen findings == []. Origen: desk/inbox/20261116-213452-suggestion-regresi-n-de-b2-600b51a9-component-spec-from-python-recorre-js-vendorizados-minificados-y-da-component-spec-syntax-error-rompe-2-pruebas-de-ir.md.

## Goal

_Describe the concrete result this task must produce._

component_spec_from_python construye el spec solo a partir de los archivos .py del árbol, como antes de B2; ningún archivo de otro lenguaje produce hallazgos en ese spec.

## Scope

_State what is in scope and what is out of scope._

Entra: que component_spec_from_python escanee solo .py (filtrar por extensión los archivos que recorre, o pedir a sldb.code un escaneo limitado a Python con la API que ya existe), sin cambiar scan_tree para los demás consumidores (code_facts, anclas). Test en tests/notations/test_component_spec_python.py: un árbol con un paquete Python y un .js minificado ilegible da el mismo spec y cero hallazgos que el árbol sin el .js. CHANGELOG. No entra: excluir vendor/ o *.min.js de scan_tree en general.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer component_spec_python.py y sldb.code.scan (scan_tree, scan_file) y files.py (find_files). 2) Limitar el recorrido a .py en el generador. 3) Test. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_graph.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con el test nuevo; el spec de src/sldb no cambia respecto de HEAD; CHANGELOG y commit; aviso a IR.
