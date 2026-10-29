---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-18T12:36:00'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-29T10:05:23'
---

# Release 0.1.13 pendiente hasta que la suite completa esté verde

_Describe the incoming message with enough evidence to triage._

Regla del dueño (2026-10-18): no hay deploys (ni tags de versión, ni releases, ni publicación
a PyPI) hasta que sldb, deskops, spec2viz y graph_ui estén listos, testeados y funcionando juntos.

Estado al 2026-10-18: pyproject.toml ya dice 0.1.13 (a0b86941) y el CHANGELOG lo acumula bajo
`## 0.1.13 — not released yet (no tag, not on PyPI)`, con 33 entradas, todas en main. Entre ellas:
aristas que siguen al contrato (b42a18b), `stores remove`/`stores add --replace` (691f1ae),
ítems de lista que se leen tal como se escribieron (69847fc), la caché por documento de stores
check (65fe325d86) y los últimos nombres kgdb pasados a nombres de sldb (52553cde).

Cuando la suite completa esté verde: fechar el encabezado 0.1.13 del CHANGELOG, tag `v0.1.13`
(dispara publish.yml) y avisar a deskops, graph-ui y spec2viz. No hay que volver a subir la
versión en pyproject.
