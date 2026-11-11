## REFORMULACION

Nodo ejecutable (`task.debug`, no agregado). **Propósito:** cerrar el fallo de seguridad de `live_stale` al cargar el índice de aristas: no abrir archivos fuera de la raíz, no seguir symlinks y no leer contenido de archivos sin cambios desde el build. **Resultado:** arreglo en `live_stale.py`, `compose.py` y `DocEdges`; tests de regresión con symlink saliente y archivo protegido; documentación y CHANGELOG; informe sobre `sldb serve`. **Repo:** `sldb` (rutas `src/sldb/store/...`, `tests/store/`, `tests/api/`, `docs/`, `CHANGELOG.md`). **Límites:** fuera de alcance rebuild y stale global (a2); la validación global de 7 pasos la corre el coordinador en clon limpio.

## AMBIGUEDADES

1. “la raíz del proyecto” no define si es raíz del repo, del store `.sldb` o del workspace; obliga a inventar la base de `is_relative_to(root.resolve())`.
2. “store/path-outside-root o similar” no fija código ni nombre exacto del hallazgo; obliga a inventarlo.
3. “se marca como stale con su motivo” no especifica motivo, enum ni formato; obliga a inventar el valor.
4. “el shard (DocEdges) guarda el stat del build” no detalla campos, compatibilidad ni migración; obliga a inventar el esquema.
5. “si rompe un caso real de sldb, el worker lo escribe y propone” no define dónde ni cómo; obliga a inventar canal y formato.
6. “el informe dice si sldb serve usa load_edge_index” no fija destinatario ni formato; obliga a inventar el informe.

## DRY-RUN

**Lecturas:** `live_stale.py`, `compose.py`, `doc_edges.py`, tests de `edge_index`/`stale`, `cli/parsers/serve.py`, docs y CHANGELOG. **Cambios previstos:** comprobar contención antes de abrir/hashear; usar `lstat` y no leer symlinks; comparar stat del build y hashear solo si cambió; ampliar `DocEdges` con stat y migrar; tests con audit hook de `open`; informe de `serve`; docs/CHANGELOG. **Dependencias:** que el build del shard escriba el stat, consumidores de `DocEdges`, fixtures de symlink y hook, API `load_edge_index`. **Validaciones futuras:** tests tocados y de `tests/store/`/`tests/api/`; después, los 7 pasos del workflow en clon limpio.

## FUTURO

El coordinador ejecuta la validación global en clon limpio. Un humano/overlord decide si la prohibición de symlinks internos rompe un caso real y aprueba la migración de `DocEdges`. La integración de `graph_ui` consume el resultado.
