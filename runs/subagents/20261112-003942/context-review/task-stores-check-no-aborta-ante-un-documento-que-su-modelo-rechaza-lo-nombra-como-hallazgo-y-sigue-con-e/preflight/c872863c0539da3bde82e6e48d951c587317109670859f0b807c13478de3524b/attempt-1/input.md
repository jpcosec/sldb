FILE:desk/tasks/task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e.md
---
sldb:
  by: agent
  at: '2026-11-12T00:38:54Z'
  authority: generated
  via: create_document
id: task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e
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
- src/sldb/store/
- src/sldb/api/stores/
- src/sldb/cli/commands/
- tests/
- docs/
- CHANGELOG.md
- contracts/layers.toml
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-stores-check-aborta-en-el-primer-documento-inv-lido-toda-escritura-re-extrae-el-modelo-entero-rollback-incompleto-hallado-por-el-task-debug-de-estados-heredados-de-deskops.md
---

# stores check no aborta ante un documento que su modelo rechaza: lo nombra como hallazgo y sigue con el resto (H1 de la nota 3895e9f7); H2 y H3 quedan con tests de regresión

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del coordinador: un desk heredado (los de AntonIA, el gateway) con un documento que su modelo rechaza no puede diagnosticarse. sldb stores check sale con Unexpected: 1 validation error, rc 1, sin JSON ni el resto del diagnóstico. Reproducido sobre sldb main ce27c82b. Las otras dos hipótesis de la nota (H2, toda escritura re-extrae el modelo entero y cae en otro inválido; H3, rollback incompleto) ya no se reproducen en main.

## Goal

_Describe the concrete result this task must produce._

sldb stores check sobre un store con documentos que su modelo rechaza termina el diagnóstico: cada documento inválido es un hallazgo por documento con su código, el resto del store se diagnostica como hoy, y la salida JSON está completa; H2 y H3 quedan cubiertos por tests de regresión que fijan el comportamiento actual.

## Scope

_State what is in scope and what is out of scope._

En alcance: el diagnóstico del store (sldb.store.diagnostics: diagnose_store, _diagnose_model, _diagnose_doc, _fields_state y lo que extrae con el modelo por documento), el hallazgo nuevo y su código en los hallazgos de store, el CLI stores check, tests, docs y CHANGELOG. Fuera: la guarda preventiva de deskops que rechaza cerrar con dos inválidas (es de deskops, parte 2 de 75e33dab, otra tarea), la seguridad de lecturas (source_read, ya cerrada) y cambiar qué valida cada modelo.

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: nota de inbox 3895e9f7 (H1-H3, del task.debug de estados heredados de deskops).

REPRODUCCIÓN (coordinador, sldb main ce27c82b con deskops main 0ccf497c; runs/subagents/20261111-repro-h123/repro.sh y repro.log). Un desk de deskops en /dev/shm con tres task.code; dos pasan a un estado que el modelo rechaza (status draft con history [task_activates, task_hands_to_closeout]).
H1, SE REPRODUCE: sldb stores check sale rc 1 con la línea Unexpected: 1 validation error for TaskCodeDoc, sin el resto del diagnóstico.
H2, NO SE REPRODUCE: sldb docs untrack de la tarea válida, y también el de una inválida mientras la otra sigue inválida, dan rc 0 y escriben solo sus índices. deskops closeout supersede de una inválida, con la guarda preventiva de deskops desactivada por monkeypatch, cierra con rc 0 aunque la otra siga inválida.
H3: sin la falla de H2 no hay transacción fallida que deje índices a medio escribir; no se reproduce.

CAUSA DE H1 (a confirmar): según la nota, diagnose_store → _diagnose_model → _diagnose_doc → _fields_state → hash_fields_with_map → extract_model_data no tiene guarda por documento, y el ValidationError sale de check_store hasta sldb.cli.main.

ARREGLO (r1-r5):
r1 (H1): el diagnóstico captura el ValidationError de extraer un documento con su modelo y lo convierte en un hallazgo por documento: código nuevo store/doc-invalid (o el nombre que encaje con los existentes), severidad error, el mensaje de pydantic resumido y el documento nombrado. El resto del store se diagnostica igual, y stores check imprime el informe completo (texto y JSON) con rc 1 por el error, sin Unexpected.
r2: el mismo hallazgo protege las otras rutas de stores check que extraen con el modelo (contrato movido, secciones, aristas) para ese documento: un documento inválido aparece una sola vez, no una vez por subsistema.
r3 (H2 y H3, regresión): tests que fijan lo que hoy pasa: con dos documentos inválidos en el mismo modelo, untrack de cualquiera de ellos y una escritura transaccional de un documento válido del modelo terminan bien y no tocan los otros. El informe dice qué commit de sldb dejó de reproducir H2 (git bisect sobre la reproducción, o el mecanismo leído en el código) y por qué.
r4: tests/test_clean_code_rules.py OBLIGATORIO (80 líneas efectivas por archivo, 10 de lógica por función, sin subir límites). Un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml; los grados medidos se actualizan con comentario fechado si cambian (tools/check.sh --fast).
r5: docs (el capítulo de stores check y los códigos de hallazgo) y CHANGELOG.

VALIDACIÓN: el worker corre de a uno los tests que toca y, antes de entregar, la suite COMPLETA de sldb de a un archivo desde /dev/shm (cada uno precedido por la espera con wait-pytest), más test_clean_code_rules y tools/check.sh --fast. Los 7 pasos del workflow de sldb los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test nuevo: stores check sobre un store con dos documentos que su modelo rechaza da rc 1, un hallazgo por documento con su código y el resto del diagnóstico, sin Unexpected; la salida JSON los trae
- Tests de regresión H2/H3: untrack de un inválido con otro inválido en el modelo y una escritura transaccional de un válido terminan bien y no tocan los otros
- test_clean_code_rules (obligatorio) y tools/check.sh --fast
- suite completa de sldb de a un archivo desde /dev/shm en verde
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

r1-r5 hechos con la causa raíz escrita en el informe antes del arreglo, el commit que resolvió H2 identificado, tests verdes y la suite completa en verde; docs y CHANGELOG actualizados.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

