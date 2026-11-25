---
sldb:
  by: agent
  at: '2026-11-25T01:22:16Z'
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

Los marcadores rev y optrev con valor None: rev None renderiza null o da un error claro, y un optrev None se puede volver a poner con fields update.

## Scope

_State what is in scope and what is out of scope._

Render y extract de rev/optrev y fields update de un path con valor None, con tests. Fuera: tablas, BaseModel, docs create.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test de rev None y de optrev None reescrito por fields update, con un modelo minimo. 2) Arreglo. Correr solo ese test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_rev_optrev_none.py

## Done When

_Name the observable condition that makes the task complete._

Los dos tests de None pasan.
