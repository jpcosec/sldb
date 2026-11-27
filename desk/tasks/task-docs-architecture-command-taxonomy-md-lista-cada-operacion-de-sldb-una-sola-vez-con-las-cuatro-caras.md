---
sldb:
  by: agent
  at: '2026-11-27T23:32:03Z'
  authority: generated
  via: save_document_payload
id: task-docs-architecture-command-taxonomy-md-lista-cada-operacion-de-sldb-una-sola-vez-con-las-cuatro-caras
status: draft
summary: 'Integrada en PR #6: la tabla está en docs/architecture/command-taxonomy.md
  y tests/test_command_taxonomy.py la mantiene completa. Falta que JP apruebe los
  nombres y las marcas.'
tags: []
current_node: ritual-execution
history: []
references:
- 22a9ad8f31ca743a30643eabdc8211d5c127a850
- tests/test_command_taxonomy.py
- docs/architecture/command-taxonomy.md
depends_on: []
pills: []
files: []
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# docs/architecture/command-taxonomy.md lista cada operación de sldb una sola vez, con las cuatro caras que la exponen hoy

## Rationale

_Explain why this task exists or the business driver behind it._

ADR docs/architecture/one-command-taxonomy-served-by-fastmcp.md (JP, 2026-11-25): sldb creció sin una taxonomía de comandos. sldb.api tiene 192 nombres públicos, la CLI unos 20 grupos, sldb serve unas 30 rutas y sldb mcp 15 herramientas; los nombres no coinciden y cada cara cubre un subconjunto distinto. La taxonomía es el paso 1 del ADR y de ella dependen el servidor fastmcp y el compositor de interfaces.

## Goal

_Describe the concrete result this task must produce._

Una tabla de operaciones que JP pueda aprobar: cada operación con sustantivo, verbo, si lee o escribe, nivel de permiso, y el nombre con que aparece hoy en sldb.api, en la CLI, en sldb serve y en sldb mcp; con duplicados, huecos y renombres marcados y un nombre canónico propuesto.

## Scope

_State what is in scope and what is out of scope._

Dentro: el documento docs/architecture/command-taxonomy.md y una prueba que lo mantiene completo. Fuera: renombrar o mover código, el servidor fastmcp, tocar la CLI. Es un inventario; no cambia comportamiento. Criterio de JP (2026-11-27): la tabla ordena, no conserva. Que alguien use un comando no es razón para dejarlo; si otra operación hace lo mismo, se marca para reemplazo y su fila nombra con qué. Una operación sobrevive si es un sustantivo-verbo propio de la taxonomía, no por existir hoy en una cara. La tabla marca además el anillo de cada operación (docs/spec/mecanismos/anillos.md).

## Implementation Path

_Outline the expected implementation route or affected surface._

Antes de crear nada, revisar si SurfaceDoc (knowledge/surfaces/) y sldb selfdoc ya guardan y chequean parte de esto, y decir en el documento qué se reutiliza. Leer el ADR y docs/architecture/mcp.md. Los nombres se sacan del código (sldb.api.__all__, el parser de la CLI, el enrutador de src/sldb/cli/serve, el registro de src/sldb/mcp), no a mano.

Aclaraciones de la revisión: público = sldb.api.__all__; comando hoja = subcomando de argparse sin subcomandos propios (sin alias ni ocultos aparte; los ocultos van en la lista final); rutas = cada (método, path) de sldb serve, sin /docs, /openapi.json ni estáticos. Nivel de permiso con tres valores: lee, escribe-store, efecto-externo (git, red, procesos); una operación que lee y escribe es escribe-store. Nombre canónico en snake_case sustantivo_verbo (p. ej. documents_create); en empate, el nombre de sldb.api. Sin operación = nombre que es alias, ayuda o utilidad interna, con su motivo en una línea. SurfaceDoc/selfdoc: se citan como fuente cuando ya registran la operación; no se modifican. La aprobación de JP es posterior y fuera de esta tarea.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_command_taxonomy.py

## Done When

_Name the observable condition that makes the task complete._

Cada nombre público de sldb.api, cada comando hoja de la CLI, cada ruta de sldb serve y cada herramienta de sldb mcp aparece en exactamente una fila, o en una lista final "sin operación" con su motivo. Cada fila dice si lee o escribe. Las filas con más de un nombre para lo mismo y las operaciones que faltan en alguna cara están marcadas. La prueba falla si se agrega una ruta, una herramienta, un comando o un nombre público que no esté en el documento.
