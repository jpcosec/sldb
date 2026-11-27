---
sldb:
  by: agent
  at: '2026-11-27T18:01:31Z'
  authority: generated
  via: create_document
id: task-la-cli-expone-solo-las-operaciones-de-la-taxonomia-se-retiran-los-alias-los-grupos-legacy-y-lo-que-o
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-docs-architecture-command-taxonomy-md-lista-cada-operacion-de-sldb-una-sola-vez-con-las-cuatro-caras
pills: []
files: []
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La CLI expone solo las operaciones de la taxonomía: se retiran los alias, los grupos legacy y lo que otra operación ya hace

## Rationale

_Explain why this task exists or the business driver behind it._

JP, 2026-11-27: la CLI tiene 151 comandos hoja y no hace falta guardarlos todos; importa ordenarlos, no conservarlos. Que alguien los use no es razón para dejarlos. Es el paso 4 del ADR docs/architecture/one-command-taxonomy-served-by-fastmcp.md, y una condición para las pruebas externas por contrato de cada anillo: no se prueba lo que se va a retirar.

## Goal

_Describe the concrete result this task must produce._

Cada comando hoja de la CLI corresponde a una fila de docs/architecture/command-taxonomy.md con su nombre canónico; lo marcado para reemplazo ya no existe y cada consumidor del workspace que lo usaba llama a la operación que lo reemplaza.

## Scope

_State what is in scope and what is out of scope._

Dentro: el parser y el dispatcher de src/sldb/cli, sus tests, la ayuda y selfdoc, y avisar a cada consumidor (deskops, IR, graph_ui, marcado) por su inbox con el reemplazo de lo que usa. Fuera: sldb serve y sldb mcp (pasos 2 y 3 del ADR), cambiar lo que hace una operación.

## Implementation Path

_Outline the expected implementation route or affected surface._

Parte de la tabla aprobada por JP. Candidatos vistos el 2026-11-27 en refactor/anillos: los 11 alias ocultos en singular (store, model, doc), los 6 ocultos de raíz (ls, get, glob, raw-find, recover, compose) y el grupo legacy, que los duplica; journal show y verify (retirados, solo imprimen un aviso); stores migrate-hashes y migrate-layout si ningún store los necesita ya; búsquedas solapadas (find, explore, docs explore, sections find); graph project missing frente a edges unresolved y graph project edges frente a edges show; stores semantic-map y semantic-export frente al grupo semantic; tags check, que es rules check filtrado; sldb inbox frente a deskops message send; bench como herramienta de desarrollo y no operación del producto. Retirar un comando es quitarlo, no dejarlo oculto.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_command_taxonomy.py
- bash tools/check.sh

## Done When

_Name the observable condition that makes the task complete._

La prueba de la taxonomía falla si la CLI tiene un comando hoja sin fila o una fila marcada para reemplazo sigue en la CLI, y pasa; bash tools/check.sh pasa; cada consumidor afectado tiene su nota en el inbox.
