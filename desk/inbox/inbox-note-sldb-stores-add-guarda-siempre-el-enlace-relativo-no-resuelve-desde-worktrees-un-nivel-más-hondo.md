---
sldb:
  by: agent
  at: '2026-11-10T21:31:25Z'
  authority: generated
  via: create_document
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: AntonIA
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-10T21:31:24Z'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb stores add guarda siempre el enlace relativo; no resuelve desde worktrees un nivel más hondo

_Describe the incoming message with enough evidence to triage._

sldb stores add guarda siempre el enlace relativo a la raíz del repo que enlaza (sldb/api/stores/link_store.py, record_store_link: rel = os.path.relpath(other, root)), aunque se le pase una ruta absoluta; no hay opción para guardarla absoluta. Con clones base en /srv/repos/<repo> y worktrees en /srv/wt/<repo>/<rama>, un nivel más hondo, el mismo enlace versionado no resuelve en los dos: en shared_llm-gateway (479b415) y manifest (9729506) quedó '../../../mnt/ssd/proyectos/SLDB_1/deskops-runtime/.sldb', que resuelve desde /srv/repos/<repo> y no desde /srv/wt/<repo>/<rama> (daría /srv/mnt/...). Propuesta: aceptar en stores add una ruta absoluta (o con ~ o una variable de entorno) y guardarla tal cual, o resolver el enlace también contra la raíz común del repo (git common dir). Reportado por AntonIA; también está en el inbox de Governance (3f392ab).
