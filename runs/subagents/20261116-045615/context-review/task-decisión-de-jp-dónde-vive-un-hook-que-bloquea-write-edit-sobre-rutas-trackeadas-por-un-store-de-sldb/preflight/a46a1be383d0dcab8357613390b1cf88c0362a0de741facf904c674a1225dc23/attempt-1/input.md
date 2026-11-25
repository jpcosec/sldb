FILE:desk/tasks/task-decisión-de-jp-dónde-vive-un-hook-que-bloquea-write-edit-sobre-rutas-trackeadas-por-un-store-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-16T04:15:48Z'
  authority: generated
  via: create_document
id: task-decisión-de-jp-dónde-vive-un-hook-que-bloquea-write-edit-sobre-rutas-trackeadas-por-un-store-de-sldb
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/tasks/task-los-llm-se-saltan-la-api-de-escritura-y-escriben-markdown-directo.md
depends_on: []
pills: []
files:
- docs/user-manual.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Decisión de JP: dónde vive un hook que bloquea Write/Edit sobre rutas trackeadas por un store de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Parte (a) del ítem "los LLM se saltan la API de escritura": un hook PreToolUse sobre Write/Edit que bloquee las rutas trackeadas por el store y diga en el error el comando de sldb que corresponde. No existe en el repo (solo .claude/settings.local.json con permisos). Es configuración del arnés de agentes, que puede vivir en sldb (un comando `sldb guard-path <ruta>` que el hook llama, más un ejemplo de settings) o solo en la configuración personal de JP (~/setup). La parte (c), que la skill se cargue sola, ya está cubierta: la skill use-sldb está instalada para los agentes. La parte (b) es la tarea task-sldb-docs-track-canonical-... Origen: drawer desk/drawer/tasks/task-los-llm-se-saltan-la-api-de-escritura-y-escriben-markdown-directo.md.

## Goal

_Describe the concrete result this task must produce._

JP decide (a) sldb ofrece `sldb guard-path` y un ejemplo de hook documentado, y se crea su tarea de código; (b) el hook vive solo en ~/setup y sldb no cambia; o (c) no se hace. La decisión queda en docs/user-manual.md, sección "Escritura por agentes", con fecha.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar las opciones; recomendación del coordinador: (a), porque la consulta "¿esta ruta está trackeada y por qué modelo?" es de sldb y el hook queda trivial en cualquier arnés. Registrar el recibo owner (dispose accepted de JP), escribir la sección y crear la tarea si es (a). No entra: implementar el hook ni el comando.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer el ítem del drawer y docs/user-manual.md. 2) Pedir decisión. 3) Escribir la sección. 4) Crear la tarea si corresponde.

## Validation

_List the checks required before this task can close._

- grep -n 'Escritura por agentes' docs/user-manual.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción y la fecha; recibo owner aceptado por JP; tarea creada si es (a); commit del doc.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-decisión-de-jp-dónde-vive-un-hook-que-bloquea-write-edit-sobre-rutas-trackeadas-por-un-store-de-sldb: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

