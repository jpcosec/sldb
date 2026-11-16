---
sldb:
  by: agent
  at: '2026-11-16T07:47:28Z'
  authority: generated
  via: save_document_payload
id: task-referrers-y-rewrite-references-aceptan-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-duplican-men
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-referrers-y-rewrite-references-para-un-grafo-armado-en-proceso-excluir-fuentes-y-menciones-duplicada.md
depends_on: []
pills:
- desk/contexts/pill-pill-grafo-en-proceso-para-referrers.md
files:
- src/sldb/api/edges/referrers.py
- src/sldb/api/edges/rewrite_references.py
- tests/api/test_referrers.py
- tests/api/test_rewrite_references.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada
---

# referrers y rewrite_references aceptan un grafo armado en proceso, excluyen fuentes y no duplican menciones del frontmatter

## Rationale

_Explain why this task exists or the business driver behind it._

deskops (CC35c) recompone en el módulo references de deskops.services (repo deskops) lo que la API pública no cubre: (H-a) referrers y rewrite_references (src/sldb/api/edges/referrers.py:50, src/sldb/api/edges/rewrite_references.py:37) leen el grafo de store.yaml con optional_graph (referrers.py:86) y deskops arma el suyo en proceso, así que no ven menciones; (H-b) rewrite_references no admite excluir fuentes; (H-c) find_hits (referrers.py:100) devuelve dos veces un campo declarado del frontmatter, como schema y como mention. Origen: desk/inbox/inbox-note-referrers-y-rewrite-references-para-un-grafo-armado-en-proceso-excluir-fuentes-y-menciones-duplicada.md.

## Goal

_Describe the concrete result this task must produce._

referrers(store, target, graph=g) y rewrite_references(..., graph=g, excluded_sources=[...]) usan g en lugar de optional_graph cuando se pasa, no tocan las fuentes excluidas, y find_hits no devuelve como mention una línea del frontmatter que ya es un hit schema del mismo documento.

## Scope

_State what is in scope and what is out of scope._

Entra: parámetro keyword-only graph: ProjectGraph | None = None en referrers y rewrite_references (si es None se usa optional_graph como hoy); parámetro keyword-only excluded_sources: Iterable[str] = () en rewrite_references, con fuentes nombradas por ruta trackeada o export id Model:name, que se saltan tanto en campos como en menciones; en find_hits, descartar las mentions cuya ruta es la de un documento con un hit schema y cuya línea cae dentro del frontmatter de ese documento. Tests en tests/api/test_referrers.py (H-a con el desk mínimo de la nota armado en tmp_path: sin graph devuelve [], con graph devuelve la mención; H-c: un campo declarado aparece una sola vez como schema) y tests/api/test_rewrite_references.py (H-b: una fuente excluida queda byte a byte igual). CHANGELOG.md. No entra: declarar project_graph en el store.yaml de deskops (es de deskops), cambiar el formato de Referrer, ni tocar deskops (al cerrar se le avisa con deskops message send --to deskops).

Precisiones (preflight-1): ProjectGraph se importa de sldb.api.edges.project_graph.project_graph. Cada excluded_source se resuelve con resolve_target (el mismo que usa referrers para el target) a un documento trackeado; se compara por ruta trackeada relativa al proyecto, así que "Model:name" y la ruta del mismo documento excluyen lo mismo; una fuente que no resuelve lanza SLDBDocumentTargetError. El frontmatter de un documento es el bloque entre la primera línea "---" (línea 1) y la siguiente línea "---", ambas incluidas, numerando líneas desde 1 como ya hace LineMentions.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer referrers.py completo (referrers, optional_graph, find_hits) y rewrite_references.py (rewrite_references, _write, _planned_text). 2) Agregar graph y pasarlo a find_hits. 3) Agregar excluded_sources y filtrar en la planificación de campos y de menciones. 4) Dedupe de H-c en find_hits. 5) Tests y CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_referrers.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rewrite_references.py

## Done When

_Name the observable condition that makes the task complete._

Los dos archivos pasan con los tres casos nuevos; sin graph ni excluded_sources el comportamiento es el de hoy (los tests existentes siguen verdes); CHANGELOG, commit y aviso a deskops.
