FILE:desk/tasks/task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024.md
---
sldb:
  by: agent
  at: '2026-11-18T04:11:40Z'
  authority: generated
  via: save_document_payload
id: task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-231010-suggestion-el-job-store-del-ci-de-sldb-no-termina-stores-build-check-regenera-knowledge-symbols-y-supera-las-6-h-del-runner.md
- desk/inbox/20261117-232608-suggestion-ci-store-build-check-pasa-en-ci-lo-que-corta-las-6-h-es-el-segundo-stores-build-del-paso-de-referencia-cli.md
- .github/workflows/ci.yml
depends_on: []
pills: []
files:
- .github/workflows/ci.yml
- src/
- tests/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# main de sldb en verde: el workflow CI falla desde el 2026-10-20 (run 42758984024)

## Rationale

_Explain why this task exists or the business driver behind it._

El CI de main de sldb no tiene una corrida verde desde el 2026-10-20 (39464199660). Los nodos de grafo-operable y generalizar-desde-deskops se integraron con tests dirigidos. Regla del dueño: un fallo conocido sin tarea no existe.

## Goal

_Describe the concrete result this task must produce._

El workflow CI de sldb (jobs test 3.12/3.13 y store) termina en success sobre main.

## Scope

_State what is in scope and what is out of scope._

Estado al 2026-11-18 (sldb origin/main d764b9fd): los fallos de la versión anterior de esta tarea ya están resueltos. Los jobs test 3.12 y 3.13 están en verde desde ca73071d (testpaths). En el job store pasan 'Build deskops' store', 'Prepare pron's store' (make world; pron a0c4100 enlaza ../deskops/.sldb) y 'Rebuild sldb's store from its sources' (sldb stores build --check). El run 44169114744 (6d87f126) se canceló a las 6 h en 'Check generated CLI reference', que corre 'sldb stores build && sldb selfdoc check'. La causa: stores build --check reconstruye una copia scratch y no escribe nada, así que el paso siguiente construye el store completo otra vez. En robocop2, sin knowledge/symbols (gitignored, se regenera), un build tarda 110 min con un núcleo al 100 %; con symbols presente, unos 55 min. El runner es varias veces más lento. En alcance: que el job store construya el store una sola vez y termine con holgura dentro del límite de 6 h del runner, sin perder ninguna comprobación (lo que verifica --check y el selfdoc check siguen verificándose). Fuera de alcance: optimizar la generación de símbolos más allá de lo necesario, y cambios en deskops o pron.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1 (método): primero reproducir y escribir la causa con evidencia (archivo y línea), después arreglar. Nada de skip, xfail ni subir timeouts como arreglo. p2 (opciones, en orden de preferencia; el ejecutor elige con evidencia y lo justifica en el informe): (a) un solo build en el job: que el paso de referencia CLI reuse el store que deja el paso anterior. Por ejemplo, el paso 'Rebuild' corre sldb stores build (escribe) y después se comprueba que el árbol versionado no cambió (git diff --exit-code sobre lo que --check compara), seguido de sldb selfdoc check. Antes de reemplazar --check hay que mostrar con el código (src/sldb/.../stores build) qué compara --check y que la sustitución verifica lo mismo; si no es equivalente, (b). (b) una opción de sldb stores build que verifique y deje el store escrito (p. ej. --check que conserve el resultado o --write), con test. (c) aparte de (a) o (b), opcional: cachear knowledge/symbols con actions/cache, con clave en el hash de las fuentes que lo generan. p3 (reproducción local, igual que el job): clones de GitHub en /dev/shm/sci/{sldb,deskops,pron} (sldb de la rama del ejecutor, deskops main, pron master), sin knowledge/symbols, con el venv /mnt/ssd/proyectos/SLDB_1/.venv. Pasos del job store en el orden de ci.yml. Medir el tiempo total del job antes y después; el criterio es que después haya un solo build completo. p4: los cambios de .github/workflows/ci.yml no se pueden pushear con OAuth sin el scope workflow; el ejecutor commitea en local y el integrador (wA:p1) pushea con jpcosec. p5: informe en runs/subagents/<run>/result-summary.md con la causa, la opción elegida y por qué, los tiempos antes y después y los comandos de la reproducción. p6: si --check y la sustitución discrepan en lo que verifican, o si hace falta una decisión de diseño, el ejecutor para y reporta con las opciones.

## Validation

_List the checks required before this task can close._

- bash tools/check.sh --fast
- pytest -q -n 4 -p no:cacheprovider (suite completa; la corre el integrador en copia limpia)
- reproducción local del job store (p3): rc 0 en todos los pasos y un solo build completo, con los tiempos en el informe
- gh run list --repo jpcosec/sldb --branch main --limit 1

## Done When

_Name the observable condition that makes the task complete._

El run de CI sobre el commit integrado en main termina en success (test 3.12, test 3.13 y store) y su URL queda en references. El job store construye el store una sola vez.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

