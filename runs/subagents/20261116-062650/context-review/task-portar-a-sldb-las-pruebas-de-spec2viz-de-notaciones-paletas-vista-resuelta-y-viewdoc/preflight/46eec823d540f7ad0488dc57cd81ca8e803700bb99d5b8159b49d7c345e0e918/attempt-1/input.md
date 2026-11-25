FILE:desk/tasks/task-portar-a-sldb-las-pruebas-de-spec2viz-de-notaciones-paletas-vista-resuelta-y-viewdoc.md
---
sldb:
  by: agent
  at: '2026-11-16T05:37:08Z'
  authority: generated
  via: save_document_payload
id: task-portar-a-sldb-las-pruebas-de-spec2viz-de-notaciones-paletas-vista-resuelta-y-viewdoc
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-192054-suggestion-sldb-notations-validar-una-notaci-n-una-paleta-o-un-spec-por-nombre-o-ruta-desde-la-cli.md
depends_on: []
pills: []
files:
- tests/notations/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Portar a sldb las pruebas de spec2viz de notaciones, paletas, vista resuelta y ViewDoc

## Rationale

_Explain why this task exists or the business driver behind it._

Desde SV01-SV04 sldb es dueño de los modelos de notación, paletas, el resolvedor de vistas y ViewDoc, pero las pruebas que los cubrían siguen en spec2viz. Como IR13c se retiró, nadie las porta, y al retirar spec2viz esa cobertura se pierde. Origen: desk/inbox/20261115-192054-suggestion-sldb-notations-validar-una-notaci-n-una-paleta-o-un-spec-por-nombre-o-ruta-desde-la-cli.md (segundo pedido de la nota).

## Goal

_Describe the concrete result this task must produce._

Cada caso de prueba de los siete archivos de spec2viz listados en Scope que aplica a código que hoy vive en sldb tiene un equivalente que pasa en tests/notations/ de sldb, importando solo sldb; los que no aplican quedan listados con su motivo en el docstring del archivo portado.

## Scope

_State what is in scope and what is out of scope._

Entra: leer /mnt/ssd/proyectos/SLDB_1/spec2viz/tests/test_notation.py, test_notation_view.py, test_style_palette.py, test_catalog_notation.py, test_catalog_resolved_views.py, test_view_contract_resolved.py y test_view_doc.py; por cada caso decidir si prueba algo que existe en sldb (sldb.api.notations, sldb.notations, sldb.models.notation) y, si existe, escribirlo en un archivo nuevo tests/notations/test_ported_from_spec2viz_<tema>.py con imports de sldb. Si un caso falla en sldb, no se arregla el código en esta tarea: se marca xfail con el motivo y se manda una nota al inbox de sldb con deskops message send. CHANGELOG.md. No entra: modificar spec2viz, cambiar código de src/sldb, ni portar pruebas de renderers (son de specIR).

Precisiones (preflight-1): un caso aplica si el símbolo que ejercita tiene equivalente en sldb con el mismo nombre o con nombre distinto pero misma firma y comportamiento documentado; en duda, se porta y, si falla, se marca xfail. Un archivo nuevo por archivo de spec2viz (test_ported_from_spec2viz_<nombre del archivo original sin test_>.py en tests/notations), cada uno con su docstring que lista los casos no portados y el motivo. La nota al inbox por un xfail se manda con deskops message send --to sldb --title "Paridad con spec2viz: <caso>" y como cuerpo el caso, el error y el archivo. Fixtures copiadas van a una carpeta fixtures dentro de tests/notations, con el nombre original.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario: por archivo de spec2viz, lista de tests y el símbolo que prueban. 2) Mapear cada símbolo a su equivalente en sldb con grep en src/sldb. 3) Portar con fixtures de tmp_path; datos de prueba copiados a tests/notations/fixtures/ si hacen falta. 4) Correr los archivos nuevos uno a uno. 5) Docstring con los casos no portados y su motivo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/ -k ported_from_spec2viz
- ! grep -rn 'import spec2viz\|from spec2viz' tests/notations/test_ported_from_spec2viz_*.py

## Done When

_Name the observable condition that makes the task complete._

Los archivos tests/notations/test_ported_from_spec2viz_*.py existen, pasan (con xfail solo donde se mandó nota al inbox) y no importan spec2viz; el docstring de cada uno lista los casos no portados con motivo; commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-portar-a-sldb-las-pruebas-de-spec2viz-de-notaciones-paletas-vista-resuelta-y-viewdoc: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

