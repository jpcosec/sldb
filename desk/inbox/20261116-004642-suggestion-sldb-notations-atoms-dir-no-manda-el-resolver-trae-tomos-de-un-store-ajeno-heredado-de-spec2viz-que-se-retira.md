---
sldb:
  by: agent
  at: '2026-11-16T08:25:01Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T00:46:42'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:24:45'
---

# sldb notations: --atoms-dir no manda; el resolver trae átomos de un store ajeno (heredado de spec2viz, que se retira)

_Describe the incoming message with enough evidence to triage._

Origen: drawer de spec2viz, task-catalog-build-trae-atoms-de-un-store-ajeno-aunque-se-pase-atoms-dir (inbox de labchile, 2026-10-22). spec2viz se retira (IR/docs/spec2viz/acta-de-retiro.md) y la lógica pasó a sldb sin cambios: sldb/src/sldb/api/matching/atoms_by_view.py:19-29 (raw_atoms_by_view) toma primero reader.atoms(view.store) de cada vista y solo usa atoms_dir como respaldo para las vistas que quedaron vacías; specir catalog build la llama desde IR/src/specir/visual/catalog/atoms.py:126-130. Síntoma: corrido desde labchile_chatbots/docs/spec2viz con --atoms-dir ../../desk/atoms, el store que se descubre es el de deskops y entran 146 átomos ajenos (p. ej. atom-agents-read-by-decision-need) en vez de los 3 del repo. Esperado: si se pasa atoms_dir, ese directorio manda para todas las vistas (o, sin él, solo el store del repo del catálogo, nunca uno ajeno). Repro: cd labchile_chatbots/docs/spec2viz && specir catalog build --config catalog.yml --out /dev/shm/c.html --atoms-dir ../../desk/atoms; contar las claves de window.ATOMS_DB. En spec2viz se bota (no se arregla un repo que se retira).
