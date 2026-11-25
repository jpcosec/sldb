REFORMULACION
Propósito: corregir `read_store` para que no indique “store not prepared” cuando el store no existe. Resultado: lanzar `SLDBStoreError` con `store not found: <ruta>` si falta el directorio del store, y conservar `store not prepared: run sldb stores update (<ruta>)` si existe pero falta el índice; añadir tests para ambos mensajes, CHANGELOG y commit. Repo: workspace actual, rutas `src/sldb/...`, `tests/api/test_api_stores.py` y `CHANGELOG.md`. Límites: tocar `read_store.py` y, si hace falta, `store_is_prepared`; no cambiar otros mensajes.

AMBIGUEDADES
1. “cuando el store existe pero le falta el índice” frente a “si falta .sldb o core/store_index.yaml”: no define si un directorio existente sin `.sldb` es “not found” o “not prepared”; obligaría a inventar la clasificación.
2. “‘store not found: <ruta>’”: no precisa si `<ruta>` es el argumento original, la ruta resuelta/absoluta o con otra normalización; obligaría a inventar el formato exacto.
3. “y en store_is_prepared si hace falta”: no fija criterio para modificar el helper ni su contrato; obligaría a inventar el diseño.
4. “aviso a graph_ui”: no indica canal, formato ni responsable; obligaría a inventar la notificación.

DRY-RUN
Hipotéticamente, un ejecutor leería `read_store.py`, `_resolve_store_arg`, `store_is_prepared`, `tests/api/test_api_stores.py` y `CHANGELOG.md`, y localizaría la resolución de ruta y la comprobación de preparación. Cambios previstos: comprobar existencia del directorio antes de preparación, emitir el mensaje nuevo, conservar el existente, ajustar mínimamente el helper si se decide, añadir tests de ambos casos y entrada de CHANGELOG. Dependencias: `SLDBStoreError`, helper de preparación y fixtures de stores temporales. Validaciones futuras, sin ejecutar: los tres comandos de `Validation`.

FUTURO
Un ejecutor producirá el parche, tests, CHANGELOG y commit; las validaciones producirán evidencia de paso/fallo. Un humano u otro nodo decidirá el canal y contenido del aviso a `graph_ui`, y resolverá previamente la semántica de ruta e índice si persiste.
