FILE:desk/tasks/task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la.md
---
sldb:
  by: agent
  at: '2026-11-12T02:26:13Z'
  authority: generated
  via: create_document
id: task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la
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
- src/sldb/api/documents/
- src/sldb/api/rules/
- src/sldb/api/tags/
- src/sldb/api/stores/
- src/sldb/cli/commands/
- tests/
- docs/architecture/rules.md
- docs/architecture/tags.md
- CHANGELOG.md
- contracts/layers.toml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-on-write-no-se-eval-a-en-create-document-ni-en-track-document-file.md
---

# sldb: create_document y track_document_file evalúan las reglas on_write (H4), declare --write conserva la declaración de tags (H5), la familia de tags da su evaluación estructurada (H6) y se documenta qué documentos ve (H7)

## Rationale

_Explain why this task exists or the business driver behind it._

Hipótesis H4-H7 de CC35d resto de deskops (notas de inbox de sldb, la de H4 del puente q18 y la de H5-H7) y seguimiento de GD27. Hoy un documento nuevo entra por create_document o track_document_file sin pasar por las reglas on_write ni por la familia builtin:tag_namespace, y deskops mantiene un puente que repite esa validación; regenerar store.yaml con stores declare --write borra la declaración de tags; y deskops tiene que leer la evaluación de la familia parseando el texto de un hallazgo.

## Goal

_Describe the concrete result this task must produce._

create_document y track_document_file evalúan on_write como save (H4); stores declare --write conserva tag_namespaces y tag_models (H5); un hallazgo de la familia de tags lleva su evaluación estructurada y rules check, rules explain y tags check la exponen en su salida JSON (H6); la guía de reglas y de tags dice qué documentos ve la familia (H7).

## Scope

_State what is in scope and what is out of scope._

En alcance: la evaluación on_write en la creación y el tracking de documentos, la declaración conservada, el dato estructurado de los hallazgos de la familia de tags y su salida JSON, docs, tests y CHANGELOG. Fuera: borrar el puente de deskops (es otra tarea de deskops que corre cuando esta entre), que stores build evalúe on_write, y cambiar qué reglas existen.

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: ítem de drawer del seguimiento de GD27 (on_write no se evalúa en create_document ni en track_document_file), nota de inbox de H4 (q18) y nota de H5-H7 de CC35d resto.

ESTADO ACTUAL: check_on_write (rules_on_write.py) solo se llama desde save_document_payload, vía check_rules_on_write de payload_save_steps.py. create_document y track_document_file no lo llaman. declare_store (stores declare --write) conserva solo generate y derived de la declaración vigente. Un hallazgo de la familia de tags lleva su evaluación como texto, con el formato cláusula y entre paréntesis seen y un JSON.

CAMBIO (q1-q5), en este orden:
q1 (H5): declare_store conserva tag_namespaces y tag_models de la declaración vigente, igual que generate y derived. El worker revisa si StoreDeclaration tiene otra clave autorada que declare --write pierda, y la suma si la hay (lo dice en el informe). Test: una declaración con tags regenerada por stores declare --write queda igual.
q2 (H4), decisión del coordinador, revisable: create_document y track_document_file evalúan las reglas on_write, las de usuario y la familia builtin:tag_namespace, con el mismo criterio que save: una violación lanza SLDBRuleViolationError y no se escribe ni se trackea nada. apply_batch, /save con create y track, transaction.create y transaction.track y scaffold_store lo heredan. stores build (el tracking en lote de apply_includes) NO evalúa on_write: es declarativo y stores check ya lo cubre con on_check (revisable; el worker lo deja dicho en la guía de reglas). Cambio de contrato de las reglas de usuario: sección de on_write de docs/architecture/rules.md.
q3 (H6): el hallazgo de la familia de tags lleva su evaluación estructurada (namespace, tags, lo que falta) como dato propio, el mismo que hoy va dentro del texto, y rules check, rules explain y tags check lo exponen en su salida JSON. El texto del hallazgo no cambia. Test que lo lee sin parsear texto.
q4 (H7): la guía de reglas y la de tags dicen que la familia solo ve documentos indexados: un documento escrito a mano no tiene hallazgos hasta que se trackea, y uno editado se evalúa sobre su proyección indexada. Sin cambio de código.
q5: tests de q2: crear y trackear un documento que viola una regla on_write se rechaza sin escribir nada; uno que no la viola pasa; apply_batch y transaction.create heredan el rechazo y la transacción restaura el árbol; stores build sigue sin evaluar. tests/test_clean_code_rules.py es obligatorio (80 líneas efectivas por archivo, 10 de lógica por función, sin subir límites; un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml, y los grados medidos salen de tools/check.sh --fast). Docs y CHANGELOG.

VALIDACIÓN: el worker corre de a uno los tests que toca; antes de entregar, la suite completa de sldb de a un archivo desde /dev/shm, test_clean_code_rules y tools/check.sh --fast. Los 7 pasos del workflow de sldb los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Tests de H4: crear y trackear un documento que viola una regla on_write se rechaza sin escribir; apply_batch y transaction.create heredan el rechazo y restauran el árbol; stores build sigue sin evaluar
- Test de H5: stores declare --write sobre una declaración con tag_namespaces y tag_models la deja igual
- Test de H6: la evaluación estructurada de un hallazgo de la familia sale en la salida JSON de rules check y de tags check, sin parsear texto
- test_clean_code_rules (obligatorio) y tools/check.sh --fast
- suite completa de sldb de a un archivo desde /dev/shm en verde
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

q1-q5 hechos, tests verdes y la suite completa en verde; docs y CHANGELOG actualizados; las notas de H4 y de H5-H7 y el ítem de drawer de origen se dan de baja por CLI al cierre.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

