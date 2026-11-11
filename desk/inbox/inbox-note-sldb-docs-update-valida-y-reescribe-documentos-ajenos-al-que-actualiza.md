---
sldb:
  by: agent
  at: '2026-11-11T00:59:13Z'
  authority: generated
  via: create_document
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: AntonIA
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-11T00:59:12Z'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb docs update valida y reescribe documentos ajenos al que actualiza

_Describe the incoming message with enough evidence to triage._

En el kit Chatbot_Infra (enlazado al checkout viejo de deskops, cuyo ReviewDoc no conoce kind evidence), 'sldb docs update borrado-de-una-persona' falló con 'Unexpected: 2 validation errors for ReviewDoc' (id fuera del patrón, kind evidence fuera del Literal) sobre recibos que no eran el documento que se actualizaba. Además dejó modificados 5 ReviewDoc .yaml ajenos y les quitó el tag workspace:desk. Esperado: un update de un documento valida y reescribe solo ese documento (y su índice); los otros documentos inválidos se reportan como alerta, sin abortar el update y sin reescribirse. Reportado por AntonIA el 2026-11-10; el desencadenante (enlace viejo) se corrigió con relink a deskops-runtime.
