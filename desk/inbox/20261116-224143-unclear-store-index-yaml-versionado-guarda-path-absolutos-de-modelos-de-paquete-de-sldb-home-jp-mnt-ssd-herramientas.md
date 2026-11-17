---
sldb:
  by: agent
  at: '2026-11-17T02:18:56Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: pron-repair
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T22:41:43'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T23:18:28'
---

# store_index.yaml versionado guarda path absolutos de modelos de paquete de sldb (/home/jp/..., /mnt/ssd/herramientas/...)

_Describe the incoming message with enough evidence to triage._

Visto en pron master 39ea972 (store versionado, opción A). .sldb/core/store_index.yaml guarda 'path:' absolutos para los modelos que vienen de paquetes de sldb, con rutas de dos máquinas distintas: RelationTypeDoc -> /home/jp/proyectos/SLDB_1/sldb/src/sldb/models/relation_type_doc.py (línea 7) y RuleDoc -> /mnt/ssd/herramientas/sldb/src/sldb/models/rule_doc.py. En store.yaml esos modelos solo declaran model_ref. Como pron versiona .sldb/core, un clon en otra máquina o en el CI hereda rutas que no existen. sldb/.sldb/core/store_index.yaml tiene lo mismo (línea 409, rule_doc). Pregunta: ¿ese path es solo informativo (se importa por model_ref) o se lee? Si se lee, ¿sldb puede dejarlo relativo u omitirlo para los modelos de paquete? No lo toca la tarea de pron del enlace a deskops (task-pron-sldb-enlaza-deskops-como-repo-hermano-…), que cambia solo el link.
