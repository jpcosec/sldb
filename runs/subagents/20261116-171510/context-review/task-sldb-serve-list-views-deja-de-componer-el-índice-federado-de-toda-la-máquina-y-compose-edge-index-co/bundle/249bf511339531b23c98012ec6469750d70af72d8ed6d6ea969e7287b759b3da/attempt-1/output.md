## REFORMULACION

Encargo del nodo `task.code` en el repo `/mnt/ssd/proyectos/SLDB_1` (sldb): evitar que `list_views` componga el índice federado completo solo para listar `ViewDoc`, y hacer que `compose_edge_index` componga una sola vez por clave ante peticiones concurrentes en frío. Resultado: mismas vistas listadas —locales y enlazadas, H9— sin `compose_edge_index`, single-flight por clave y caso mínimo de graph_ui por debajo de 1 GB. Límites: nuevos `view_nodes.py` y `compose_lock.py`, cambios en `list_views.py`, tests indicados y `CHANGELOG.md`; fuera: `copy=False` global en `read_store_contributions`, límite de hilos en `sldb serve` y timeouts.

## AMBIGUEDADES

1. «el comando en el README de su evidencia» y «después < 1 GB»: el README no está en el bundle; obligaría a inventar el caso mínimo y el comando de medición.
2. «compose_edges_documents(ruta, "ViewDoc", copy=False)» y «federated_stores(store_path, True)»: `shard_compose.py` y `federation.py` se nombran pero no se incluyen; obligaría a inventar firmas y formatos.
3. «estampa facets.source.store_path»: no aclara si conserva `generated_from` y `hash_a` como `_source`; obligaría a inventar el contrato de facets.
4. «list_views con compose_edge_index parcheado para lanzar»: no fija el punto de parcheo (`load_edge_index`, `compose_edge_index` o `view_nodes`); obligaría a inventar el monkeypatch.
5. «8 hilos que llaman a la vez ... cuentan una sola composición»: no define barrera, clave exacta ni compositor interno a contabilizar; obligaría a inventar el test.
6. «devuelve las mismas vistas que hoy»: no fija orden, colisiones ni aviso por ruta rechazada; obligaría a inventar la equivalencia exacta.
7. «aviso a graph_ui con deskops message send --to graph_ui»: no da asunto ni cuerpo; obligaría a inventar el mensaje.

## DRY-RUN

Lecturas: `list_views.py`, `view_reading.py`, `compose.py`, `composed_reading.py`, `federation.py`, `shard_compose.py`, `shards.py`, tests nombrados y rituales. Cambios previstos: crear `view_nodes.py` con lectura directa de shards `ViewDoc` y calificación; reescribir `list_views` para usarlo; crear `compose_lock.py` y envolver la rama de fallo de caché de `compose_edge_index`; añadir tests y entrada de CHANGELOG. Dependencias: APIs reales de federación y composición de shards, más el compositor interno observable. Validaciones futuras: los siete comandos listados, de menor a mayor alcance, y medición RSS antes/después. No se ejecuta nada.

## FUTURO

Otros nodos o humanos: validar la medición RSS en robocop2 y su evidencia; confirmar el aviso a graph_ui; decidir una tarea aparte para `copy=False` global; ejecutar testing/closeout, commit y retirada del Board.
