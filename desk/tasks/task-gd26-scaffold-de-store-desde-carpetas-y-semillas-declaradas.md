---
id: task-gd26-scaffold-de-store-desde-carpetas-y-semillas-declaradas
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
- src/sldb/api/stores/store_declaration.py
- src/sldb/api/stores/scaffold_store.py
- src/sldb/api/stores/build_store.py
- src/sldb/api/__init__.py
- src/sldb/cli/commands/stores_build.py
- src/sldb/cli/parsers/stores.py
- src/sldb/cli/commands/stores.py
- tests/api/test_scaffold_store.py
- tests/store/test_stores_build.py
- tests/api/test_api_stores.py
- docs/architecture/store-declaration.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD26: Scaffold de store desde carpetas y semillas declaradas

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD26 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG2. Depende de: nada. Gates requeridos: ninguno.

## Goal

_Describe the concrete result this task must produce._

StoreDeclaration gana folders y seeds (modos if_missing y managed; fuentes text, file con pkg: y document con track); sldb.api.scaffold_store(store, *, declaration=None, apply=False, template_root) idempotente con reporte created/rewritten/present/conflicts; sldb.api.build_store ejecuta apply_declaration y luego scaffold_store; CLI sldb stores scaffold [--apply] y stores build con sección scaffold; doc en docs/architecture/store-declaration.md.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/stores/store_declaration.py, scaffold_store.py y build_store.py (nuevos), src/sldb/api/__init__.py, src/sldb/cli/commands/stores_build.py, src/sldb/cli/parsers/stores.py, src/sldb/cli/commands/stores.py, tests, docs/architecture/store-declaration.md, CHANGELOG.md. Fuera: las semillas de deskops (las declara CC36), cambiar la forma de store.yaml existente, nombres del caso deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD26). SCOPE: StoreDeclaration (api/stores/store_declaration.py:20) gana dos claves (GP5): folders (lista de rutas relativas a la raíz) y seeds (lista de Seed = {path, mode: if_missing | managed, y una fuente: text (literal), file (ruta a una plantilla relativa a store.yaml o a un paquete Python como pkg:modulo/ruta) o document {model, name, payload} renderizado con el renderizador del modelo (api/documents/document_render.py:31 render_model_template); track: bool (default true si es document)}). Función sldb.api.scaffold_store(store, *, declaration=None, apply=False) → ScaffoldReport (declaration = un StoreDeclaration parcial con folders y seeds pasado en proceso por el consumidor; si se pasa, se usa en lugar de las claves de store.yaml y no se escribe en store.yaml: así un consumidor declara sus semillas en su paquete sin cambiar el formato de su store; las rutas file: relativas se resuelven contra el directorio que el consumidor indique con template_root) {created, rewritten, present, conflicts}: if_missing nunca sobrescribe (present si existe); managed compara bytes y, si difieren, lo reporta como rewritten (con apply) o como pendiente (sin apply); un document con track se trackea con el modelo y nombre declarados; idempotente: una segunda corrida con apply no cambia nada y todo sale present. Escribe dentro de sldb.api.transaction si GD24 ya cerró; si no, por archivo con rollback_on_error. build_store pasa de cli/commands/stores_build.py:35 a sldb.api.build_store(store, *, apply) y la CLI lo llama; build_store ejecuta apply_declaration (links, models, predicates, includes) y después scaffold_store, en ese orden, en un solo reporte. CLI: sldb stores scaffold [--apply] con envelope; sldb stores build incluye el reporte de scaffold. Doc en docs/architecture/store-declaration.md (sección folders y seeds).

ACCEPTANCE: En un store temporal: una declaración con dos carpetas, una semilla text if_missing, una file managed y una document if_missing con track: sin --apply el reporte lista todo como created pendiente y no escribe nada (hashes iguales); con --apply se crean y el documento queda trackeado con su nombre; una segunda corrida da todo present; editar el archivo managed hace que la siguiente corrida lo reporte rewritten y lo restaure; editar el if_missing no lo toca; una plantilla pkg: de un paquete de prueba se resuelve; la misma declaración pasada como declaration= produce el mismo resultado y store.yaml queda igual (hash); una clave desconocida en seeds falla al cargar nombrando la clave; sldb stores build sin cambios en la declaración produce el mismo reporte de links/models/includes que antes (golden existente) más la sección scaffold vacía; CHANGELOG; doc; nota de cierre a deskops.

