---
sldb:
  by: agent
  at: '2026-11-11T09:31:40Z'
  authority: generated
  via: create_document
id: task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez
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
files:
- src/sldb/api/stores/
- tests/store/
- tests/api/
- docs/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-un-documento-que-cae-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-dos-veces.md
---

# Un documento en el glob de un modelo padre y en los paths de un modelo hijo se trackea una sola vez, bajo el hijo (gana el más específico)

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del coordinador, delante de H9. Rompe deskops view board en todo store de deskops construido en limpio (clon nuevo o CI): cada tarea queda trackeada dos veces y los selectores por nombre dan Ambiguous task selector.

## Goal

_Describe the concrete result this task must produce._

sldb resuelve un path nombrado por varias reglas include a una sola fila: gana el modelo hijo por paths sobre el glob del padre; sin herencia, error store/include-conflict; un store ya duplicado se corrige en el próximo build.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/stores/, tests/store/, tests/api/, docs/, CHANGELOG.md. Fuera: store.yaml de deskops y una vía de CLI para quitar includes.

## Implementation Path

_Outline the expected implementation route or affected surface._

Decisión del coordinador (2026-11-11, revisable): prioridad POR DELANTE de H9, detrás de la tarea de seguridad live_stale. Nota de origen: inbox 6f9576a7 (glob de modelo padre y paths de modelo hijo). Deskops la espera en su drawer bcf090a8.

REPRODUCCIÓN (coordinador; log runs/subagents/20261111-repro-dbltrack/repro.log): checkout limpio de deskops origin/main 64a5bcc7 con sldb 9c9dac6b. .sldb/store.yaml declara 'model: TaskDoc, glob: desk/tasks/task-*.md' y además cada tarea por 'paths' en su modelo hijo (TaskCodeDoc, TaskDebugDoc). Tras 'rm -rf .sldb_cache && sldb stores build --store .sldb' (rc 0), cada una de las 3 tareas queda trackeada dos veces (TaskDoc y su hijo). 'deskops view board' da 0 tareas y un 'Ambiguous task selector' por tarea. Lo hace cualquier clon nuevo y el CI; con una caché vieja no se ve.

CAUSA: src/sldb/api/stores/declared_files.py declared_files suma las filas (model, path, name) de cada regla include sin mirar si un mismo path ya lo nombra otra regla. apply_includes trackea cada fila, así que un archivo que cae en el glob del padre y en los paths del hijo queda trackeado bajo los dos modelos.

ARREGLO (vía fijada por el coordinador: gana el modelo más específico; no se toca store.yaml):
t1 (resolución): cuando un mismo path lo nombran varias reglas include, gana una sola fila. La de 'paths' explícitos gana sobre la de 'glob' si su modelo es descendiente del modelo del glob (herencia de modelos del store: base_names / contrato). Entre dos reglas del mismo tipo, o con modelos sin relación de herencia, no se elige: build y stores check dan un error 'store/include-conflict' que nombra el path y los modelos.
t2 (stores declare --write): conserva el glob autorado como hoy; con t1 ya no duplica.
t3 (un store ya construido con duplicados): el próximo build o stores update destrackea la fila perdedora (la del glob padre) y deja la del hijo, sin tocar el archivo. Idempotente.
t4 (tests): un store de prueba con modelo padre por glob y modelo hijo por paths sobre los mismos archivos, construido en limpio (sin caché). Cada archivo queda trackeado una sola vez bajo el hijo. Un selector por nombre resuelve sin ambigüedad. t3 se prueba sobre un store ya duplicado. El conflicto entre modelos sin herencia da el error. El test va en tests/store/ para que el CI construya en limpio.
t5 (deskops): el informe dice si el drawer de deskops bcf090a8 (quitar o migrar el glob TaskDoc) sigue haciendo falta con t1.

VALIDACIÓN: el worker corre los tests que toca, tests/store y tests/api de stores (build, declare, update, check), test_clean_code_rules y tools/check.sh --fast. Un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml; api/stores ya es carpeta declarada. Los 7 pasos del workflow los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test en tests/store con padre por glob e hijo por paths, build en limpio: una sola fila bajo el hijo
- Selector por nombre sin ambigüedad; store ya duplicado corregido por build/update (idempotente)
- Conflicto sin herencia da store/include-conflict
- test_clean_code_rules y check.sh --fast
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

t1-t5 hechos con causa raíz escrita y tests verdes; CHANGELOG y docs.
