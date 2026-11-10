FILE:desk/tasks/task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024.md
---
sldb:
  by: agent
  at: '2026-11-10T07:24:16Z'
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
references: []
depends_on: []
pills: []
files:
- src/
- tests/
- tools/
- docs/
- pyproject.toml
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

Run 42758984024 (c1f41105). Job test, paso 'Structural gates' (tools/check.sh --fast): 24 archivos sin eje (api/rules/*, api/tags/*, api/views/*, core/finding_route.py); 3 modelos sin clasificar en el contrato (doc_anchor_value, rule_doc, transition_attributes); grados de dependencia de las unidades grafo, notacion y nucleo distintos de los declarados. Job store, paso 'Build deskops' store when it declares one': falla (log con SurfaceDoc y RelationDoc de pron). Además hay que correr los pasos que sigan, que el CI no alcanzó: pytest, python -m build, make world, build --check y selfdoc check. Causa raíz escrita por cada fallo antes del arreglo, sin skip ni xfail, y sin relajar los gates estructurales: se clasifica lo que falta.

## Implementation Path

_Outline the expected implementation route or affected surface._

PRECISIONES DE PROMOCIÓN (2026-11-10, coordinador del plan de deskops):
p1 (método, regla del dueño): por cada fallo, primero se reproduce y se escribe la causa raíz con evidencia (archivo, línea y el commit que lo introdujo, por git log/blame); recién entonces se arregla. Nunca skip, xfail, relajar un gate estructural ni bajar un umbral. Lo que falta clasificar se clasifica: a los 24 archivos sin eje se les da su eje, los 3 modelos sin clasificar entran en el contrato y los grados de dependencia de grafo, notación y núcleo se corrigen. Si un gate está mal (su expectativa quedó vieja), el informe lo prueba y se corrige el gate con su causa escrita.
p2 (los pasos del workflow, en un clon limpio de esta rama en /dev/shm, en el orden de .github/workflows/ci.yml):
- job test: (1) bash tools/check.sh --fast; (2) pytest, un proceso por archivo de test con TMPDIR=/dev/shm, de a uno, con la guarda de pgrep anclada; (3) python -m build.
- job store, con los hermanos al lado como en el CI: el clon de esta rama de sldb en /dev/shm/sci/sldb, deskops main en /dev/shm/sci/deskops y pron master en /dev/shm/sci/pron, clonados de GitHub. Pasos: (4) make world en pron; (5) en deskops, sldb stores build si existe .sldb/store.yaml; (6) en sldb, sldb stores build --check; (7) en sldb, sldb stores build && sldb selfdoc check. Con sldb y pron instalados desde esos clones (pip install -e en un venv aparte en /dev/shm, no el .venv compartido).
p3 (job store, «Build deskops' store»): el log trae SurfaceDoc y RelationDoc de pron. Hay que reproducir con deskops main actual (c66b4fad o posterior, que ya trae RuleDoc declarado y los links como alerta) antes de concluir: puede haber quedado arreglado por las tareas de link-absent y main-en-verde de deskops.
p4 (paralelo): wt/rule-graph-local (bdb9b0ff) espera a que este CI esté verde y no se integra antes. Esta tarea no lo incluye; si un fallo coincide con lo que esa rama toca (api/rules), el worker lo dice y coordinamos.
p5 (fallos sin tarea): si un fallo exige una decisión (por ejemplo, el eje correcto de un archivo no es obvio), el worker para y avisa con las opciones. El coordinador decide o abre tarea (p1 de main-en-verde de deskops).

## Validation

_List the checks required before this task can close._

- bash tools/check.sh --fast
- pytest (un proceso por archivo, TMPDIR=/dev/shm)
- gh run list --repo jpcosec/sldb --branch main --limit 1

## Done When

_Name the observable condition that makes the task complete._

El run de CI sobre el commit de cierre está en success y su URL queda en references; el informe nombra la causa raíz de cada fallo.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

