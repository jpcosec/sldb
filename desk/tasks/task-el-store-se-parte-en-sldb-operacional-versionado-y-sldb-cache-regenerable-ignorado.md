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
files: []
task_type: ''
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

src/sldb/store/layout.py (runtime_dir -> .sldb_cache hermano), api/stores/gitignore_policy.py (core versionado, cache ignorada, declaración versionada), stores init/build/check, un stores migrate-layout que mueva runtime/ a .sldb_cache/ y retire el journal, docs/architecture/derived-store-boundary.md reescrito, atom con la regla, tests. Coordinar con task-congelar-journal-autoridad-arbol (misma decisión). Avisar a deskops, spec2viz, pron y scion por inbox al integrar: sus .gitignore cambian.

## Implementation Path

_Outline the expected implementation route or affected surface._

Agente Scion (deskops-executor) implementa con tests; el supervisor revisa, migra los stores hermanos y cierra.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests -k 'layout or gitignore or stores or migrate'

## Done When

_Name the observable condition that makes the task complete._

En un repo nuevo, stores init deja .sldb/ versionable y .sldb_cache/ ignorada; stores build reconstruye .sldb_cache desde .sldb; stores check pasa en los cinco stores de SLDB_1 tras migrate-layout; git log de .sldb/core/documents muestra el pasado de un documento editado.
