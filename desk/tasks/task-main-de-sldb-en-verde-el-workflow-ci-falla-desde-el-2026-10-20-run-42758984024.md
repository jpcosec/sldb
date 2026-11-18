---
sldb:
  by: agent
  at: '2026-11-18T04:32:53Z'
  authority: generated
  via: save_document_payload
id: task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
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

p1 (causa): el integrador la diagnosticó con evidencia de CI (run 44169114744, job 134343092734: 'Rebuild sldb's store from its sources' en success, 'Check generated CLI reference' cancelado a las 6 h) y con la ayuda de la CLI ('--check: Rebuild a scratch copy of the sources and compare, writing nothing here'). Es una hipótesis fuerte, no un hecho cerrado: el ejecutor la confirma en el código (archivo y línea de stores build --check y del paso del workflow) antes de cambiar nada, y si no se confirma, para y reporta. Nada de skip, xfail ni subir timeouts como arreglo. p2 (opciones, en orden de preferencia; el ejecutor elige con evidencia y lo justifica en el informe): (a) un solo build en el job: que el paso de referencia CLI reuse el store que deja el paso anterior. Por ejemplo, el paso 'Rebuild' corre sldb stores build (escribe) y después comprueba que el árbol versionado no cambió (git diff --exit-code sobre lo que --check compara), seguido de sldb selfdoc check. Antes de reemplazar --check hay que mostrar con el código qué compara --check y que la sustitución verifica lo mismo; si no es equivalente, (b). (b) una opción de sldb stores build que verifique y deje el store escrito (p. ej. --check que conserve el resultado o --write), con test. (c) aparte de (a) o (b), opcional: cachear knowledge/symbols con actions/cache, con clave en el hash de las fuentes que lo generan. p3 (reproducción local y criterio medible): clones en /dev/shm/sci/{sldb,deskops,pron}. deskops desde GitHub main y pron desde GitHub master. sldb se clona de GitHub y después se trae el commit local del ejecutor con: git -C /dev/shm/sci/sldb fetch /mnt/ssd/proyectos/SLDB_1/sldb <sha> && git -C /dev/shm/sci/sldb checkout --detach <sha> (el commit no está pusheado; se trae del checkout local). Sin knowledge/symbols, con el venv /mnt/ssd/proyectos/SLDB_1/.venv. Perímetro del cronómetro: solo los pasos del job store que van después de 'Install sldb and pron', es decir desde el inicio de 'Build deskops' store when it declares one' hasta el final del último paso del job (hoy 'Check generated CLI reference'). Cada paso se corre con /usr/bin/time -f '%e s' y en el orden de ci.yml. El total es la suma de esos tiempos. Se mide dos veces: con el ci.yml de origin/main (antes) y con el del commit del ejecutor (después). Build de referencia: un sldb stores build sin --check de ese mismo sldb (el commit del ejecutor), en la misma máquina, en la misma sesión y sin knowledge/symbols. Criterio de holgura: después hay exactamente un build completo, y el total del después no supera 1,2 veces ese build de referencia. p4 (dónde trabaja y cómo se cierra): el ejecutor commitea en el checkout /mnt/ssd/proyectos/SLDB_1/sldb, rama main local, con rutas nombradas (nunca git add -A ni -u sobre todo el árbol; hay trabajo ajeno sin commitear en sldb/surface/ y un stash que no se tocan) y sin push. Los cambios de .github/workflows/ci.yml no se pueden pushear sin el scope workflow; el integrador (wA:p1) corre la suite completa en copia limpia y pushea con jpcosec. El run de cierre es el de CI cuyo headSha es el commit integrado: gh run list --repo jpcosec/sldb --commit <sha> --json status,conclusion,url. p5: informe en el run dir que fija el despacho (runs/subagents/exec-<nombre del agente scion>/result-summary.md; el brief del ejecutor trae la ruta exacta) con la causa confirmada, la opción elegida y por qué, los tiempos y el número de builds antes y después y los comandos de la reproducción. p6: si --check y la sustitución discrepan en lo que verifican, o si hace falta una decisión de diseño, el ejecutor para y reporta con las opciones.

## Validation

_List the checks required before this task can close._

- bash tools/check.sh --fast
- pytest -q -n 4 -p no:cacheprovider (suite completa; la corre el integrador en copia limpia)
- reproducción local del job store (p3): rc 0 en todos los pasos, exactamente un build completo y tiempo total <= 1,2 x un build, con los tiempos en el informe
- gh run list --repo jpcosec/sldb --commit <sha integrado> --json status,conclusion,url: success en test 3.12, test 3.13 y store

## Done When

_Name the observable condition that makes the task complete._

El run de CI sobre el commit integrado en main termina en success (test 3.12, test 3.13 y store) y su URL queda en references. El job store construye el store una sola vez.
