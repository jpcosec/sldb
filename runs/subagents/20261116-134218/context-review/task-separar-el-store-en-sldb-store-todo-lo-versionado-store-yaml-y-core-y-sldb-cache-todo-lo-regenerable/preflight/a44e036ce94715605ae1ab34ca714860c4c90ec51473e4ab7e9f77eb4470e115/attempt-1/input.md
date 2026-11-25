FILE:desk/tasks/task-separar-el-store-en-sldb-store-todo-lo-versionado-store-yaml-y-core-y-sldb-cache-todo-lo-regenerable.md
---
sldb:
  by: agent
  at: '2026-11-16T13:41:48Z'
  authority: generated
  via: save_document_payload
id: task-separar-el-store-en-sldb-store-todo-lo-versionado-store-yaml-y-core-y-sldb-cache-todo-lo-regenerable
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on:
- task-merge-de-dos-sldb-sin-detenerse-merge-driver-de-sldb-un-comando-que-regenera-los-índices-derivados-y
pills: []
files:
- src/sldb/store/layout.py
- src/sldb/store/migration.py
- src/sldb/api/stores/init_store.py
- src/sldb/api/stores/store_declaration.py
- tests/store/test_legacy_layout_migration.py
- docs/architecture/derived-store-boundary.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
---

# Separar el store en .sldb_store (todo lo versionado: store.yaml y core/) y .sldb_cache (todo lo regenerable), con stores migrate-layout, lectura del layout viejo y migración del ecosistema

## Rationale

_Explain why this task exists or the business driver behind it._

Tarea nueva de JP (2026-11-16, vía supervisor): que sea obvio qué se trackea y qué se regenera. Hoy el store versionado vive en .sldb/ (store.yaml, core/ y README.md; .sldb/.config/ está en .gitignore pero nadie lo usa) y lo regenerable ya vive aparte en .sldb_cache/ (composed, edges, rules, sections, semantic, locks; ignorado). El nombre .sldb no dice que es lo versionado, y el literal ".sldb" está repartido en unos 35 archivos de src/sldb (por ejemplo src/sldb/api/stores/init_store.py:33, src/sldb/api/stores/store_declaration.py:86-108, src/sldb/api/edges/project_graph/project_store.py:32). El atom atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past ya fija la regla; esta tarea la hace visible en el nombre.

## Goal

_Describe the concrete result this task must produce._

Un store nuevo se crea en .sldb_store/ (store.yaml, core/ y README.md, todo versionado) con su cache en .sldb_cache/ (todo regenerable e ignorado); `sldb stores migrate-layout` lleva un store del layout viejo al nuevo con git mv; todo comando de sldb sigue leyendo un store en .sldb/ (layout viejo) con una alerta que dice que se migre; el store de sldb está migrado; y cada repo del ecosistema que tiene store recibió por inbox el aviso con el comando.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) una constante única STORE_DIR_NAME = ".sldb_store" y LEGACY_STORE_DIR_NAME = ".sldb" en src/sldb/store/layout.py (junto a CACHE_DIR_NAME), y reemplazar cada literal ".sldb" de src/sldb que nombra el directorio del store por esas constantes (inventario con `grep -rn '"\.sldb"' src/sldb`; un literal que forma parte de ".sldb_cache" no cuenta). (2) Descubrimiento y resolución (store_discovery, store_declaration, init_store, links de store.yaml): preferir .sldb_store; si solo existe .sldb, usarlo y emitir la alerta store/legacy-layout "this store uses the old .sldb/ layout: run `sldb stores migrate-layout`"; un enlace de store.yaml que nombra ../repo/.sldb resuelve también a ../repo/.sldb_store si el primero no existe. (3) `sldb stores migrate-layout` (el subcomando ya existe en src/sldb/cli/parsers/stores.py; hoy mueve el runtime a .sldb_cache): además, con el repo en git, `git mv .sldb .sldb_store` (sin git, rename), quita .sldb/.config si está vacío, actualiza .gitignore (.sldb_store/ versionado, .sldb_cache/ ignorado, sin la línea .sldb/.config/) y las rutas .sldb/ de .gitattributes si existen; es idempotente y no toca un store que ya está migrado. (4) `sldb stores init` crea .sldb_store/. (5) Migrar el store de este repo con el comando y commitear el resultado en el mismo commit; correr stores check y stores build --check (bajo flock /dev/shm/sldb1-tests.lock). (6) Documentación: .sldb_store/README.md y docs/architecture/derived-store-boundary.md explican qué va en cada carpeta; CHANGELOG.md marca el cambio de layout. (7) Avisos: deskops message send a deskops, IR, pron, graph_ui, spec2viz, scion y mepu (los que tengan store) con el comando de migración y la fecha desde la cual el layout viejo solo se lee con alerta; para un repo que no esté en el registro, el aviso va como línea "Aviso a <repo>" en result-summary.md. (8) Tests en tests/store/test_legacy_layout_migration.py: un store viejo en .sldb se lee con la alerta; migrate-layout lo deja en .sldb_store con el mismo contenido versionado (mismo store_hash) y es idempotente; init crea .sldb_store; un enlace a ../otro/.sldb resuelve a .sldb_store migrado. No entra: migrar los stores de otros repos (cada coordinador lo hace con el comando al recibir el aviso); quitar la lectura del layout viejo (otra tarea, cuando todos migren); cambiar el formato de los archivos.

