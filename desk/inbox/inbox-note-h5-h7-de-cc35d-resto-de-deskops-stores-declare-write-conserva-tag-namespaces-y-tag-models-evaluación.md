---
sldb:
  by: agent
  at: '2026-11-11T18:02:19Z'
  authority: generated
  via: create_document
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-11T18:02:17'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# H5-H7 de CC35d resto de deskops: stores declare --write conserva tag_namespaces y tag_models, evaluación estructurada de la familia de tags, y la familia solo ve documentos indexados

_Describe the incoming message with enough evidence to triage._

Hipótesis del worker de CC35d resto de deskops (rama wt/cc35d-resto-r, informe cc35d-resto-worker-report.md en deskops). H4 (on_write en create_document y track) ya está en el inbox (83e097a2).
H5: declare_store (sldb stores declare --write) conserve tag_namespaces y tag_models de la declaración. Hoy _kept solo guarda generate y derived: regenerar store.yaml borra la declaración de tags, y hasta el próximo desk update --apply la familia builtin:tag_namespace no corre.
H6: una forma pública de leer la evaluación estructurada de la familia de tags (namespace, tags, missing) en lugar de parsear Finding.what con el formato '<clause> (seen: <json>)' de rules §4, que es lo que hace hoy deskops en tag_findings.
H7 (informativa, preexistente): la familia solo ve documentos indexados; un átomo escrito a mano no tiene hallazgos hasta que se trackea y uno editado se evalúa sobre la proyección indexada. Si sldb quisiera evaluar los archivos del glob declarado sin trackear, es su decisión.
