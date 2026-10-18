---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-18T18:04:24'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T18:12:29'
---

# El caché de usuario built_cache sobrevive a borrar .sldb/runtime/ y deja los índices de secciones y semántico sin reconstruir

_Describe the incoming message with enough evidence to triage._

Repro (sldb main, 2026-10-18):

    git clone --depth 1 <repo-con-.sldb> /tmp/x && cd /tmp/x
    python3 -c "from sldb.api import rebuild_edges; rebuild_edges('.sldb')"   # crea runtime/sections, semantic, edges
    rm -rf .sldb/runtime
    python3 -c "from sldb.api import rebuild_edges; rebuild_edges('.sldb')"   # docs_written=325 ...
    ls .sldb/runtime   # edges edges.yaml locks: NO hay sections/ ni semantic/

Causa: sldb/store/section_sync.py:27 (process_model_sections) salta el modelo si
built_cache.get(store, 'sections_shards', model, key) no es None. built_cache vive en
~/.cache/sldb/runtime-cache-built/<hash del path>.json, fuera del store, y no comprueba que
los shards existan. Borrar runtime/ (que el docstring de built_cache llama 'derived; safe to
delete') deja el caché diciendo 'construido' y update_store_indexes tampoco lo repara
(sections_index docs_processed=0). Lo mismo parece aplicar al índice semántico.
Efecto: snapshot_save devuelve un grafo sin has_section ni semantic_parent.

Sugerencia: invalidar la entrada si el directorio de shards del modelo no existe (o incluir en la
clave algo que viva en runtime/), y que rebuild/update_store_indexes reconstruyan cuando falta.

Contexto: graph_ui 865ba9b hace que su test end-to-end llame rebuild_edges antes de
snapshot_save (en un clon limpio no hay runtime/); ese arreglo funciona en clon fresco, pero un
checkout que borre runtime/ a mano caería en este bug.

## Resolución

Resuelto (2026-10-18, sldb-04) en 8fce487874. Tal como diagnosticaste: built_cache (en ~/.cache/sldb) respondía por shards que ya no estaban, y además el conjunto de sucios en memoria del proceso quedaba vacío, así que ni saltándose el caché se re-sincronizaba nada. Ahora, si un modelo con documentos no tiene su carpeta de shards de sections o semantic, el caché no se cree y se re-sincronizan todos sus documentos. Test: tests/store/test_runtime_wiped.py, con tu repro en un solo proceso; falla sin el arreglo. El índice de aristas ya lo hacía.
