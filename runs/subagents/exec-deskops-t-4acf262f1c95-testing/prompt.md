Task: task-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta-no-co
Title: stores check sobre un clon sin build reporta los documentos generados ausentes como una alerta, no como miles de errores
Status: active
Current node: ritual-testing
Task type: task.code
From drawer: drawer task-stores-check-sobre-un-clon-sin-build-da-rc-1-con-2453-errores-missing-de-pythonsymboldoc-generados-y-tapa-los-errores-reales (retirado en el triaje 2026-11-16; contenido en git antes del commit del triaje)
Effective atoms:
- atom-lo-que-el-código-dice-de-sí-mismo-se-publica-con-lo-que-no-se-pudo-probar-a-la-vista
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-20T12:13:28Z'
  authority: generated
  via: save_document_payload
id: task-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta-no-co
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files:
- src/sldb/store/diagnostics.py
- src/sldb/api/stores/store_check.py
- tests/store/test_diagnostics.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-lo-que-el-código-dice-de-sí-mismo-se-publica-con-lo-que-no-se-pudo-probar-a-la-vista
from_drawer: drawer task-stores-check-sobre-un-clon-sin-build-da-rc-1-con-2453-errores-missing-de-pythonsymboldoc-generados-y-tapa-los-errores-reales
  (retirado en el triaje 2026-11-16; contenido en git antes del commit del triaje)
---

# stores check sobre un clon sin build reporta los documentos generados ausentes como una alerta, no como miles de errores

## Rationale

_Explain why this task exists or the business driver behind it._

En un checkout limpio de sldb sin correr stores build, `sldb stores check --store .sldb` da FAIL con 2453 errores, todos PythonSymbolDoc "missing: tracked at knowledge/symbols/<id>.md, not on disk" (mensaje de src/sldb/store/diagnostics_models/document_diagnosis.py:85). knowledge/symbols/ está en .gitignore y esos documentos los genera selfdoc python-sync durante stores build, pero sus shards sí están versionados. Los errores reales quedan tapados. La declaración del store ya dice qué rutas son derivadas (StoreDeclaration.derived en src/sldb/api/stores/store_declaration.py; en este repo `derived: [knowledge/symbols/]` en .sldb/store.yaml), pero stores check no la lee. Se elige reportarlos como alerta resumida (opción reversible y local a stores check); dejar de trackear documentos generados es la decisión de la tarea de python-sync. Origen: drawer desk/drawer/tasks/task-stores-check-sobre-un-clon-sin-build-da-rc-1-con-2453-errores-missing-de-pythonsymboldoc-generados-y-tapa-los-errores-reales.md.

## Goal

_Describe the concrete result this task must produce._

En un store cuyo store.yaml declara rutas derived, un documento trackeado ausente cuya ruta cae bajo una de ellas no es error: stores check emite una sola alerta store/generated-missing con el número y el modelo ("2453 PythonSymbolDoc documents are generated and not on disk: run `sldb stores build`"), sigue reportando como error cualquier otro ausente, y su exit code depende solo de los errores.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/store/diagnostics.py (_diagnose_doc línea 36, diagnose_store línea 112) recibir la lista de prefijos derived (leída de la declaración del store) y, para un missing cuya ruta empieza por uno de ellos, contar en lugar de emitir error; al final emitir la alerta resumida por modelo. src/sldb/api/stores/store_check.py (línea 18) pasa la declaración. Tests en tests/store/test_diagnostics.py: store de prueba con derived: [gen/], 3 documentos trackeados ausentes bajo gen/ y 1 ausente fuera de gen/ -> 1 alerta que dice 3 y 1 error. Al cerrar, correr en un clon limpio en /dev/shm `sldb stores check --store .sldb` y `sldb stores build && sldb selfdoc check`, y anotar en el informe el rc y las alertas changed de selfdoc check que queden (resto de la nota de "main de sldb en verde", punto 2). CHANGELOG.md. No entra: destrackear PythonSymbolDoc (decisión de python-sync) ni cambiar selfdoc check.

Precisiones (preflight-1): store_check.py pasa a diagnose_store solo la lista de prefijos (list[str]) de StoreDeclaration.derived; el prefijo se compara por componentes de ruta (Path(ruta).parts empieza por Path(prefijo).parts), no por texto. La alerta es un Finding de nivel alert con code "store/generated-missing", subject "<Modelo>" y el texto de Goal, creado con la función alert() de sldb.core.finding como las demás alertas de stores check. Lo que se anota en result-summary.md es el rc de los dos comandos del clon y las líneas de selfdoc check con estado changed tal como salen.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer diagnostics.py, store_check.py, store_declaration.py y tests/store/test_diagnostics.py (test_missing_document, línea 78). 2) Pasar los prefijos derived. 3) Contar y resumir. 4) Tests. 5) Prueba en clon limpio e informe.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_diagnostics.py
- TMPDIR=/dev/shm pytest -q tests/test_serve_stores_check.py

## Done When

_Name the observable condition that makes the task complete._

Los dos comandos pasan con el test nuevo; en un clon limpio sin build stores check sale con 0 errores de PythonSymbolDoc y una alerta store/generated-missing; el informe lista las alertas de selfdoc check; CHANGELOG y commit.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta-no-co"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
