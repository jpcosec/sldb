---
sldb:
  by: agent
  at: '2026-11-21T04:17:05Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-21T01:10:13'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T01:16:42'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en tarea de sldb: el merge driver se instala solo cuando .gitattributes
  lo pide y falta la config.'
---

# El merge driver no quedó instalado en el clon principal de sldb pese al auto-install

_Describe the incoming message with enough evidence to triage._

2026-11-21: al mergear origin/main (enlaces #3) en /mnt/ssd/proyectos/SLDB_1/sldb, .gitattributes tenía las líneas merge=sldb pero .git/config no tenía merge.sldb.driver, así que git dejó en conflicto store.yaml, store_index.yaml y models/InboxNoteDoc.yaml como texto. 'sldb stores merge-driver --install' dijo '0 .gitattributes lines added, 2 git config keys set' y con eso el merge rehecho resolvió el store solo. El auto-install de 9007f78a/5900a3eb no se disparó en este clon. Pedido: que se instale cuando falte, en cualquier comando de sldb que toque el store, o que stores check avise si .gitattributes lo pide y la config no lo tiene.
