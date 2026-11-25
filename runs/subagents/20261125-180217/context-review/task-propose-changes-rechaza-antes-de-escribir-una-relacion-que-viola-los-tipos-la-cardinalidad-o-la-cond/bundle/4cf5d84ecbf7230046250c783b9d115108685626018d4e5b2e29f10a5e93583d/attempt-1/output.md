## REFORMULACION

Encargo: que `propose_changes` valide un lote antes de escribir y rechace relaciones que violan tipos, cardinalidad o condición. Resultado: rechazo con motivo por violación, sin tocar el store; el lote se prevalida como unidad; `pendings` deja de declarar faltante esa validación; `dry_run` informa lo mismo. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: dentro `src/sldb/mcp/write/`, `changes/assert_edge.py` y `sldb.api.apply_batch`; fuera portar pron, registro persistente/undo y cualquier interfaz.

## AMBIGUEDADES

1. «el estado que resultaría del lote»: no define orden de operaciones ni dependencias entre relaciones del mismo lote; obliga a inventar la semántica de simulación.
2. «reusando las comprobaciones [...] que ya hace check_edges»: no da firma ni aclara si exige store escrito; obliga a inventar cómo reutilizarlas sin escribir.
3. «un motivo por cada violación» y «nombra la relación y la violación»: no fija formato, código de error ni si varias violaciones de una relación producen varios motivos; obliga a inventar el contrato de salida.
4. «el hash del store no cambia»: no define qué hash ni cómo obtenerlo; obliga a inventar el mecanismo de aserción.
5. «apply_batch con dry_run»: no dice si `dry_run` ya existe, su firma ni si devuelve la misma estructura de rechazo; obliga a inventar API.
6. «pendings deja de informar la validación de relaciones como faltante»: no cita el texto exacto ni el criterio de retirada; obliga a inventar mensaje y condición.

## DRY-RUN

Lecturas: `docs/architecture/{rules,edges,mcp}.md`, implementación de `check_edges`, `src/sldb/mcp/write/{propose,pendings,findings}.py`, `changes/assert_edge.py`, `sldb.api.apply_batch`, tests existentes. Cambios previstos: prevalidación sobre estado simulado antes de escribir; integración en `propose` y `dry_run`; motivos agregados; retirada del aviso en `pendings`; nuevo test `tests/test_mcp_propose_rejects_invalid_edges.py`. Dependencias: funciones de `check_edges`, modelo de estado, contrato de findings. Validaciones futuras: los dos `pytest` indicados, hash de store invariante, lote válido sin regresión, lote mixto rechazado entero, `dry_run` coherente.

## FUTURO

Un nodo de ejecución implementa el cambio; el ritual de testing ejecuta las suites; closeout commitea y cierra. Un humano debe resolver las ambigüedades 1–6. Otra tarea cubre registro/undo; `graph_ui` consume el rechazo.
