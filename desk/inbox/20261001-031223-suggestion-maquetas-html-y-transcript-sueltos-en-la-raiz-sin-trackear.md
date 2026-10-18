---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-01T03:12:23'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T13:12:15'
---

# Maquetas HTML y transcript sueltos en la raiz, sin trackear

_Describe the incoming message with enough evidence to triage._

SLDB_ extracción, grafo y compositor.html, SLDB_ caso Levira, de fuentes a respuesta.html y sldb_surface.md están en la raíz sin trackear. surface/README.md y docs/surface/OPERACIONALIZACION-VISTAS.md los citan por nombre como referencia de diseño; el commit 68e54a5 dice que la maqueta suelta sale de la raíz. Propuesta: moverlos a docs/surface/ y corregir las referencias.

## Resolución

Resuelto (2026-10-18, sldb-04). Las maquetas y el transcript ya no están sueltos en la raíz: viven trackeados en docs/surface/ (mockup-extraccion-grafo-compositor.html, sldb-caso-levira-fuentes-a-respuesta.html, sldb-extraccion-grafo-compositor.html, sldb_surface.md), commit ab6cf2b5.
