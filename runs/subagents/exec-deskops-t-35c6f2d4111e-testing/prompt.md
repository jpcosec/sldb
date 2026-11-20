Task: task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo
Title: Reglas de código limpio de 0f91540d: cinco archivos pasan los límites (rule_graph, rules_on_write, component_spec_graph, store_check, diagnostics)
Status: active
Current node: ritual-testing
Task type: task.refactor
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-20T13:46:29Z'
  authority: generated
  via: save_document_payload
id: task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Reglas de código limpio de 0f91540d: cinco archivos pasan los límites (rule_graph, rules_on_write, component_spec_graph, store_check, diagnostics)

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-20: integrate de la tarea on_write (código en 0f91540d, compartido con raw_atoms_by_view, notations from-graph y stores check sin build porque cuatro ejecutores commitearon en el mismo checkout) falló en tests/test_clean_code_rules.py: rule_graph.py tiene 97 líneas efectivas (máx. 80); component_spec_graph.py, 90 (máx. 80); store_check.py, 86 (máx. 80); check_on_write en rules_on_write.py, 12 líneas de lógica (máx. 10); _diagnose_model en store/diagnostics.py, 11 (máx. 10). La suite tiene 3172 tests en verde aparte de esos 5.

## Goal

_Describe the concrete result this task must produce._

tests/test_clean_code_rules.py pasa entero sin subir límites, partiendo funciones y moviendo código a módulos nuevos donde haga falta, con el mismo comportamiento: los tests de las cuatro tareas (tests/api/test_on_write_entering.py, tests/api/test_rules.py, tests/matching/test_matching_refs.py, tests/notations/test_notations_from_graph_cli.py, tests/store/test_diagnostics.py) siguen en verde sin cambiar sus asserts. Un módulo nuevo fuera de una carpeta con eje se declara en contracts/layers.toml.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/rules/rule_graph.py, src/sldb/api/rules/rules_on_write.py, src/sldb/api/notations/component_spec_graph.py, src/sldb/api/stores/store_check.py, src/sldb/store/diagnostics.py, los módulos nuevos que salgan de partirlos y contracts/layers.toml si hace falta. Fuera: cambiar comportamiento o límites.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: correr tests/test_clean_code_rules.py y ver los 5. p2: partir cada uno (funciones auxiliares, módulo hermano). p3: correr test_clean_code_rules entero y los cinco archivos de tests de arriba, de a uno. p4: bash tools/check.sh --fast: todas las puertas en verde salvo 'identidad' por workbench_demo (excepción autorizada; decisión aparte). p5: commit SOLO de tus archivos con 'git commit -- <rutas>' (puede haber otros agentes en el repo), con el trailer Task-Id, y deskops advance. Sin commit es FALLA.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py

## Done When

_Name the observable condition that makes the task complete._

test_clean_code_rules y los cinco archivos de tests pasan; la suite completa la corre integrate.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
