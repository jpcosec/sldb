---
id: task-gd22-referencias-entrantes-buscar-y-reescribir
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-gd21-grafo-de-proyecto-aristas-declaradas-y-nodos-fuente-desde-el-índice-de-sldb-declarado-por-datos
- task-gd24-transacción-multi-documento-en-sldb-api-y-save-atómico-absorbe-doc-io-doctransaction
pills: []
files:
- src/sldb/api/edges/referrers.py
- src/sldb/api/edges/referrer.py
- src/sldb/api/edges/rewrite_references.py
- src/sldb/api/edges/rewrite_report.py
- src/sldb/api/edges/rewrite_values.py
- src/sldb/api/edges/rewrite_mentions.py
- src/sldb/api/__init__.py
- src/sldb/cli/parsers/edges.py
- src/sldb/cli/commands/edges.py
- src/sldb/cli/commands/edges_rewrite.py
- src/sldb/cli/serve/edges_routes.py
- src/sldb/cli/serve/edges_rewrite_routes.py
- src/sldb/cli/serve/routes.py
- tests/api/test_referrers.py
- tests/api/test_rewrite_references.py
- tests/test_serve.py
- docs/architecture/references.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD22: Referencias entrantes - buscar y reescribir

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD22 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG1. Depende de: ['GD21', 'GD24']. Gates requeridos: G_PROJECT_GRAPH: Grafo de proyecto declarado y servido por sldb (satisfied); G_WRITE_API: Transacción y referencias entrantes en sldb.api (satisfied).

## Goal

_Describe the concrete result this task must produce._

sldb.api.referrers(store, target) devuelve las referencias entrantes (campos escalares, elementos de listas y menciones en superficies no modeladas) desde el índice y el grafo de proyecto de GD21; sldb.api.rewrite_references(store, target, replacement | None, *, transaction=None) las reescribe o quita dentro de una transacción de GD24 (todo o nada) y devuelve un RewriteReport; CLI sldb edges referrers y sldb edges rewrite --to | --remove [--dry-run] con envelope; GET /edges/referrers y POST /edges/rewrite; docs/architecture/references.md.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/edges/ (referrers, rewrite_references y auxiliares nuevos), src/sldb/api/__init__.py, src/sldb/cli/parsers/edges.py, src/sldb/cli/commands/edges*.py, src/sldb/cli/serve/edges_routes.py, edges_rewrite_routes.py (nuevo) y routes.py, tests, docs/architecture/references.md, CHANGELOG.md. Fuera: editar src/sldb/api/documents/payload_save_steps.py; borrar prosa (una mención con replacement None se informa en skipped); el código de deskops que esto reemplaza (lo retira deskops).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD22). SCOPE: Función sldb.api.referrers(store, target) → lista de Referrer {source (export_id o ruta de superficie no modelada), field (nombre del campo, o null para una mención), index (posición en un campo lista, o null), location (ruta:línea para una mención), origin (schema | mention)}, construida con edges_to del índice (api/edges/edge_reading.py:47; el campo sale de metadata.field, store/edge_index/declared_references.py:68) más ProjectGraph.edges_to de GD21 para menciones; target acepta export_id, Model:name, ruta trackeada o id de nodo del grafo de proyecto. Función sldb.api.rewrite_references(store, target, replacement | None, *, transaction=None) → RewriteReport {changed: [{source, field|location, before, after}], skipped: [{source, motivo}]}: para un campo escalar reemplaza el valor (o lo vacía si replacement es None); para un campo lista reemplaza el elemento (o lo quita, sin dejar huecos ni duplicados); para una mención reescribe el texto que el MentionPattern capturó, con límite de palabra, en la línea registrada (replacement None = la mención se deja y se informa en skipped, nunca se borra prosa); conserva la forma del valor original (p. ej. prefijo tipo:id si el campo lo usa); escribe dentro de sldb.api.transaction de GD24 (la suministrada o una propia), así que todo o nada. Valores de campos __doc_anchors__ (si GO07 ya cerró): se reescribe a doc:Model:name sin @sha256 para que sldb lo repinee al guardar; si GO07 no cerró, esos campos no existen y no hay caso. CLI: sldb edges referrers TARGET y sldb edges rewrite TARGET --to NUEVO | --remove [--dry-run], con envelope (dry-run devuelve el RewriteReport sin escribir). sldb serve: GET /edges/referrers?target= y POST /edges/rewrite {target, replacement|null, dry_run}. Doc en docs/architecture/references.md.

