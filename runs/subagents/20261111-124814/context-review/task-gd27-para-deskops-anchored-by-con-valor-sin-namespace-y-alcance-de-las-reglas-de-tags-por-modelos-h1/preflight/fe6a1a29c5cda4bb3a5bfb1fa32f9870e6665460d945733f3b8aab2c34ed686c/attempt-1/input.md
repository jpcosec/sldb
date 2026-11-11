FILE:desk/tasks/task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1.md
---
sldb:
  by: agent
  at: '2026-11-11T12:47:53Z'
  authority: generated
  via: create_document
id: task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1
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
- src/sldb/api/stores/tag_namespace.py
- src/sldb/api/stores/store_declaration.py
- src/sldb/api/rules/builtin_tag_rules.py
- src/sldb/api/tags/
- src/sldb/cli/commands/tags.py
- tests/
- docs/architecture/tags.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-tag-namespaces-acotado-por-modelos-y-tag-folder-con-segmentos-vac-os-bloquea-cc35d.md
---

# GD27 para deskops: anchored_by con valor sin namespace y alcance de las reglas de tags por modelos (H1-H2); tag_folder estricto documentado (H3)

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del coordinador: es lo que más destraba. Libera el resto de CC35d de deskops (dominios, namespaces y tag_folder por la API de sldb) y con eso el camino a CC51.

## Goal

_Describe the concrete result this task must produce._

anchored_by acepta un campo con el valor pelado (value: bare); la declaración del store acota las reglas de tags a unos modelos (tag_models); tag_folder sigue estricto y documentado.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/stores/tag_namespace.py, src/sldb/api/stores/store_declaration.py, src/sldb/api/rules/builtin_tag_rules.py, src/sldb/api/tags/, src/sldb/cli/commands/tags.py, tests/, docs/architecture/tags.md, CHANGELOG.md. Fuera: cambios en deskops (los hace CC35d resto).

## Implementation Path

_Outline the expected implementation route or affected surface._

Prioridad del coordinador (2026-11-11): libera el resto de CC35d de deskops (drawer 'CC35d resto', DO7) y con eso el camino a CC51. Drawer de origen: 6b34cd5f (GD27 para deskops, H1-H3, hallado por CC35d de deskops, wt/cc35d 568d2140, runs/subagents/cc35d-worker-report.md).

PROBLEMA (de CC35d):
- B1/H1: el anchored_by de GD27 exige que el campo del documento ancla valga el tag completo ('domain:a.b'). CrossroadDoc.path de deskops vale 'a.b'. Con el crossroad existente, la API da igual 5 hallazgos y tag_tree devuelve roots=[].
- B2/H2: declarar tag_namespaces desde desk/tag-namespaces.yaml de deskops da 115 errores nuevos (workspace 78, pill-type 29, ...), y on_write rechazaría tareas y pills. Hoy la familia builtin:tag_namespace exige que todo namespace usado en cualquier documento del store esté declarado, y deskops solo registra los namespaces de los átomos.
- H3: tag_folder da ValueError con segmentos vacíos ('a..b', 'a.'), y deskops los ignoraba.

CAUSA: src/sldb/api/stores/tag_namespace.py y src/sldb/api/rules/builtin_tag_rules.py (anchors_of compara el campo con el tag completo; las reglas de la familia corren sobre todos los documentos locales con tags).

ARREGLO (g1-g4):
g1 (H1, anchored_by con valor pelado): anchored_by admite una clave opcional 'value' con 'tag' (por defecto, el comportamiento de hoy) o 'bare' (el campo guarda el valor sin namespace, 'a.b'). anchors_of, tag_tree y las reglas comparan f'{name}:{field}' cuando es 'bare'. Las anchored_by existentes no cambian.
g2 (H2, alcance por modelos): la declaración del store admite 'tag_models: [Modelo, ...]', opcional. Si está, la familia builtin:tag_namespace (namespace no declarado, prefijos anclados, etc.) solo evalúa documentos de esos modelos o de sus descendientes (base_models del índice), y los tags de otros modelos no se chequean. Si no está, todo sigue como hoy. tag_tree y tag_check respetan el mismo alcance. Va a nivel store y no por namespace porque el problema de deskops es un namespace no declarado, que no tiene entrada propia donde decir 'no aplica'.
g3 (H3, decisión revisable del coordinador): tag_folder sigue estricto (ValueError con segmentos vacíos). Lo adapta deskops en 'CC35d resto', prohibiendo esos tags en su patrón de átomo. Este nodo solo documenta la regla en docs/architecture/tags.md.
g4 (tests): (a) un store con CrossroadDoc.path 'a.b' y anchored_by {model: CrossroadDoc, field: path, value: bare}: tag_tree da la raíz y el check no da hallazgos por los prefijos anclados; (b) un store con tag_models [AtomDoc] y tareas con tags 'workspace:x' no declarados: sin hallazgos en las tareas y con hallazgo en un átomo con un namespace no declarado; (c) sin 'value' ni 'tag_models', todo igual que hoy (tests existentes de tags y reglas en verde).

VALIDACIÓN: el worker corre los tests que toca, los de tests/ sobre tags y reglas (grep tag_namespace, anchored_by, tag_tree, tag_check), tests/test_clean_code_rules.py (80 líneas efectivas por archivo, 10 de lógica por función; no se suben límites) y tools/check.sh --fast. Un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml. Los 7 pasos del workflow los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test anchored_by value bare con CrossroadDoc.path a.b: tag_tree con raíz y check sin hallazgos
- Test tag_models [AtomDoc]: tareas con namespaces no declarados sin hallazgos; átomo sí
- Sin value ni tag_models, tests existentes de tags y reglas en verde
- test_clean_code_rules y check.sh --fast
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

g1-g4 hechos con tests verdes; docs/architecture/tags.md y CHANGELOG.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

