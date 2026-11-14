## REFORMULACION

**Propósito:** optimizar `run_view`/`load_edge_index` para que no compongan en cada proceso el índice de aristas de todos los stores enlazados cuando la vista solo necesita algunos. **Resultado:** `sldb views run board` y `deskops view board`, en proceso nuevo y con el store construido, tardan menos de 1 s; en frío no empeoran; resultado y revisión de la vista no cambian. **Repo:** sldb (`src/sldb/api/views/`, `src/sldb/api/edges/`, `src/sldb/store/edge_index/`, `src/sldb/store/io/`, `tests/`, `docs/architecture/views.md`, `CHANGELOG.md`, `contracts/layers.toml`). **Límites:** fuera H12, H13, ViewDoc/contrato de deskops y cualquier cambio de resultado; obligan `tests/test_clean_code_rules.py` y `tools/check.sh --fast`. No es agregado ni paquete no ejecutable: es una tarea ejecutable de depuración/optimización.

## AMBIGUEDADES

1. «El criterio sale de la definición de la vista, no de una lista fija.» Obliga a inventar qué parte de la definición selecciona stores/filtros y cómo demostrar que un store enlazado no hace falta.
2. «si h2 no alcanza para menos de 1 s» y «solo si h2 y h3 no alcanzan»: no define margen ni medición exacta para decidir pasar a h3/h4; obliga a fijar umbral y metodología.
3. «el índice compuesto (o las contribuciones por store) se guarda en disco»: obliga a inventar formato, ubicación y granularidad.
4. «clave por los hashes de los índices de cada store»: obliga a elegir algoritmo y canonicalización del hash.
5. «no más lento que hoy»: obliga a fijar la línea base (¿9,4/9,7 s? ¿10,89 s?) y condiciones.
6. «los 7 pasos del workflow de sldb»: no están enumerados; obliga a conocerlos externamente.

## DRY-RUN

Lecturas previstas: `run_view.py`, `edge_reading.py`, `edge_index`, tests, docs de vistas, `contracts/layers.toml` y nota 9c08039a. Cambios previstos: h1 benchmark reproducible; h2 lectura selectiva por secciones/filtros; h3 caché en disco con clave por hashes si hace falta; h4 coste por shard; h5 test de equivalencia de resultado/revisión; docs y CHANGELOG. Dependencias: tarea H1-H3, layout de reproducción con stores enlazados, store construido, caché fría/caliente. Validaciones futuras: benchmark <1 s, comparación en frío, test de equivalencia e invalidación, suite completa de a un archivo desde `/dev/shm`, `test_clean_code_rules`, `tools/check.sh --fast`.

## FUTURO

El worker mide y elige h2/h3/h4, y reporta números antes/después. El coordinador ejecuta los 7 pasos del workflow en clon limpio. Otro nodo aporta el log/layout de reproducción. Un humano decide si alguna opción excede el alcance.