ACCEPTANCE: En un store temporal con un documento A referenciado por B (campo escalar), C (campo lista con otros dos valores) y una superficie no modelada D (mención en prosa), referrers(A) devuelve los tres con field/index/location correctos; rewrite_references(A, A2) deja B y C apuntando a A2 (C conserva el orden y los otros valores) y reescribe la mención de D; --remove vacía B, quita el elemento de C y deja D en skipped; un fallo inyectado al escribir C revierte B (todo o nada, por GD24); --dry-run no cambia ningún byte (hash de los archivos antes y después); la operación no recorre el disco con el índice fresco (contado); POST /edges/rewrite y la CLI producen el mismo reporte; CHANGELOG; docs/architecture/references.md; nota de cierre a deskops.

OUTPUT_SCOPE: src/sldb/api/edges/referrers.py, src/sldb/api/edges/rewrite_references.py, src/sldb/api/__init__.py, src/sldb/cli/parsers/edges.py, src/sldb/cli/commands/edges.py, src/sldb/cli/serve/edges_routes.py, src/sldb/cli/serve/routes.py, tests/, docs/architecture/references.md, CHANGELOG.md

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de sldb, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review). Las revisiones en frío las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`; nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de sldb aparte del de grafo-operable (otras áreas: edges, documents, serve, stores). Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor sobre el resultado integrado. Un nodo no cierra con tests rojos ni saltados.
3. Toda capacidad nueva entra con: función pública en `sldb.api` (reexportada en `sldb/api/__init__.py`), comando CLI con envelope JSON, ruta de `sldb serve` cuando el consumidor la necesita, pruebas, entrada en `CHANGELOG.md` y doc en `docs/architecture/`. Nada queda solo en el código.
4. Genericidad: ningún nombre del caso deskops (TaskDoc, Board, ritual, pill, atom, closeout) aparece en `src/sldb/` ni en sus tests, salvo como dato en fixtures. Un grep lo comprueba en la aceptación de cada nodo.
5. Compatibilidad: ninguna salida existente de la CLI ni de `sldb serve` cambia (goldens existentes verdes); lo nuevo es aditivo. Si un nodo necesita cambiar un contrato existente (p. ej. `/save` pasa a ser atómico), lo nombra en su aceptación y en el CHANGELOG.
6. Ante un contrato ausente de un nodo GO no cerrado, el nodo registra la hipótesis en su TaskDoc, implementa la parte que no depende de él y no inventa la API de grafo-operable.
7. Cada nodo, al cerrar, manda nota a deskops (`deskops message send --to deskops --kind suggestion`) con la función, el comando y la ruta nuevos y el código de deskops que quedan sin motivo (tabla de arriba); así se satisface el gate `G_GDxx` del plan de deskops.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-06):
q1 (gates): G_PROJECT_GRAPH (ad679a8d) y G_WRITE_API (fe36893f) están satisfied; GD21 y GD24 cerrados: ProjectGraph.edges_to (src/sldb/api/edges/project_graph/project_graph.py:60) y sldb.api.transaction existen en main.
q2 (GO07): GO07 está cerrado (anclas a documentos con hash de contrato): los campos __doc_anchors__ existen; su valor se reescribe a doc:Model:name sin @sha256 para que sldb lo repinee al guardar (caso cubierto por un test).
q3 (GO08 y on_write): la reescritura de un documento trackeado pasa por transaction.update (save_document_payload), así que las reglas on_write de GO08 y la familia de GD27 se evalúan; un rechazo revierte el lote entero.
q4 (files): la lista es la mejor previsión al promover; un archivo autorizado que no se use se reporta en la entrega y el coordinador lo poda del TaskDoc; uno nuevo se pide antes.
PRECISIONES DEL PREFLIGHT (review-task-gd22-preflight-1, 2026-11-06):
q5 (menciones): una mención es lo que captura un MentionPattern de la configuración project_graph del store (GD21: src/sldb/api/edges/project_graph/mention_pattern.py, LineMentions y SectionMentions); el fixture declara su propio patrón (p. ej. un regex de identificadores tipo card:card-a). rewrite_references reescribe solo el texto capturado, en la línea que registró la arista (location ruta:línea), respetando límite de palabra; si en esa línea el texto ya no está, la mención va a skipped con motivo.
q6 (resolución de target): primero como documento trackeado con la misma regla que doc_status (name, Model/name, Model:name o ruta trackeada; ambiguo = error con candidatos); si no resuelve, como id de nodo del grafo de proyecto (kind:identity); si tampoco, SLDBDocumentTargetError. El export_id de un documento es Model:name.
q7 (--remove en un campo escalar): el valor pasa a null (None) y se guarda por transaction.update; si el modelo no admite null en ese campo, la validación del modelo lo rechaza y no se escribe nada del lote (error con el campo). En un campo lista se quita el elemento (sin huecos ni duplicados).
q8 (sin recorrer disco): el test hace una primera llamada para calentar el memo de GD21 y después cuenta con monkeypatch os.walk, os.scandir y Path.rglob durante referrers y rewrite_references --dry-run: deben ser cero.
q9 (fallo inyectado): el test hace fallar la escritura de C dentro de la transacción (monkeypatch del update de la transacción para el ref de C, o un model_validator del modelo de C que rechaza el valor nuevo) y comprueba que B queda con sus bytes, su entrada y su índice originales (hash).
q10 (HTTP igual a la CLI): como en GD21 y GD23, el cuerpo de POST /edges/rewrite y GET /edges/referrers es el mismo JSON que la CLI con --format json (igualdad de datos, sin envelope); parámetros faltantes o inválidos son 400.
q11 (--to y --remove): son mutuamente excluyentes y uno es obligatorio (sin ninguno o con los dos, error de uso, exit 2). En POST /edges/rewrite, replacement es obligatorio en el cuerpo: null = quitar; ausente = 400.
PRECISIONES DEL COLD-BUNDLE (review-task-gd22-bundle-1, 2026-11-06):
q12 (files manda): files: es la lista autorizada; OUTPUT_SCOPE es el resumen del nodo en el dag. Los auxiliares de files (referrer.py, rewrite_report.py, rewrite_values.py, rewrite_mentions.py, edges_rewrite.py, edges_rewrite_routes.py) están autorizados por la regla de clean code (q4).
q13 (salidas): como en los demás nodos del plan, la CLI con --format json emite el objeto de datos (lista de Referrer o RewriteReport) y con --envelope lo envuelve en el envelope habitual (data); el cuerpo HTTP 200 es el mismo objeto de datos que --format json, sin envelope.
q14 (--dry-run): no escribe nada ni abre escritura: calcula el RewriteReport y valida en memoria cada payload nuevo contra su modelo (render y validación de modelo, sin persistir); un payload que el modelo rechaza va como error del dry-run. Las reglas on_write de GO08 no se evalúan en dry-run (solo al escribir); queda dicho en references.md.
q15 (forma del valor): el valor nuevo conserva la forma en que el original nombraba al target: name -> name del reemplazo; Model:name o Model/name -> la misma forma con el Model y el name del reemplazo; ruta trackeada -> ruta del reemplazo; doc:Model:name@sha256... -> doc:Model:name sin @sha256 (q2). Para eso replacement se resuelve como el target (q6); si no resuelve a un documento (p. ej. un id de nodo del grafo de proyecto), se escribe literal.
q16 (límite de palabra): un token de mención es una secuencia de caracteres [A-Za-z0-9_:./-]; el texto capturado se reemplaza solo si coincide con un token completo (el carácter anterior y el siguiente no son de ese conjunto, o son inicio o fin de línea). Así card:card-a no reescribe card:card-ab.
PRECISIONES DE EJECUCIÓN (coordinador, 2026-11-06):
q17 (q8 afinada, hallazgo del ejecutor): shards_signature (src/sldb/store/edge_index/shard_signature.py:31) hace un os.scandir del directorio de shards de aristas en cada load_edge_index y en cada comprobación del memo de GD21: es una lectura de un directorio de .sldb, no un recorrido del árbol. El test de q8 cuenta os.walk y Path.rglob (cero, como el de GD21) y, para os.scandir, cero llamadas sobre directorios fuera de .sldb (ningún scandir del proyecto); los scandir dentro de .sldb no cuentan. Afinado (ejecutor): los shards de aristas viven en .sldb_cache/edges/, así que el conteo excluye los scandir sobre .sldb y .sldb_cache (directorios cuyo nombre empieza por .sldb); cualquier otro scandir del proyecto cuenta y debe ser cero.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_referrers.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rewrite_references.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/api/test_project_graph.py
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_every_command_has_a_handler.py
- grep de genericidad: ninguna línea agregada por el diff (git diff origin/main...HEAD) en src/ o tests/ contiene taskdoc|board|ritual|pill|atom|closeout (regla 4)
- sldb edges referrers TARGET y sldb edges rewrite TARGET --to NUEVO --dry-run --format json sobre el store temporal del test (salida en el reporte de entrega)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, máximo 1 clase y 80 líneas efectivas por archivo)
- git fetch y rebase sobre origin/main antes de entregar; en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio
- files: del TaskDoc coincide con el diff entregado (los autorizados que no se usen se reportan y el coordinador los poda antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

En un store temporal con un documento A referenciado por B (campo escalar), C (campo lista con otros dos valores) y una superficie no modelada D (mención en prosa), referrers(A) devuelve los tres con field/index/location correctos; rewrite_references(A, A2) deja B y C apuntando a A2 (C conserva el orden y los otros valores) y reescribe la mención de D; --remove vacía B, quita el elemento de C y deja D en skipped; un fallo inyectado al escribir C revierte B (todo o nada, por GD24); --dry-run no cambia ningún byte (hash de los archivos antes y después); la operación no recorre el disco con el índice fresco (contado); POST /edges/rewrite y la CLI producen el mismo reporte; CHANGELOG; docs/architecture/references.md; nota de cierre a deskops.
