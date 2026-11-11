---
id: task-seguridad-live-stale-lee-todos-los-archivos-trackeados-y-sigue-symlinks-fuera-de-la-ra-z-al-cargar-el-ndice-de-aristas
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
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

# SEGURIDAD: live_stale lee todos los archivos trackeados y sigue symlinks fuera de la raíz al cargar el índice de aristas

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-seguridad-live-stale-lee-todos-los-archivos-trackeados-y-sigue-symlinks-fuera-de-la-raíz-al-cargar-e.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-seguridad-live-stale-lee-todos-los-archivos-trackeados-y-sigue-symlinks-fuera-de-la-raíz-al-cargar-e.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallado por la integración de graph_ui (wt/deskops-ui, test_mindmap_workspace_reader), 2026-11-11, sldb 84eb7f75, introducido por GO04 d7eefdeb. live_stale._file_hash abre y hashea CADA archivo trackeado del store en cuanto un proceso nuevo llama load_edge_index; en el desk de prueba abrió las 28 md. Lee archivos que el consumidor tiene marcados como protegidos y sigue un symlink que escapa de la raíz (secreto-externo.md) antes de que el consumidor pueda aplicar sus guardas. Rompe la garantía de graph_ui de 'no abrir lo no autorizado', y graph_ui no lo puede evitar sin dejar de usar load_edge_index. Esperado: live_stale no sigue symlinks ni lee rutas que resuelvan fuera de la raíz del store (comprobar con resolve + is_relative_to antes de abrir); mejor aún, el chequeo de frescura usa stat (mtime/size) y solo hashea cuando cambió, o es perezoso por documento. Hasta el arreglo, test_mindmap_workspace_reader de graph_ui queda rojo con esta causa (sin skip ni xfail).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
