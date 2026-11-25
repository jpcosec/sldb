Task: task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato
Title: El tercer valor del lenguaje de predicados (incomplete) se demuestra alcanzable con un test sobre datos reales o se retira
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
  at: '2026-11-21T08:29:39Z'
  authority: generated
  via: save_document_payload
id: task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-dd3a304c7b74 FALLA. La roja de ''identidad''
  por workbench_demo es la excepción autorizada (f055723d), pero hay dos defectos
  reales. (a) Doc incompleta: docs/architecture/graph-backend.md:44 y 51-52 siguen
  describiendo ''incomplete'' como vigente, y knowledge/commands/cmd-sldb-rules-explain.md:10,20
  y knowledge/symbols/python-sldb-sldb-api-rules-rules_explain-explain_exit.md siguen
  diciendo ''2 incomplete''. sldb selfdoc check da selfdoc/changed en cmd-sldb-rules-explain.md.
  (b) El commit borró tests/api/test_rules.py::test_save_document_payload_returns_the_on_write_alerts_without_a_listener,
  ajeno al retiro (el tester lo reconstruyó y pasa contra el commit). Intento 2: corregir
  graph-backend.md; regenerar los knowledge con ''sldb selfdoc sync'' (no a mano)
  hasta que ''sldb selfdoc check'' quede sin alertas sobre esos archivos; restaurar
  ese test desde el padre (git show HEAD~1:tests/api/test_rules.py) sin tocar el resto;
  correr tests/api/test_rules.py, tests/api/test_rules_evaluation.py y tests/test_rules_language_spec.py.
  Commit desde tu worktree con ''git commit -- <rutas>'' y trailer Task-Id.'
- task_activates
references:
- docs/architecture/rules-language.md
depends_on: []
pills: []
files:
- src/sldb/api/where.py
- docs/architecture/rules-language.md
- tests/test_predicates_cli.py
- CHANGELOG.md
- tests/api/test_rules_evaluation.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El tercer valor del lenguaje de predicados (incomplete) se demuestra alcanzable con un test sobre datos reales o se retira

## Rationale

_Explain why this task exists or the business driver behind it._

El lenguaje de predicados tiene tres valores (true, false, incomplete), pero incomplete parece inalcanzable con datos reales: ningún camino de evaluación sobre un store real lo produce. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16). Código: src/sldb/api/where.py, src/sldb/store/graph/language/predicate_explain.py, predicate_reach.py y src/sldb/api/rules/.

## Goal

_Describe the concrete result this task must produce._

O hay un test que, con un store real armado en tmp_path, obtiene incomplete de una evaluación pública (where o rules check) y documenta cuándo ocurre; o incomplete se retira del lenguaje, de la API y de la doc sin cambiar los resultados true/false existentes.

## Scope

_State what is in scope and what is out of scope._

Entra: buscar todos los productores y consumidores de incomplete; intentar construir el caso real; decidir con evidencia en result-summary.md; implementar la opción elegida con tests en tests/test_predicates_cli.py o tests/api/test_rules_evaluation.py; actualizar docs/architecture/rules-language.md. CHANGELOG. No entra: otros cambios del lenguaje.

Precisiones (coordinador, bundle-1): dato real = un store armado con la API pública en tmp_path; vale un store enlazado que después se borra o se renombra para que quede no disponible. Primero se intenta demostrar; solo si en result-summary.md queda la evidencia de que ningún camino público lo produce (grep de cada sitio que emite incomplete y por qué no se alcanza), se retira. El retiro abarca GraphBackend.eval, StructuredQuery, el tipo de holds, los tests de especificación que lo nombran y docs/architecture/rules-language.md; si el hash del contrato GO02 de esa doc cambia, se actualiza con el mecanismo que check.sh --fast señala. Línea base: los tests existentes pasan sin cambiar sus valores esperados true/false. tests/api/test_rules_evaluation.py existe y se amplía.

Precisiones (coordinador, bundle-2): si se retira incomplete, toda evaluación que hoy lo devolvería devuelve false, que es lo que ya da hoy cuando compose_edge_index descarta las aristas hacia nodos que no existen (H4). El test de alcance o de retiro va en tests/api/test_rules_evaluation.py, que se agrega a files; tests/test_predicates_cli.py solo se ajusta si nombra incomplete. El índice se compone después de dejar no disponible el store enlazado.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep de incomplete en src/sldb. 2) Intentar el caso real. 3) Decidir y documentar la decisión. 4) Implementar y testear. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_predicates_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; result-summary.md explica la decisión con evidencia; CHANGELOG y commit.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
