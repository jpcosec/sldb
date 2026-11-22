Task: task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda
Title: El guard de sobrescritura con pérdida acepta quitar un encabezado no declarado si su contenido queda en un campo del texto nuevo
Status: active
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-22T11:53:39Z'
  authority: generated
  via: save_document_payload
id: task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-3fca8df15867 FALLA. La roja de ''identidad''
  por workbench_demo es la excepción autorizada y el tester tampoco la usó como motivo.
  El bloqueante es real.


  _heading_bodies reconoce solo encabezados ATX en la columna 0 (_HEADING_LINE = ^(#{1,6})...).
  En cambio scan_headings, que alimenta report.undeclared, usa el AST de Markdown
  y también ve encabezados setext e indentados. Para esos, bodies.get(line, [""])
  cae en el default [""], y all(body in target ...) con "" siempre da verdadero: el
  guard los toma por conservados y deja perder su cuerpo.


  Reproducción del tester con TicketDoc: ''## Tags'' declarado, más un encabezado
  setext h2 no declarado (''Lost Section'' subrayado con guiones) con ''content only
  here'' debajo. save_document_payload con title, status y tags guarda sin error y
  el contenido se pierde.


  Intento 2:

  1. Que los cuerpos salgan del mismo escaneo que scan_headings: el AST, con sus rangos
  de líneas. Así cada encabezado que reporta como no declarado tiene su cuerpo real,
  sea ATX, setext o indentado.

  2. Un encabezado perdido sin cuerpo encontrado no puede contar como conservado.
  Si no se pudo calcular su cuerpo, se rechaza (falla cerrado).

  3. Agregar los tests de setext e indentado (rechazo cuando el cuerpo se pierde,
  aceptación cuando sobrevive), además de los dos que ya hay.

  4. Correr tests/api completo con -n 4 y tests/test_extraction_segments.py.

  5. Commit desde tu worktree con ''git commit -- <rutas>'' y el trailer Task-Id.'
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El guard de sobrescritura con pérdida acepta quitar un encabezado no declarado si su contenido queda en un campo del texto nuevo

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-22: un ejecutor de deskops (tarea 'los 4 átomos de salud del desk dejan de dar store/structural-noise en sldb stores check') quedó bloqueado. Para limpiar el ruido estructural de 4 átomos hay que plegar sus encabezados no declarados (por ejemplo '## Tags') en el campo answer, cuyo contenido ya está en el campo tags. Pero refuse_lossy_overwrite (src/sldb/api/documents/lossy_overwrite.py:18) rechaza toda escritura de campo mientras el archivo tenga encabezados no declarados que no sobreviven en el texto renderizado, aunque su contenido sí quede (como párrafo '**Heading:** ...' en answer, o en tags). Hoy la única salida es la política structural_noise: allow en store.yaml o editar a mano, y las dos están vedadas: no hay forma por CLI de limpiar ese ruido.

## Goal

_Describe the concrete result this task must produce._

refuse_lossy_overwrite no rechaza la escritura cuando cada encabezado no declarado que se pierde tiene su contenido (el texto bajo el encabezado, normalizado en espacios) presente en el texto renderizado nuevo: en el valor de algún campo o como párrafo. Sigue rechazando si se pierde contenido. Un test cubre los dos casos, y la limpieza de ruido estructural de un documento con un '## Tags' cuyo contenido ya está en el campo tags pasa por 'sldb fields set' o 'deskops edit atom'.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/documents/lossy_overwrite.py, su test y CHANGELOG. Fuera: la política structural_noise y otros guards.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: un documento con un encabezado no declarado cuyo texto se reescribe dentro de un campo; la escritura hoy es rechazada y debe pasar. p2: test de que si el contenido no aparece, se sigue rechazando. p3: implementar la comparación de contenido (normalizando espacios y quitando el marcado del encabezado). p4: tests de tests/api relacionados (grep -rln lossy tests/) y la suite con -n 4. p5: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo. La puerta 'identidad' de check.sh --fast en rojo por workbench_demo es la excepción autorizada (f055723d).

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider -n 4 tests/api

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos y los tests de lossy existentes pasan.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-01426e49e09c-a2`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-01426e49e09c-a2

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
