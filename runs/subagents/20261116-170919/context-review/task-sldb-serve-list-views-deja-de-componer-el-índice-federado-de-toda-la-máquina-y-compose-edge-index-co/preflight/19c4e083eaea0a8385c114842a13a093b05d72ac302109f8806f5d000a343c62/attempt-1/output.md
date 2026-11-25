## REFORMULACION
**Propósito:** evitar que `sldb serve` componga el índice federado completo de la máquina al listar vistas y evitar composiciones duplicadas concurrentes. **Resultado:** `list_views` lista las mismas `ViewDoc` locales y enlazadas sin llamar a `compose_edge_index`; N llamadas concurrentes en frío con la misma clave componen una vez; el caso mínimo de graph_ui queda por debajo de 1 GB. **Repo:** `SLDB_1`, módulos `src/sldb/api/views/`, `src/sldb/store/edge_index/`, tests indicados, `CHANGELOG.md`. **Límites:** no cambia la semántica global de copias en `read_store_contributions`, no limita hilos de `serve` ni añade timeouts. Es un nodo ejecutable `task.code`, no un agregado.

## AMBIGUEDADES
1. «el caso mínimo de graph_ui (comando en el README de su evidencia)»: el input no da ruta ni comando; obligaría a inventar dónde está ese README y cómo reproducir la medición.
2. «result-summary.md tiene el RSS máximo... antes y después»: no se indica ubicación del archivo ni si el "antes" debe medirse en el mismo entorno; obligaría a inventar destino y método de baseline.
3. «(locales y de stores enlazados, H9)»: «H9» no se define; obligaría a inventar qué requisito o comportamiento designa.
4. «federated_stores(store_path, True)»: no se define `store_path` ni el significado del booleano; obligaría a inferir la firma y el punto de entrada.
5. «aviso a graph_ui con deskops message send --to graph_ui»: no se concreta contenido ni criterio de cierre del aviso; obligaría a inventar el mensaje.
6. «CHANGELOG.md»: no se indica sección/formato de entrada; obligaría a inventar convención.

## DRY-RUN
**Lecturas previstas:** `list_views.py`, `view_reading.py`, `compose.py`, `composed_reading.py`, `federation.py`, `shard_compose.py`, `shards.py`; tests citados y CHANGELOG. **Cambios previstos:** crear `view_nodes.py` y `compose_lock.py`; sustituir la llamada de `list_views`; envolver la rama de fallo de caché de `compose_edge_index` con single-flight por clave; añadir dos tests y changelog. **Dependencias:** APIs internas de federación, composición y calificación de nodos; lock de módulo; monkeypatch del compositor. **Validaciones futuras:** los siete comandos pytest/check indicados, más medición RSS y aviso a graph_ui. **Sin ejecutar nada.**

## FUTURO
Otro nodo o humano decide la ubicación/formato de `result-summary.md`, aporta el comando exacto de graph_ui, valida el baseline RSS, revisa el commit y confirma la recepción del aviso.