OUTPUT_SCOPE: src/sldb/api/stores/store_declaration.py, src/sldb/api/stores/scaffold_store.py, src/sldb/api/stores/build_store.py, src/sldb/api/__init__.py, src/sldb/cli/commands/stores_build.py, src/sldb/cli/parsers/stores*.py, src/sldb/cli/commands/stores*.py, tests/, docs/architecture/store-declaration.md, CHANGELOG.md

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
q1 (GD24): GD24 se promueve a la vez y no hay arista entre ambos; si GD24 no cerró al ejecutar GD26, se escribe por archivo con rollback_on_error (src/sldb/store/io/rollback.py) como dice el scope; no se espera a GD24.
q2 (doc): docs/architecture/store-declaration.md no existe hoy; se crea con la sección folders y seeds.
q3 (base): commit base 6b80df36 de main de sldb.

PRECISIONES DEL PREFLIGHT (review-task-gd26-preflight-1, 2026-11-06):
q4 (firma): scaffold_store(store, *, declaration=None, apply=False, template_root=None) -> ScaffoldReport; template_root=None = el directorio de store.yaml.
q5 (folders): cada carpeta se crea con sus padres (mkdir parents); si ya existe como directorio va a present; si existe como archivo va a conflicts y no se toca; sin apply, las faltantes se reportan en created como pendientes. folders no tiene modo.
q6 (GD24): decide el ejecutor al implementar mirando main: si sldb.api.transaction existe (GD24 cerrado), se usa; si no, rollback_on_error (store/io/rollback.py:11) por archivo. Sin detección en tiempo de ejecución.
q7 (track): un seed document con track se trackea con track_document_file(store, model, path, name) (api/documents/track_document_file.py:20).
q8 (reporte vacío): la sección scaffold de stores build es siempre el objeto {created: [], rewritten: [], present: [], conflicts: []} (listas de rutas relativas); vacía = las cuatro listas vacías.
q9 (pkg:): pkg:modulo/ruta se resuelve con importlib.resources.files("modulo").joinpath("ruta") sobre el paquete importable (instalado o en pythonpath); no se resuelve relativo a nada más.
q10 (clave desconocida): Seed y la parte nueva de StoreDeclaration usan model_config = ConfigDict(extra="forbid"); load_declaration levanta pydantic.ValidationError, cuyo mensaje nombra la clave (loc). Las claves existentes de StoreDeclaration no cambian de comportamiento.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_scaffold_store.py
- TMPDIR=/dev/shm pytest -q tests/store/test_stores_build.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_stores.py
- grep -rniE 'taskdoc|board|ritual|pill|atom|closeout' src/sldb/ sin nombres nuevos contra el commit base 6b80df36 (salida de ambos en esta sección)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- sldb stores scaffold --format json y sldb stores scaffold --apply sobre el store temporal del test; segunda corrida todo present

## Done When

_Name the observable condition that makes the task complete._

En un store temporal: una declaración con dos carpetas, una semilla text if_missing, una file managed y una document if_missing con track: sin --apply el reporte lista todo como created pendiente y no escribe nada (hashes iguales); con --apply se crean y el documento queda trackeado con su nombre; una segunda corrida da todo present; editar el archivo managed hace que la siguiente corrida lo reporte rewritten y lo restaure; editar el if_missing no lo toca; una plantilla pkg: de un paquete de prueba se resuelve; la misma declaración pasada como declaration= produce el mismo resultado y store.yaml queda igual (hash); una clave desconocida en seeds falla al cargar nombrando la clave; sldb stores build sin cambios en la declaración produce el mismo reporte de links/models/includes que antes (golden existente) más la sección scaffold vacía; CHANGELOG; doc; nota de cierre a deskops.
