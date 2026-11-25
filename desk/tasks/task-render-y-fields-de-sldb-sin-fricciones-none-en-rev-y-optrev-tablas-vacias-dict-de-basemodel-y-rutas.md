---
sldb:
  by: agent
  at: '2026-11-25T12:34:42Z'
  authority: generated
  via: save_document_payload
id: task-render-y-fields-de-sldb-sin-fricciones-none-en-rev-y-optrev-tablas-vacias-dict-de-basemodel-y-rutas
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references:
- src/sldb/cli/commands/fields_mutate.py
- src/sldb/core/renderer_engine/base.py
- src/sldb/runtime/validation.py
- tests/test_rev_optrev_none.py
- b3dd710632c1ecdb09ce3bd5086093ff175c0d00
depends_on: []
pills: []
files:
- src/sldb/cli/commands/fields_mutate.py
- src/sldb/core/renderer_engine/base.py
- src/sldb/runtime/validation.py
- tests/test_rev_optrev_none.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-rev-y-optrev-con-none-renderizan-null-y-se-pueden-reescribir
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
