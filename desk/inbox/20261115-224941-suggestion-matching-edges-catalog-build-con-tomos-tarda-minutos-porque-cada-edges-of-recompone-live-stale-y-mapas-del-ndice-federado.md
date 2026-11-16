---
sldb:
  by: agent
  at: '2026-11-16T08:24:41Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T22:49:41'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:24:25'
---

# matching/edges: catalog build con átomos tarda minutos porque cada edges_of recompone live-stale y mapas del índice federado

_Describe the incoming message with enough evidence to triage._

Medición de IR13 (pendiente que dejó IR13d): `specir catalog build --config tests/visual/fixtures/catalog/examples/catalog/project.yml` dentro del repo IR no termina en 300 s (`timeout 300`, rc 124, 3 min 50 s de CPU). El tiempo es de sldb, no de specIR.

cProfile (corrida cortada a los 150 s): 146 de 149 s en `specir.visual.catalog.atoms.catalog_atoms` -> `sldb.api.matching.attach_atom_edges` -> `StoreReader.edges_of` (31 llamadas, una por átomo/ref) -> `store_edges.edges_of` -> `edges_from` + `edges_to` -> `load_edge_index` (62 llamadas, ~1,1 s cada una):
- `compose_edge_index` acierta la caché de `_COMPOSED`, pero `with_live_stale` corre `stale_of_facts` en cada llamada (490 llamadas, 284 251 `_moved`, 613 577 `Path.resolve` en `source_read.unreadable_reason`: 63 s).
- Como el índice federado tiene stale extra, `with_live_stale` devuelve un `model_copy` nuevo en cada llamada, y `EdgeIndex._ensure_maps` reconstruye los mapas cada vez (61 llamadas, 66 s, con 19 M de `pydantic __getattr__`).
- El store descubierto es el `.sldb` de IR (el fixture vive dentro del repo y el catálogo sube al store del proyecto, como spec2viz). Federa 8 stores: IR, deskops, sldb, spec2viz, pron, scion y además `/mnt/ssd/herramientas/deskops/.sldb` y `/mnt/ssd/herramientas/sldb/.sldb` (los checkouts de despliegue, con los mismos nombres `deskops` y `sldb` que los de SLDB_1). `load_edge_index(IR/.sldb)`: primera llamada 28,6 s, siguientes 0,4 s cada una, cada vez un objeto distinto, 1963 stale.

Pedido: que leer aristas varias veces del mismo store no recalcule el estado vivo ni los mapas en cada llamada. Opciones: (a) `StoreReader` de `sldb.api.matching` carga el índice una vez por store y consulta `edges_from`/`edges_to` sobre ese objeto; (b) `with_live_stale` guarda su resultado mientras no cambien la firma de los shards ni los stats de las fuentes, o no copia el índice (y conserva los mapas) cuando solo añade stale; (c) `model_copy` conserva los mapas ya construidos. Además conviene revisar si es correcto que IR federe dos veces `deskops` y `sldb` (SLDB_1 y herramientas). specIR no lo arregla por su lado porque solo usa la API pública (`attach_atom_edges` con el `StoreReader` de sldb).

Reproducir: `cd IR && timeout 300 .venv/bin/specir catalog build --config tests/visual/fixtures/catalog/examples/catalog/project.yml --out /tmp/x.html`.
