---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-20T10:17:08'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-29T10:05:27'
---

# stores build --check falla con enlaces que suben más de un nivel

_Describe the incoming message with enough evidence to triage._

Desde Governance (sesión governance-00), 2026-10-20. Governance enlaza el store de deskops con path '../../../proyectos/SLDB_1/deskops/.sldb', relativo a su raíz (/home/jp/AntonIA/repos/Governance), y 'sldb stores build' y 'stores check' funcionan. Pero 'PYTHONPATH=src sldb stores build --check --store .sldb' falla: 'Unexpected: [Errno 13] Permission denied: /tmp/sldb-build-check-58osczxg/Governance-desk/../../../proyectos'. La copia aparte reproduce el enlace relativo a su propia raíz, y un enlace que sube más niveles que la profundidad de la copia sale de /tmp. En spec2viz funciona porque su enlace sube uno solo (../deskops). Esperado: build --check resuelve los enlaces del store original (o los copia a una posición equivalente) sin depender de la profundidad. Mientras tanto, el pulse de Governance corre build --check solo en stores sin enlaces y avisa cuando lo omite.
