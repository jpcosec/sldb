---
sldb:
  by: agent
  at: '2026-11-16T08:25:21Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T00:47:03'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:25:05'
---

# sldb matching: el payload de átomos del catálogo incrusta rutas absolutas (path y store) en ATOMS_DB

_Describe the incoming message with enough evidence to triage._

Origen: inbox de spec2viz 20261104-192518 (visto en MEPU el 2026-11-04 en rendered/catalogo.html). spec2viz se retira (IR/docs/spec2viz/acta-de-retiro.md) y el código pasó a sldb igual: sldb/src/sldb/api/matching/atom_payload.py:30 emite "path": str(doc_path) y "store": str(store_path) absolutos por átomo (store_documents.py:22-23 hace lo mismo con "store" y "path"); specir catalog build los vuelca en window.ATOMS_DB/ATOMS_BY_VIEW (IR/src/specir/visual/catalog/atoms.py:146). Efecto: un HTML commiteado queda atado a la máquina y a la ubicación de cada repo (p. ej. /home/jp/proyectos/SLDB_1/deskops/desk/atoms/...) y cambia si se mueve un repo. Propuesta: emitir la ruta relativa a la raíz del repo del átomo (o id de repo + ruta relativa) y no emitir la ruta del store. Verificación sugerida: construir un catálogo y comprobar que grep -c "/mnt/\|/home/" sobre el HTML da 0.
