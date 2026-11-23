---
sldb:
  by: agent
  at: '2026-11-23T17:55:02Z'
  authority: generated
  via: save_document_payload
id: task-render-y-fields-de-sldb-sin-fricciones-none-en-rev-y-optrev-tablas-vacias-dict-de-basemodel-y-rutas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
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

Cada uno de los cinco casos tiene un test que hoy falla y pasa despues: rev None da null o error claro, optrev None se puede volver a poner con fields update, una tabla vacia no renderiza fila ni extrae dato, el warning falso desaparece, y docs create -o resuelve contra el cwd (o avisa).

## Scope

_State what is in scope and what is out of scope._

Render, extract y fields de sldb y docs create; tests en tests/. Fuera: serve y surface.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Un test por caso con un modelo minimo. 2) Arreglo en render/extract de marcadores rev y optrev con None y de tablas vacias. 3) fields update de un path cuyo valor es None. 4) Resolucion del marcador rev,dict con BaseModel. 5) Ruta de docs create -o.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q -n 4 tests/

## Done When

_Name the observable condition that makes the task complete._

Los cinco tests nuevos pasan y la suite de render, extract y fields sigue verde.
