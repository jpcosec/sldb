FILE:desk/tasks/task-migrar-specsync-de-spec2viz-a-sldb-api-notations-junto-a-notationsync-y-palettesync-d1-b1-cierra-lo.md
---
sldb:
  by: agent
  at: '2026-11-15T15:52:53Z'
  authority: generated
  via: create_document
id: task-migrar-specsync-de-spec2viz-a-sldb-api-notations-junto-a-notationsync-y-palettesync-d1-b1-cierra-lo
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
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Migrar SpecSync de spec2viz a sldb.api.notations junto a NotationSync y PaletteSync (D1, B1, cierra lo pendiente de SV02)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: nunca reimplementar en un consumidor lo que es de sldb. NotationSync y PaletteSync ya están en sldb; SpecSync, que reconcilia un conjunto de specs (materializa y borra lo que salió), quedó en spec2viz.

## Goal

_Describe the concrete result this task must produce._

Reconciliar un conjunto de documentos de spec en un store: crear, actualizar y borrar SpecDoc, SpecNodeDoc y RelationDoc, con informe.

## Scope

_State what is in scope and what is out of scope._

SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE. Origen: el módulo sldb_sync de spec2viz (repo hermano spec2viz, 886 líneas; la parte de specs: clase SpecSync, spec_elements, spec_edges, spec_style_kinds, node_ref, edge_name, resolve_spec_notation, catalog_entries, check_catalog, sync_catalog y los formateadores de informe) y su test test_sldb_sync de spec2viz, más lo que use de test_catalog_notation. Destino: el paquete de notaciones de sldb.api donde ya viven NotationSync y PaletteSync, reutilizando su StoreWriter y SyncReport en vez de duplicarlos (en spec2viz hay una copia propia de _StoreWriter y SyncReport: converger en la de sldb). Exponerlo como API pública y en la CLI de notations. Paridad: los tests de spec2viz de esta pieza se portan a sldb, contra un store real y sin mocks. spec2viz NO se retira en este encargo: queda para el gate IR13; spec2viz podrá importar de sldb después. Cierra B1 del brief (reconciliar un conjunto de documentos).

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

SpecSync disponible en sldb con los tests portados verdes y la misma salida que spec2viz sobre los mismos specs; reconcilia borrando lo que salió del conjunto; suite de a un archivo, tools/check.sh y stores build --check.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-migrar-specsync-de-spec2viz-a-sldb-api-notations-junto-a-notationsync-y-palettesync-d1-b1-cierra-lo: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

