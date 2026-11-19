---
sldb:
  by: agent
  at: '2026-11-19T14:25:29Z'
  authority: generated
  via: save_document_payload
id: task-el-guard-de-escritura-por-campos-refuse-lossy-overwrite-rechaza-headings-no-declarados-que-viven-den
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- src/sldb/api/documents/lossy_overwrite.py
- src/sldb/api/documents/payload_save.py
- tests/api/test_structural_noise.py
- 9e168c33deac9f077bfed425cd4a37df0127b1d2
depends_on: []
pills: []
files:
- src/sldb/api/documents/lossy_overwrite.py
- src/sldb/api/documents/payload_save.py
- tests/api/test_structural_noise.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-la-escritura-por-campos-rechaza-solo-los-headings-o-claves-que-perderia
---

# El guard de escritura por campos (refuse_lossy_overwrite) rechaza headings no declarados que viven dentro del valor de un campo y sobreviven a la escritura

## Rationale

_Explain why this task exists or the business driver behind it._

Regresión de 6a4e5ec5, 2026-11-19. refuse_lossy_overwrite corre refuse_structural_noise sobre el texto actual del archivo y rechaza toda escritura por campos si hay headings que el modelo no declara, aunque estén dentro del valor de un campo (p. ej. un '### Validation' dentro de scope) y el render nuevo los conserve. Rompe tests/test_promotion_nesting.py::test_advance_task_keeps_nested_h3_sections_inside_scope de deskops: con deskops 7e8492ea pasa con sldb 6a4e5ec5^ y falla con 6a4e5ec5 ('ruido estructural en task-nested-active: ... 3 headings que TaskDoc no declara'). La suite de deskops está roja en main y bloquea sus integraciones.

## Goal

_Describe the concrete result this task must produce._

Una escritura por campos solo se rechaza si pierde contenido: headings (o claves de frontmatter) del archivo actual que no aparecen en el texto que se va a escribir. Los headings dentro del valor de un campo que el render conserva no bloquean la escritura. Lo que el guard rechazaba de verdad (contenido que se pierde) se sigue rechazando.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/documents/lossy_overwrite.py (y payload_save.py si hace falta pasarle el texto renderizado) y tests/api/test_structural_noise.py. Fuera: refuse_structural_noise de docs track/create, que no cambia.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests que fallen antes, en tests/api/test_structural_noise.py: (a) un documento cuyo campo de texto trae '### Sub' dentro del valor; save_document_payload cambiando otro campo escribe y el '### Sub' sigue en el archivo; (b) un documento con un heading no declarado fuera de todo campo (el caso que cubre 6a4e5ec5) sigue rechazándose. p2: en refuse_lossy_overwrite comparar los headings del texto actual con los del texto que se va a escribir y rechazar solo los ausentes en el nuevo (para el frontmatter, solo las claves ausentes); el mensaje sigue nombrándolos. p3: CHANGELOG. p4: quick_gates (bash tools/check.sh --fast) en 0 y commit con rutas nombradas y Task-Id. El integrador verifica con el test de deskops.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_structural_noise.py tests/api/test_transaction.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos y los de 6a4e5ec5 pasan; con este sldb, tests/test_promotion_nesting.py de deskops pasa.
