---
sldb:
  by: agent
  at: '2026-11-24T02:24:48Z'
  authority: generated
  via: create_document
id: task-decision-para-jp-p4-como-se-invalida-el-indice-del-daemon-con-git-y-con-las-escrituras
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
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Decision para JP P4: como se invalida el indice del daemon con git y con las escrituras

## Rationale

_Explain why this task exists or the business driver behind it._

Un indice residente envejece cuando alguien edita un Markdown fuera de sldb o cambia de rama. Hoy el live stale reescanea stats en cada llamada (~1 s en este repo) y esa parte no mejora con el motor. Plan: desk/drawer/plans/grafo-datalog-daemon (poc/informe.md).

## Goal

_Describe the concrete result this task must produce._

Elegir el mecanismo. Opciones: A) dirty set avisado por las escrituras de sldb mas deteccion externa por HEAD y estado del arbol de git y stat de los archivos rastreados, sin reescanear todo por peticion; B) vigilante de archivos (inotify) en el daemon: reaccion inmediata, pero no cubre bien checkouts masivos ni sistemas de archivos de contenedores; C) revalidar por peticion con el escaneo actual (~1 s): simple y seguro, sin ganancia en stale. Recomendacion: A.

## Scope

_State what is in scope and what is out of scope._

Dentro: invalidacion con git y con las escrituras, interaccion con los hooks actuales. Fuera: forma del daemon (P3).

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer poc/informe.md punto 4; JP responde A, B o C; se actualiza G_INVALIDATION

## Validation

_List the checks required before this task can close._

- JP responde en la tarea; el dag.yaml del plan grafo-datalog-daemon refleja la respuesta

## Done When

_Name the observable condition that makes the task complete._

JP respondio y G_INVALIDATION tiene la respuesta como evidence.
