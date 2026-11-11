---
id: task-seguridad-resto-rebuild-track-y-check-store-todav-a-leen-archivos-trackeados-sin-la-guarda-de-ra-z-y-symlinks
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

# SEGURIDAD (resto): rebuild/track y check_store todavía leen archivos trackeados sin la guarda de raíz y symlinks

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-seguridad-resto-rebuild-track-y-check-store-todavía-leen-archivos-trackeados-sin-la-guarda-de-raíz-y.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-seguridad-resto-rebuild-track-y-check-store-todavía-leen-archivos-trackeados-sin-la-guarda-de-raíz-y.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Lo deja fuera de alcance el task.debug de seguridad live_stale (wt/livestale-security 1a6aeed3, runs/subagents/livestale-worker-report.md). Ese arreglo pone la guarda (rutas que resuelven fuera de project_root y symlinks con O_NOFOLLOW, en store/hashing.py) en la lectura del índice de aristas y en stores check para esos casos. Pero rebuild/track y otras partes de check_store (scan_rewrite_loss, structural_noise) siguen leyendo por la ruta trackeada sin esa guarda. Un documento trackeado que es symlink hacia afuera de la raíz se sigue abriendo en esas operaciones. Hecho cuando: toda lectura de un documento trackeado pasa por la misma guarda (un solo punto de apertura), con test de audit hook de 'open' para track, rebuild y stores check sobre un symlink saliente.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