Precisiones (preflight-1): si en un proyecto existen a la vez .sldb/ y .sldb_store/, todo comando que descubre el store lanza SLDBStoreError con code store/ambiguous-layout y el texto "both .sldb/ and .sldb_store/ exist in <proyecto>: keep one (run `sldb stores migrate-layout` on a project that only has .sldb/)", y migrate-layout se niega con el mismo error sin tocar nada. Si .sldb/.config/ existe y no está vacío, migrate-layout lo deja dentro de .sldb_store/.config/ (sigue ignorado en .gitignore como .sldb_store/.config/) y emite una alerta que lo nombra. .gitattributes: solo se reescriben las líneas cuyo patrón empieza por .sldb/ (por ejemplo las que agrega `sldb stores merge-driver --install`), cambiando el prefijo por .sldb_store/; si no hay .gitattributes o no tiene esas líneas, no se crea ni se toca. El grep de Done When busca el literal entre comillas dobles ".sldb" (con la comilla de cierre), que no casa con ".sldb_cache".

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/layout.py, src/sldb/store/migration.py, el comando de migrate-layout (grep "migrate-layout" src/sldb/cli), src/sldb/api/stores/init_store.py, src/sldb/api/stores/store_discovery.py y store_declaration.py. 2) Inventario de literales y reemplazo por constantes. 3) Descubrimiento con fallback y alerta. 4) migrate-layout. 5) Tests. 6) Migrar este repo, stores check y build --check. 7) Docs y CHANGELOG. 8) Avisos. Ejecutar después de la tarea del merge driver (depends_on), porque esa escribe rutas .sldb/ en .gitattributes que esta migra.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_legacy_layout_migration.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_stores_build.py
- flock /dev/shm/sldb1-tests.lock env TMPDIR=/dev/shm uv run --frozen --extra code --extra dev sldb stores build --check --store .sldb_store

## Done When

_Name the observable condition that makes the task complete._

Los cuatro comandos de Validation pasan; `grep -rn '"\.sldb"' src/sldb` solo deja la constante LEGACY_STORE_DIR_NAME; el repo de sldb tiene .sldb_store/ versionado y .sldb_cache/ ignorado, sin .sldb/; los avisos a los consumidores están enviados o anotados; README y doc explican el layout; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-separar-el-store-en-sldb-store-todo-lo-versionado-store-yaml-y-core-y-sldb-cache-todo-lo-regenerable: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

