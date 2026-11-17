---
sldb:
  by: agent
  at: '2026-11-17T02:03:29Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T10:18:51'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T23:02:37'
---

# sldb serve: list_views compone el índice federado de toda la máquina en frío y sin lock; 2-5 GB por proceso

_Describe the incoming message with enough evidence to triage._

Hallazgo en robocop2 (2026-11-16) con evidencia en UIs/graph_ui/runs/subagents/20261116-sldb-serve-rss/ (README.md, rss2.log, stack5.txt, compose-single.out). Caso mínimo: pytest tests/test_mindmap_deskops.py::test_real_advance_stale_origin_and_types (un worker, MemoryMax=3G): el sldb serve que levanta graph_ui sobre un desk temporal de 300 KB pasa de 55 MB a 2,4 GB en 63 s y nunca responde. Pila (faulthandler): 6 hilos de petición en list_views -> load_edge_index(include_linked=True) -> compose_edge_index -> _merge_store -> load_edges_shard -> _cached_shard(model_copy(deep=True)). En un hilo, load_edge_index sobre ese store federa por enlaces transitivos 7 stores (el suyo, deskops, sldb, spec2viz, pron, scion, /mnt/ssd/herramientas/deskops): 15.617 shards, 31.152 nodos, 178.756 aristas, 35,5 s y 1,2 GB en frío (0,6 s en caliente). Causas: (1) list_views (src/sldb/api/views/list_views.py:24) pide el índice federado completo y transitivo solo para listar ViewDoc; (2) compose_edge_index no tiene lock: cada petición concurrente en frío compone por su cuenta, retiene sus copias profundas y la memoria se multiplica por el número de hilos; (3) el timeout del cliente no cancela el hilo. Con pytest -n 4 de graph_ui, 4 serves llegaron a 2,3-4,8 GB cada uno y robocop2 quedó con 5 GB disponibles (riesgo de OOM para todos los agentes). Propuestas: lock (single-flight) por clave en compose_edge_index; list_views sin la federación transitiva o solo con el modelo ViewDoc; no hacer copia profunda de cada shard al componer en solo lectura; tope de hilos en sldb serve.
