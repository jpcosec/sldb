---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-27T14:45:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# El error de builtin:tag_namespace debería nombrar deskops atoms add-namespace

_Describe the incoming message with enough evidence to triage._

Viene de mepu (27-11): ante SLDBRuleViolationError rules/builtin:tag_namespace:<ns> «namespace declared», el mensaje lista los espacios declarados pero no dice cómo declarar uno. Se terminó editando tag_namespaces de .sldb/store.yaml a mano, y deskops desk update lo borró al regenerar desde desk/atoms/tag-namespaces.yaml. Sugerencia: que el mensaje diga «declararlo con deskops atoms add-namespace <ns>» y que store.yaml marque tag_namespaces como derivado.
