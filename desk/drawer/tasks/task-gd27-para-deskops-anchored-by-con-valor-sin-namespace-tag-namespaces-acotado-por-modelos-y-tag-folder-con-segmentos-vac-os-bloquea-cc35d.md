---
id: task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-tag-namespaces-acotado-por-modelos-y-tag-folder-con-segmentos-vac-os-bloquea-cc35d
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

# GD27 para deskops: anchored_by con valor sin namespace, tag_namespaces acotado por modelos y tag_folder con segmentos vacíos (bloquea CC35d)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-gd27-para-deskops-anchored-by-con-valor-sin-namespace-tag-namespaces-acotado-por-modelos-y-tag-folde.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-gd27-para-deskops-anchored-by-con-valor-sin-namespace-tag-namespaces-acotado-por-modelos-y-tag-folde.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallado por CC35d de deskops (wt/cc35d 568d2140, runs/subagents/cc35d-worker-report.md, 2026-11-10). La parte de árbol de dominios y namespaces de CC35d no puede pasar a la API de tags de sldb hasta resolver esto. La parte de replace (sldb.replace_text) sigue adelante sin esperar.

B1/H1. anchored_by de GD27 exige que el campo valga 'domain:a.b', pero CrossroadDoc.path vale 'a.b'. Con crossroad existente, la API igual da 5 hallazgos y tag_tree devuelve roots=[]. Propuesta: anchored_by acepta un campo con el valor del tag sin namespace, sea como opción ({model, field, value: bare}) o como regla (un valor sin colon es el valor del namespace).

B2/H2. Declarar tag_namespaces desde tag-namespaces.yaml de deskops da 115 errores nuevos (workspace 78, pill-type 29, ...), y on_write rechazaría tareas y pills. Hoy un namespace declarado vuelve obligatorio todo namespace en todo modelo. Propuesta: TagNamespace o la declaración acota la familia, con models: [...] por namespace o con undeclared: ignore|error.

H3 (menor). tag_folder difiere de deskops en tags con segmentos vacíos ('a..b', 'a.'): deskops los ignora. Ningún desk usa folder axis. Propuesta: tag_folder ignora los segmentos vacíos, o deskops prohíbe esos tags en ATOM_TAG_PATTERN.

Cuando H1 y H2 estén en sldb main, CC35d (o una continuación) mueve domain_tree, require_domain_parents y tag_namespaces. Eso incluye además doc_access.py, services/atoms.py y cli/commands/atoms.py (B3).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
