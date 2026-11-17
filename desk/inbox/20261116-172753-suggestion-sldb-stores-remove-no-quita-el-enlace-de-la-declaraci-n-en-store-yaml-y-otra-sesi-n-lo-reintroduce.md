---
sldb:
  by: agent
  at: '2026-11-17T02:04:15Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T17:27:53'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T23:03:40'
---

# sldb stores remove no quita el enlace de la declaración en store.yaml y otra sesión lo reintroduce

_Describe the incoming message with enough evidence to triage._

Al quitar el enlace federado a spec2viz del store de deskops (decisión de JP, G5 opción b), sldb stores remove spec2viz --store .sldb editó solo .sldb/core/store_index.yaml y dejó la entrada links: spec2viz -> ../spec2viz/.sldb en .sldb/store.yaml. Al rato otra sesión regeneró el índice desde store.yaml y el enlace reapareció. Lo que dejó los dos coherentes fue sldb stores remove spec2viz seguido de sldb stores declare --store .sldb --write. Propuesta: que stores remove quite también el enlace de la declaración (o que avise y pida declare --write). Evidencia en deskops: runs/subagents/exec-deskops-e-e1719ad4ee0d/remove.txt y result-summary.md.
