---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-29T00:55:56'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# stores declare --write aplana los globs de include: en paths enumerados

_Describe the incoming message with enough evidence to triage._

sldb stores declare --write reescribe la sección include: del store.yaml convirtiendo cada 'glob: desk/atoms/atom-*.md' en una lista 'paths:' enumerada (93 líneas nuevas en deskops/.sldb/store.yaml). La declaración es autorada: el glob es la intención del dueño y la enumeración es derivada. Esperado: declare --write conserva los globs y solo agrega lo que falta (links, modelos nuevos), o avisa que va a aplanar y pide confirmación. Reproducción: cd deskops && sldb stores add ../sldb/.sldb --name sldb --store .sldb && sldb stores declare --store .sldb --write && git diff .sldb/store.yaml. Contexto: armando el store central de deskops (links a sldb, spec2viz, pron, scion) el 2026-10-29; restauré el archivo y agregué los links a mano.
