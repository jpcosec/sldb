Task: task-arreglo-de-3f547569-cache-vieja-de-reviewdoc-layout-py-pasa-el-limite-de-80-lineas-y-el-test-de-rees
Title: Arreglo de 3f547569 (caché vieja de ReviewDoc): layout.py pasa el límite de 80 líneas y el test de reescritura en el mismo tick falla en una copia limpia
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-20T03:26:54Z'
  authority: generated
  via: save_document_payload
id: task-arreglo-de-3f547569-cache-vieja-de-reviewdoc-layout-py-pasa-el-limite-de-80-lineas-y-el-test-de-rees
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
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Arreglo de 3f547569 (caché vieja de ReviewDoc): layout.py pasa el límite de 80 líneas y el test de reescritura en el mismo tick falla en una copia limpia

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-20: integrate de la tarea de la caché vieja de ReviewDoc (código 3f547569, cerrada en 04b9d13a) falló en la suite completa de sldb en la copia limpia (log runs/queue/logs/integrate-task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen.log). Falla 1: tests/test_clean_code_rules.py[sldb/store/layout.py]: 'File layout.py has 86 effective lines (max 80)'; drop_disk_caches agregó líneas a src/sldb/store/layout.py. Falla 2: tests/api/test_select_documents_disk.py::test_a_rewrite_in_place_inside_one_clock_tick_is_seen_by_the_next_process (línea 119): assert [] == ['TaskDoc:b']. El test pasó en el contenedor del tester y falla en la copia limpia de integrate (pytest -n 4), así que el arreglo o el test dependen del reloj o del orden. La tarea ya está cerrada; esto es su arreglo.

## Goal

_Describe the concrete result this task must produce._

La suite completa de sldb pasa en una copia limpia con pytest -n 4: layout.py queda en 80 líneas efectivas o menos, sin subir el límite (drop_disk_caches pasa a un módulo propio o junto a las cachés que borra), y la caché ve de verdad una reescritura in place dentro del mismo tick de reloj, en cualquier proceso y orden. Si el test asumía algo falso, se corrige el arreglo, no se debilita el test.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/store/layout.py, el módulo nuevo de drop_disk_caches si hace falta, src/sldb/store/edge_index/cache_keys.py, composed_disk.py, store/query_engine/document_rows_disk.py, tests/api/test_select_documents_disk.py y CHANGELOG. Fuera: subir límites de código limpio.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: reproducir las dos fallas: 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py -k layout' y el test de reescritura varias veces y con '-n 4' junto al resto de tests/api, para ver si es de reloj, de orden o de proceso. p2: mover drop_disk_caches fuera de layout.py. p3: arreglar la clave de la caché que falla (la caché de filas de documentos document_rows_disk.py, si es la que lee el test, también tiene que ver el roster como la compuesta). p4: el test pasa 20 veces seguidas y con -n 4. p5: quick_gates (bash tools/check.sh --fast) en 0 y commit con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py tests/test_clean_code_rules.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_clean_code_rules.py y tests/api/test_select_documents_disk.py pasan, también 20 veces seguidas y con -n 4; la suite completa la corre integrate.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-arreglo-de-3f547569-cache-vieja-de-reviewdoc-layout-py-pasa-el-limite-de-80-lineas-y-el-test-de-rees"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
