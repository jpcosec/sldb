# REFORMULACION

Encargo ejecutable (no agregado): en el repo SLDB_1, hacer que los tres textos que hoy mandan a reconstruir ante un `EdgeIndex.stale` por edición externa indiquen `sldb stores update` (`update_store_indexes`), y probarlo con un test. Resultado esperado: descripción del campo `stale` en `src/sldb/store/edge_index/edge_index.py`, docstring de `load_edge_index` en `src/sldb/api/edges/edge_reading.py` y alerta `edges/stale` de `_report_findings` en `src/sldb/cli/commands/edges.py` con los textos exactos de las precisiones; test nuevo en `tests/api/test_api_edges.py` (edición externa → `stale` → `rebuild_edges` no lo saca → `update_store_indexes` sí); entrada en `CHANGELOG.md`. Límites: no rehashear en `rebuild_edges`, no tocar `stale` por documento en graph_ui, no modificar `tests/api/test_composition_edges.py`, no push.

# AMBIGUEDADES

1. "Del grep solo se cambian los mensajes cuyo texto habla de stale o de documentos editados fuera de sldb" — no hay criterio objetivo para los mensajes del grep que mencionan rebuild sin decir stale ni versión; obliga a inventar el juicio de clasificación.
2. "alerta de _report_findings ... (what: ..., fix: ...)" — no se da la firma de `alert()`; el orden/aridad de argumentos se infiere del texto, no del código.
3. "editar a mano un documento de un store de prueba" — no especifica el mecanismo (escribir el archivo, mutar payload, tocar timestamps) para que `live_stale` lo detecte; obliga a inventarlo.
4. "la tarea se detiene y el ejecutor reporta el caso" frente a "Done When: ... CHANGELOG y commit" — no dice si en el camino de fallo se commitean los cambios de texto ya hechos.
5. "bajo el encabezado \"## 0.1.13 — not released yet\"" — no consta que ese encabezado exista a HEAD 7288d93e; si falta, no se indica crearlo.
6. "deskops message send --to <repo>" vs. "aviso a graph_ui" — el placeholder `<repo>` no se resuelve explícitamente a `graph_ui`.

# DRY-RUN

Lecturas: los cinco archivos citados, la inbox-note de origen, `rebuild_edges.py`, `CHANGELOG.md` y los helpers de `tests/api/test_api_edges.py`. Cambios: test primero; luego tres literales; línea de changelog; grep y alineación de mensajes. Dependencias: existencia del encabezado 0.1.13, firma real de `alert`, helpers de store de prueba. Validaciones futuras: los dos pytest con `TMPDIR=/dev/shm`. Nada ejecutado.

# FUTURO

El coordinador hace el commit con `deskops closeout commit` y no hay push. El ejecutor escribe `runs/subagents/<run-dir>/result-summary.md` y envía el aviso (o lo anota si el repo no está registrado). Si `update_store_indexes` no saca el documento de `stale`, decide un humano cómo seguir.
