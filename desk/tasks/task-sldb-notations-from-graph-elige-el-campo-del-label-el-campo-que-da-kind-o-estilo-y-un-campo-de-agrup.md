---
sldb:
  by: agent
  at: '2026-11-16T06:20:19Z'
  authority: generated
  via: create_document
id: task-sldb-notations-from-graph-elige-el-campo-del-label-el-campo-que-da-kind-o-estilo-y-un-campo-de-agrup
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-004723-suggestion-sldb-notations-from-graph-elegir-campo-para-label-kind-estilo-y-agrupaci-n-heredado-de-spec2viz.md
depends_on: []
pills: []
files:
- src/sldb/cli/commands/notations_from_graph.py
- src/sldb/cli/parsers/notations.py
- tests/notations/test_notations_from_graph_cli.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb notations from-graph elige el campo del label, el campo que da kind o estilo y un campo de agrupación

## Rationale

_Explain why this task exists or the business driver behind it._

spec2viz diagram from-graph pasó a sldb notations from-graph --store/--snapshot (src/sldb/cli/commands/notations_from_graph.py) y conserva la limitación: el label del nodo es el id del documento (repo-chatbot-infra) y el kind es el modelo (RepositoryDoc), así que no se pueden colorear los repos por sistema o estado sin editar el spec generado. Lo pidió Governance (DAG de repos, 2026-10-21). Origen: desk/inbox/20261116-004723-suggestion-sldb-notations-from-graph-elegir-campo-para-label-kind-estilo-y-agrupaci-n-heredado-de-spec2viz.md.

## Goal

_Describe the concrete result this task must produce._

from-graph acepta --label-field <campo>, --kind-field <campo|tag:<namespace>> y --group-field <campo|tag:<namespace>>; con ellos, el label del nodo es el valor de ese campo del payload (o el id si falta), el kind es el valor del campo o del tag con ese namespace (o el modelo si falta), y los nodos con el mismo valor de agrupación quedan dentro de un nodo contenedor con aristas contains.

## Scope

_State what is in scope and what is out of scope._

Entra: los tres flags en el parser de from-graph (src/sldb/cli/parsers/notations.py, _add_from_graph y _from_graph_filters) y su aplicación en notations_from_graph.py y en la función de API que compila el grafo a spec (localizarla desde notations_from_graph.py). Un tag se lee de la lista tags del payload: "tag:system" toma el primer tag que empieza por "system:" y usa lo que sigue. Tests en tests/notations/test_notations_from_graph_cli.py: un store en tmp_path con dos RepositoryDoc-like (title y tags system:a / system:b); con --label-field title --kind-field tag:system los nodos tienen label = title y kind a/b; con --group-field tag:system hay dos contenedores con aristas contains. Sin flags, la salida es idéntica a hoy (golden del test existente). CHANGELOG.md. No entra: estilos o paletas nuevas; el --snapshot sin payload solo usa el id y el modelo (se documenta en el --help).

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer notations_from_graph.py, el parser y tests/notations/test_notations_from_graph_cli.py. 2) Agregar flags. 3) Aplicarlos al construir nodos. 4) Tests. 5) CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_notations_from_graph_cli.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_graph.py

## Done When

_Name the observable condition that makes the task complete._

Los dos comandos pasan con los tests nuevos; sin flags la salida no cambia; CHANGELOG y commit.
