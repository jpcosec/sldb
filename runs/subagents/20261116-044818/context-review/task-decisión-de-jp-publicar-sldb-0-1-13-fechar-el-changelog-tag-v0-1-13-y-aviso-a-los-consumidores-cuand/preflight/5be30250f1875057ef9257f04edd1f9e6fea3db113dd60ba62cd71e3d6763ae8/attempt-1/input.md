FILE:desk/tasks/task-decisión-de-jp-publicar-sldb-0-1-13-fechar-el-changelog-tag-v0-1-13-y-aviso-a-los-consumidores-cuand.md
---
sldb:
  by: agent
  at: '2026-11-16T04:11:34Z'
  authority: generated
  via: create_document
id: task-decisión-de-jp-publicar-sldb-0-1-13-fechar-el-changelog-tag-v0-1-13-y-aviso-a-los-consumidores-cuand
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261018-123600-suggestion-release-0-1-13-pendiente-hasta-que-la-suite-completa-este-verde.md
depends_on:
- task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024
pills: []
files:
- CHANGELOG.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Decisión de JP: publicar sldb 0.1.13 (fechar el CHANGELOG, tag v0.1.13 y aviso a los consumidores) cuando la suite conjunta esté verde

## Rationale

_Explain why this task exists or the business driver behind it._

Regla del dueño (2026-10-18): no hay deploys (tags, releases ni PyPI) hasta que sldb, deskops, spec2viz y graph_ui estén listos, testeados y funcionando juntos. pyproject.toml ya dice 0.1.13 y CHANGELOG.md:5 acumula "## 0.1.13 — not released yet"; no existe el tag v0.1.13 (los últimos son v0.1.7 a v0.1.9). El tag dispara publish.yml (PyPI), que es irreversible y externo. Precondición: la tarea task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024. Origen: desk/inbox/20261018-123600-suggestion-release-0-1-13-pendiente-hasta-que-la-suite-completa-este-verde.md.

## Goal

_Describe the concrete result this task must produce._

JP decide si se publica 0.1.13 y cuándo; si dice que sí, el encabezado 0.1.13 de CHANGELOG.md queda fechado, el tag v0.1.13 está en origin y deskops, graph_ui y spec2viz recibieron el aviso; si dice que no o "más adelante", la decisión y su condición quedan escritas en CHANGELOG.md bajo el encabezado 0.1.13 como línea "Release: <decisión de JP, fecha>".

## Scope

_State what is in scope and what is out of scope._

Entra: comprobar que el último run de CI de main está verde (gh run list --repo jpcosec/sldb --branch main --limit 1) y que la tarea de main en verde está cerrada; presentar a JP el estado (CI, suite de deskops, spec2viz y graph_ui) y pedir la decisión; registrar el recibo owner (deskops review record --kind owner; el dispose accepted es de JP); si aprueba: fechar el encabezado en CHANGELOG.md, commit, git tag v0.1.13 sobre ese commit y push del tag por el coordinador integrador, y deskops message send --to deskops, --to graph_ui y --to spec2viz con el aviso. No entra: subir la versión en pyproject.toml (ya dice 0.1.13), publicar a mano en PyPI, ni decidir por JP.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Esperar a que depends_on esté cerrada. 2) Reunir estado de CI de los cuatro repos. 3) Pedir decisión a JP. 4) Ejecutar según la respuesta. Ningún paso de tag o push se hace sin el recibo owner aceptado por JP.

## Validation

_List the checks required before this task can close._

- gh run list --repo jpcosec/sldb --branch main --limit 1
- grep -n '^## 0.1.13' CHANGELOG.md

## Done When

_Name the observable condition that makes the task complete._

Recibo owner aceptado por JP; CHANGELOG.md refleja la decisión (fecha de release o línea "Release:" con la condición); si se publicó, git ls-remote --tags origin v0.1.13 devuelve el tag y los tres desks tienen el aviso en su inbox.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-decisión-de-jp-publicar-sldb-0-1-13-fechar-el-changelog-tag-v0-1-13-y-aviso-a-los-consumidores-cuand: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

