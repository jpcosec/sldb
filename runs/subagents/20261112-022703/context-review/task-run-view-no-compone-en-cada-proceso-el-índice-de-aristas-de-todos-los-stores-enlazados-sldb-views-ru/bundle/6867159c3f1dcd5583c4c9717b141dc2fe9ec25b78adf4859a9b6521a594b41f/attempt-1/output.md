## REFORMULACION

Nodo ejecutable (`task.debug`), no agregado. Propósito: que `run_view` no componga en cada proceso el índice de aristas de todos los stores enlazados. Resultado observable: `sldb views run board` y `deskops view board`, en proceso nuevo con el store construido, por debajo de 1 s sobre el layout de deskops; en frío no peor que hoy; resultado y `revision` idénticos. Repo: `sldb` (`src/sldb/api/views/`, `api/edges/`, `store/edge_index/`, `store/io/`, tests, `docs/architecture/views.md`, `CHANGELOG.md`, `contracts/layers.toml`). Límites: fuera H12, H13, la ViewDoc/contrato de deskops y cualquier cambio del resultado; h1–h5 en orden, midiendo antes de elegir.

## AMBIGUEDADES

1. "en frío (sin caché de disco) no tardan más que hoy" frente a "tardan menos de 1 s": no dice si <1 s aplica solo en caliente. Obliga a inventar el umbral en frío.
2. "run_view solo lee los shards de los stores que alguna sección puede seleccionar" con "El criterio sale de la definición de la vista, no de una lista fija": no define cómo un `where` o `include_linked` determina stores. Obliga a inventar el análisis (conservador o exacto).
3. "las secciones del board solo seleccionen documentos locales" contradice `views.md`: "select, project and join over the store that calls, never over the store the ViewDoc comes from". Obliga a decidir qué premisa vale.
4. "clave por los hashes de los índices de cada store": no nombra qué campo es ese hash. Obliga a inventar su definición e invalidez.
5. "Un store enlazado cambiado se nota en la siguiente corrida" choca con h2 (store no leído) y con la caché de h3. Obliga a inventar cómo se detecta sin leerlo.
6. "la revision ... no cambian" frente a "the store's shards signature" (`views.md`): no aclara si reducir stores altera la firma de shards. Obliga a inventar el alcance de la firma.
7. "los 7 pasos del workflow de sldb" no se enumeran en el input. Obliga a inventarlos.
8. `pills: []` y `atoms: []` frente a la instrucción "las pills ligadas" y al ritual "Bind the pills": no hay ninguna. Obliga a inventar cuáles.
9. No fija commits de spec2viz/scion del layout. Obliga a inventar versiones.

## DRY-RUN

Lecturas: `run_view.py:72`, `edge_reading.py:14`, `views.md`, `layers.toml`, `tests/api/test_views.py`, `tests/test_clean_code_rules.py`, `repro.log`. Cambios: script de benchmark (h1); filtrado de stores por selectores (h2); caché en disco por hash de índice (h3); coste por shard (h4); test de equivalencia resultado/revisión (h5); docs, CHANGELOG y eje en `layers.toml` si aparece carpeta nueva. Dependencias: tarea H1–H3 (mismo índice) y layout deskops. Validaciones futuras: benchmark frío/caliente, equivalencia, `test_clean_code_rules`, `tools/check.sh --fast`, suite por archivo desde `/dev/shm`, 7 pasos.

## FUTURO

El coordinador ejecuta los 7 pasos y valida `repro.log`; un humano fija el umbral en frío y resuelve las ambigüedades 1–7; deskops mantiene Board y closeout; H12/H13 quedan para otros nodos.
