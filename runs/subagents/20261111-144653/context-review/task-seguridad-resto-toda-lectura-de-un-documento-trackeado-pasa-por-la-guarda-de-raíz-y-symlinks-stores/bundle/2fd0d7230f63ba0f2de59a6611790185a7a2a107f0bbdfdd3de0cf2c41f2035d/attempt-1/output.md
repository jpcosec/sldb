## REFORMULACION

Encargo ejecutable, no agregado: no hay hijos que recorrer. Propósito: cerrar la fuga por la que operaciones del store abren documentos trackeados que son symlink o resuelven fuera de la raíz. Resultado: un solo punto de apertura (`source_read`), hallazgo nombrado en vez de error, `track` rechaza symlinks y tests con audit hook. Repo: sldb, rutas `src/sldb/api/stores/`, `src/sldb/store/`, `src/sldb/api/documents/`, `tests/store/`, `tests/api/`, `docs/`, `CHANGELOG.md`, `contracts/layers.toml`. Límites: fuera el comportamiento stale/rebuild y la forma de los hallazgos existentes.

## AMBIGUEDADES

1. «CAUSA (lecturas sin la guarda, a confirmar y completar por grep de read_text/open…)»: la lista de archivos y líneas no está confirmada; obliga a inventar el alcance exacto de cambios.
2. «el comando lo nombra con el hallazgo existente (store/path-outside-root o store/symlink-not-read)»: no se define dónde ni cómo se emiten; obliga a inventar el contrato de hallazgos.
3. «cada excepción justificada (por ejemplo, archivos que no son documentos: store.yaml, pyproject)»: criterio abierto; obliga a inventar qué archivos eximir del grep.
4. «r1-r5 hechos con causa raíz escrita, inventario en el informe y tests verdes; CHANGELOG y docs»: no se especifica qué docs cambian; obliga a inventar su contenido.
5. «7 pasos del workflow de sldb en clon limpio»: no están enumerados en el input; obliga a inventar los pasos.
6. «Los grados medidos de unidad se actualizan con comentario fechado si cambian»: no se identifican los campos ni la medición; obliga a inventar el procedimiento.

## DRY-RUN

Lecturas hipotéticas: TaskDoc, rituales execution/testing/closeout, `contracts/layers.toml`, archivos fuente y tests nombrados. Cambios previstos: r1 centralizar lecturas de documentos en `source_read`; r2 rechazo en `docs track`; r3 inventario archivo:línea; r4 tests de audit hook en subproceso; r5 límites de `test_clean_code_rules`; docs y CHANGELOG. Dependencias: `source_read`, hallazgos existentes, Board/pills (vacías), clon limpio. Validaciones futuras: tests de check/update/build/build --check/docs update, `test_live_stale_security`, tests de store/api tocados, `test_clean_code_rules`, `check.sh --fast` y los 7 pasos. Nada ejecutado.

## FUTURO

Un humano confirma la causa por grep, aprueba las excepciones del inventario y el contenido de docs; el coordinador corre los 7 pasos y el closeout con commit atómico.
