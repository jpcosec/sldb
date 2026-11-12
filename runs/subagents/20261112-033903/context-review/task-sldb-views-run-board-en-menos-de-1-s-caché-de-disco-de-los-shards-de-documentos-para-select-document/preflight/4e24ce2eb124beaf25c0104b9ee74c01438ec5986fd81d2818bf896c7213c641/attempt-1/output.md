## REFORMULACION

Encargo ejecutable sobre el repo `sldb`, partiendo de `main` con H11 ya integrada. Propósito: que `sldb views run board`, con el store construido y en un proceso nuevo, tarde menos de 1 s (mediana de 3) sobre el layout del benchmark de H11, sin cambiar el resultado ni la revisión de la vista. Resultado esperado: pasos b1-b5 con mediciones antes/después (caché fría y caliente), una caché de disco en JSON —nunca pickle— de lo que `select_documents` necesita de los shards de documentos, recorte seguro del import de `sldb.api`, tests, docs de vistas y CHANGELOG. Límites: fuera de alcance el índice de aristas y su caché compuesta, el costo de deskops en `view board`, H12 y H13; no se cambia la superficie pública ni el orden de efectos; si el recorte del import es menor a 0,1 s no se hace y se mide; si no se alcanza la meta, se explica con medición. El worker valida con tests de a uno, suite completa de a un archivo desde `/dev/shm`, `test_clean_code_rules` y `tools/check.sh --fast`; los 7 pasos del workflow los corre el coordinador.

## AMBIGUEDADES

1. «en el .sldb_cache del store que llama»: no define la raíz exacta ni si `select_documents` recibe el store; obliga a inventar la convención de ruta.
2. «lo que select_documents necesita de los shards de documentos»: no enumera campos; obliga a inventar el esquema JSON.
3. «la versión del índice y el contrato de cada modelo»: no indica cómo obtenerlos ni su formato; obliga a inventar claves de invalidación.
4. «la revision de la vista»: no define qué es la revisión; obliga a inferir su representación.
5. «el layout del benchmark de H11» y «el script del benchmark vive en tests/perf de esa tarea»: no da ruta exacta; obliga a buscarlo o inventarlo.
6. «caché frío además del caliente»: no define frío/caliente; obliga a fijar el procedimiento.
7. «los 7 pasos del workflow de sldb»: no los enumera; obliga a consultarlos fuera del input.

## DRY-RUN

Lecturas: TaskDoc, informe/repro de H11, script de benchmark en `tests/perf`, `select_documents.py`, `store/io`, `store/edge_index` como patrón, `contracts/layers.toml`, `docs/architecture/views.md`, tests y `tools/check.sh`. Cambios previstos: b1 perfil con `-X importtime` y cProfile; b2 módulo de caché JSON con clave por mtimes/tamaños de `core/documents`, versión de índice y contrato; b3 imports perezosos solo si el recorte seguro ≥0,1 s; b4 tests de equivalencia, invalidación y caché corrupta; b5 docs y CHANGELOG. Dependencias: H11 integrada, benchmark disponible, límites de clean code. Validaciones futuras: benchmark mediana 3 frío/caliente, equivalencia de resultado y revisión, invalidación al escribir/cambiar documento, caché corrupta ignorada, `test_clean_code_rules`, suite por archivo desde `/dev/shm`, `check.sh --fast`.

## FUTURO

El coordinador confirma que H11 está integrada y ejecuta los 7 pasos del workflow. El worker de H11 aporta benchmark y repro. Un humano decide si acepta la meta no alcanzada con explicación. Otra tarea cubre deskops; H12 y H13 quedan para nodos posteriores.
