---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-20T02:41:37'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-29T10:05:25'
---

# stores check en verde sobre un store que no se construyó (enlace roto)

_Describe the incoming message with enough evidence to triage._

Desde Governance (sesión governance-00), 2026-10-20. Corrección: la primera versión de esta nota decía que los enlaces entre stores no eran portables; era un error mío. El enlace se guarda relativo a la raíz del proyecto (api/stores/link_store.py:81) y es portable si cada entorno reproduce la posición relativa de los repos. Eso le toca a Governance (su CI), no a sldb.

Lo que sigue en pie es el falso verde: con un enlace declarado cuyo destino no existe (p.ej. el repo copiado a otra profundidad sin el dueño al lado), 'PYTHONPATH=src sldb stores build --store .sldb' falla con 'No store at <ruta>', y después 'sldb stores check --store .sldb' devuelve 'PASS: store integrity — 0 documents in 0 models' (exit 0). En CI eso deja pasar un store que no se construyó. Esperado: check falla si el store declarado no está construido o si un enlace declarado está roto.

Reproducción: clonar Governance, 'deskops init .', 'sldb stores declare --write', copiar el repo a /tmp/a/b/gov, 'rm -rf .sldb/core' y correr build y check.
