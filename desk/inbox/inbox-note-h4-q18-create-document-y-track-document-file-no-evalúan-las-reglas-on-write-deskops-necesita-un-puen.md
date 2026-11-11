---
sldb:
  by: agent
  at: '2026-11-11T15:23:48Z'
  authority: generated
  via: create_document
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-11T18:00:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# H4 (q18): create_document y track_document_file no evalúan las reglas on_write; deskops necesita un puente para el chequeo de padres de dominio

_Describe the incoming message with enough evidence to triage._

Hallado por 'CC35d resto' de deskops (2026-11-11, coordinador 2; decisión B-c). Con GD27 (anchored_by value bare, tag_models), la familia builtin:tag_namespace exige que un tag hierarchical tenga anclados todos sus prefijos; deskops la usa para 'domain:'. Pero sldb.api create_document y track_document_file no evalúan las reglas on_write (gap q18): un átomo con domain:a.b sin crossroad 'a' se crea igual y el hallazgo solo aparece después, en stores check (on_check). Por eso deskops, antes de escribir, lee tag_tree y TagNamespace.required de sldb y rechaza con el mensaje de hoy ('Write the parent first: ...'), marcado en código como puente hasta este arreglo. Esperado: create_document y track_document_file (y docs track del CLI) evalúan las reglas on_write del documento nuevo dentro de la misma transacción y rechazan con el hallazgo, como ya hacen las escrituras de fields update. Test: un store con tag_namespaces domain (anchored_by CrossroadDoc.path value bare) y tag_models [AtomDoc]; create_document de un AtomDoc con domain:a.b sin crossroad 'a' se rechaza con el hallazgo de la familia y no deja el archivo. Cuando entre, deskops borra el puente de CC35d resto.
