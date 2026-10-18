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
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Release 0.1.13 pendiente hasta que la suite completa esté verde

_Describe the incoming message with enough evidence to triage._

Regla del dueño (2026-10-18): no hay deploys (ni tags de versión, ni releases, ni publicación
a PyPI) hasta que sldb, deskops, spec2viz y graph_ui estén listos, testeados y funcionando juntos.

Lo que espera en `## Unreleased` del CHANGELOG, todo ya en main:

- 9f07436: `sldb store`/`model`/`doc` vuelven a tener handler (pedido por graph-ui).
- b42a18b: un cambio de contrato reconstruye las aristas de los documentos (pedido por deskops).
- 691f1ae: `unlink_store`, `link_store(..., replace=True)`, `stores remove`, `stores add --replace`
  y la nota de links rotos en `stores check` (pedido por deskops).
- 69847fc: un item escalar de lista se lee de vuelta tal como se escribió (fences, `#`, `>`...),
  encontrado por graph-ui.

Cuando la suite completa esté verde: subir la versión a 0.1.13 en pyproject.toml y en el
CHANGELOG, tag `v0.1.13` (dispara publish.yml) y avisar a deskops, graph-ui y spec2viz.
