---
sldb:
  by: agent
  at: '2026-11-17T02:00:57Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T05:48:45'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T23:00:11'
---

# declared_target_nodes: aceptar un directorio como target declarado

_Describe the incoming message with enough evidence to triage._

Caso: en deskops, una MaterializationContractDoc con target_identity igual a un directorio (p. ej. pkg/sub, o en sldb src/sldb/notations) no se convierte en nodo del grafo: src/sldb/api/edges/project_graph/declared_target_nodes.py (~l.52) exige is_file(), asi que el target queda como missing_declared_target y la materialization se considera invalida. En el cierre SV01-SV04 de sldb (2026-11-06) eso obligo a crear 62 materializations para 66 archivos.

Salida de deskops graph missing en un desk sandbox (materialization-pkg-sub, target_identity pkg/sub, directorio existente con pkg/sub/a.py):

Missing graph references:
- missing_declared_target: materialization:materialization-pkg-sub -> pkg/sub
  provenance: desk/materializations/materialization-pkg-sub.md:frontmatter
  reason: declared target was not found among extracted graph nodes
1 missing, 0 informational
(rc=1)

Pedido: que declared_target_nodes acepte un directorio como target declarado (nodo de directorio o equivalente), para que graph missing no lo reporte. Del lado deskops, la tarea task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc ya hace que closeout cubra los archivos bajo el directorio por prefijo de ruta (target_covers en deskops/services/closure.py) sin esperar esta respuesta.
