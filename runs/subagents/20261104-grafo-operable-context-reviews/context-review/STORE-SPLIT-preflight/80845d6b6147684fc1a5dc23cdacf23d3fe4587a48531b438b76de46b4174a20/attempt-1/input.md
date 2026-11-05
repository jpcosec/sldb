FILE:desk/tasks/task-el-store-se-parte-en-sldb-operacional-versionado-y-sldb-cache-regenerable-ignorado.md
---
id: task-el-store-se-parte-en-sldb-operacional-versionado-y-sldb-cache-regenerable-ignorado
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
- src/sldb/store/layout.py
- src/sldb/api/stores/gitignore_policy.py
- src/sldb/cli/commands/stores.py
- src/sldb/store/journal/
- docs/architecture/derived-store-boundary.md
- docs/architecture/journal-authority.md
- CHANGELOG.md
task_type: code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El store se parte en .sldb (operacional, versionado) y .sldb_cache (regenerable, ignorado)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión del dueño (2026-10-29): el pasado del árbol del store se pregunta a git, y eso exige que los shards de core/ estén versionados; hoy con declaración se ignoran core/ y runtime/ (docs/architecture/derived-store-boundary.md) y el journal vive en runtime/. sldb debe separar físicamente lo operacional de la caché y declarar la caché en .gitignore para que sea correcto por construcción.

## Goal

_Describe the concrete result this task must produce._

.sldb/ contiene store.yaml y core/ (store_index, models, documents) y se versiona entero; .sldb_cache/ (hermano de .sldb) contiene lo que hoy es runtime/ (edges, sections, semantic, graphs, cache, locks) y se ignora; el journal desaparece porque su función la cumple git; stores init escribe la línea .sldb_cache/ en .gitignore y stores check alerta si falta o si core/ está ignorado.

## Scope

_State what is in scope and what is out of scope._

src/sldb/store/layout.py (runtime_dir pasa a .sldb_cache/, hermano de .sldb/ en la raiz del repo), src/sldb/api/stores/gitignore_policy.py, stores init/build/check, un comando nuevo stores migrate-layout, src/sldb/store/journal/ (escritor retirado), docs/architecture/derived-store-boundary.md y journal-authority.md reescritos, un atom con la regla, tests. Precisiones: (1) el .gitignore que se edita es el de la raiz del repo que contiene .sldb/ (el mismo donde hoy se ignoran core/ y runtime/); stores init agrega la linea .sldb_cache/ si no esta (idempotente) y nunca borra otras lineas; (2) migrate-layout mueve el CONTENIDO de .sldb/runtime/ a .sldb_cache/ (edges, sections, semantic, graphs, cache, locks), se niega si .sldb_cache/ existe y no esta vacia salvo --force, borra .sldb/runtime/journal/ sin archivarlo (git es la autoridad del pasado, decision del dueno 2026-10-29) y deja .sldb/runtime/ eliminado; retira del camino de escritura el escritor del journal (ninguna escritura vuelve a producir journal) y el comando sldb journal show pasa a imprimir un aviso que remite a sldb docs history; (3) 'declaracion versionada' = store.yaml; migrate-layout reescribe el .gitignore de la raiz: quita las lineas que ignoran .sldb/core/ y .sldb/runtime/ y agrega .sldb_cache/; (4) stores check emite Finding (src/sldb/core/finding.py): error stores/core_ignored si .sldb/core/ o store.yaml estan ignorados por git (exit 1), alert stores/cache_not_ignored si falta la linea .sldb_cache/ (exit 0); (5) los cinco stores de SLDB_1 son deskops/.sldb, sldb/.sldb, spec2viz/.sldb, pron/.sldb y scion/.sldb; la migracion de los cuatro hermanos y los avisos por inbox los hace el supervisor al integrar, no este ejecutor. Coordina con task-congelar-journal-autoridad-arbol: esta tarea implementa su decision; aquella se cierra documentando que el journal fue retirado.

## Implementation Path

_Outline the expected implementation route or affected surface._

Ejecutor con tests, en worktree propio de sldb; el supervisor revisa, corre la suite en robocop2, migra los stores hermanos con stores migrate-layout y cierra. Orden sugerido: layout.py y gitignore_policy.py con tests; stores init/check; migrate-layout con tests sobre un store temporal creado con la version anterior del layout; retiro del escritor del journal y aviso en journal show; docs y atom; CHANGELOG (seccion vigente). Ante un contrato ausente, registrar la hipotesis en este TaskDoc, no inventar API.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests -k 'layout or gitignore or stores or migrate'

## Done When

_Name the observable condition that makes the task complete._

En un repo nuevo, stores init deja .sldb/ versionable y .sldb_cache/ ignorada con la linea en el .gitignore de la raiz; stores build reconstruye .sldb_cache/ desde .sldb/; stores migrate-layout sobre un store con layout viejo deja .sldb/runtime/ eliminado, .sldb_cache/ poblada, sin journal y el .gitignore corregido; stores check emite stores/core_ignored como error y stores/cache_not_ignored como alert en los casos definidos; ninguna escritura produce journal; pytest -q tests -k 'layout or gitignore or stores or migrate or journal' verde y la suite completa verde en robocop2; derived-store-boundary.md y journal-authority.md describen el layout nuevo; CHANGELOG actualizado.

FILE:instruccion
Preflight solo-TaskDoc del nodo STORE-SPLIT: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita y da el DRY-RUN. No ejecutes nada.

