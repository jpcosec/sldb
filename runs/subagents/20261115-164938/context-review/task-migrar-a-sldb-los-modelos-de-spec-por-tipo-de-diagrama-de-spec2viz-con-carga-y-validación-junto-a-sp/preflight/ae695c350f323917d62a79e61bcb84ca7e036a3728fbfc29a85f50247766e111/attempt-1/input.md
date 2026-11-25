FILE:desk/tasks/task-migrar-a-sldb-los-modelos-de-spec-por-tipo-de-diagrama-de-spec2viz-con-carga-y-validación-junto-a-sp.md
---
sldb:
  by: agent
  at: '2026-11-15T15:53:12Z'
  authority: generated
  via: create_document
id: task-migrar-a-sldb-los-modelos-de-spec-por-tipo-de-diagrama-de-spec2viz-con-carga-y-validación-junto-a-sp
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

# Migrar a sldb los modelos de spec por tipo de diagrama de spec2viz, con carga y validación, junto a SpecDoc (D3)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: los modelos de spec son genéricos. Los compiladores y renderers se quedan en specIR (IR11 e IR12) como capa visual y consumen estos modelos en vez de redefinirlos.

## Goal

_Describe the concrete result this task must produce._

sldb aloja los modelos de spec de los ocho tipos de diagrama con su carga y validación.

## Scope

_State what is in scope and what is out of scope._

SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE. Origen: el paquete de modelos de spec2viz (modelo base y los de clase, secuencia, estado, componente, actividad, despliegue, matriz y reflexión; el de catálogo solo si no depende de los renderers), con su cargador (módulo loader) y su validador (módulo validator) y las excepciones que usan. Destino: junto a SpecDoc en los modelos de notación de sldb. Antes, comparar con SpecDoc y SpecNodeDoc existentes y no duplicar: los modelos de tipo validan el contenido del spec y SpecDoc lo guarda. Nada de compiladores ni renderers. Paridad: portar a sldb los tests de spec2viz test_base_model, test_models_activity, test_models_component, test_models_deployment, test_models_matrix, test_models_sequence, test_models_state, test_class_diagram, test_class_packages, test_loader, test_validator y test_exceptions, en lo que toquen solo modelos, carga y validación. spec2viz no se retira (gate IR13).

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

Los ocho modelos y su carga y validación en sldb, con los tests portados verdes y mismos errores que spec2viz sobre las mismas entradas; dependencias de spec2viz (pydantic u otras) declaradas en sldb solo si hacen falta; suite de a un archivo, tools/check.sh y stores build --check.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-migrar-a-sldb-los-modelos-de-spec-por-tipo-de-diagrama-de-spec2viz-con-carga-y-validación-junto-a-sp: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

