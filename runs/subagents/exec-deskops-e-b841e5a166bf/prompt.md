Task: task-render-y-fields-de-sldb-sin-fricciones-none-en-rev-y-optrev-tablas-vacias-dict-de-basemodel-y-rutas
Title: Render y fields de sldb sin fricciones: None en rev y optrev, tablas vacias, dict de BaseModel y rutas relativas de docs create
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-25T03:48:54Z'
  authority: generated
  via: save_document_payload
id: task-render-y-fields-de-sldb-sin-fricciones-none-en-rev-y-optrev-tablas-vacias-dict-de-basemodel-y-rutas
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261121-125747-unclear-fricciones-al-tipar-una-wiki-de-negocio-webprojects-agenda-wiki-paginas.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Render y fields de sldb sin fricciones: None en rev y optrev, tablas vacias, dict de BaseModel y rutas relativas de docs create

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261121-125747-unclear-fricciones-al-tipar-una-wiki-de-negocio-webprojects-agenda-wiki-paginas (sesion de minegocio, 21-nov, wiki de negocio en WebProjects/agenda): (1) un rev en None deja el marcador crudo en el Markdown; (2) un optrev en None borra la linea y despues fields update responde 'No value at field path' (igual con una clave null dentro de un dict tipado); (3) una tabla con lista vacia renderiza una fila basura que luego se extrae como dato; (4) un dict cuyo valor es BaseModel imprime '[warning] Template marker rev,dict•campo references unknown field' aunque funciona; (5) docs create -o con ruta relativa resuelve contra la carpeta del store y no contra el cwd, sin avisar.

## Goal

_Describe the concrete result this task must produce._

Contrato elegido: un marcador rev con valor None renderiza 'null' (y extract lo devuelve como None, round-trip), en vez de fallar; y un campo optrev que vale None se puede volver a poner con fields update <doc> <campo> <valor>.

## Scope

_State what is in scope and what is out of scope._

Render y extract de rev/optrev y fields update de un path con valor None, con tests. Fuera: tablas, BaseModel, docs create.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test NUEVO tests/test_rev_optrev_none.py con un modelo minimo (un campo rev Optional[str] y un campo optrev Optional[str]): (a) render de rev=None produce 'null' y extract lo devuelve None; (b) un documento con optrev None acepta fields update del campo a 'x' y el valor queda 'x'. 2) Arreglo en render/extract y fields update. Correr solo ese test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_rev_optrev_none.py

## Done When

_Name the observable condition that makes the task complete._

Los dos tests de None pasan.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-render-y-fields-de-sldb-sin-fricciones-none-en-rev-y-optrev-tablas-vacias-dict-de-basemodel-y-rutas"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-b841e5a166bf"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-b841e5a166bf`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-b841e5a166bf

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
