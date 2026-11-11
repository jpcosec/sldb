## REFORMULACION

Encargo de ejecución (`task.debug`) en el repo sldb (base `ca578fd2`, con `wt/secrest` integrada). Propósito: que ninguna superficie lea o escriba el texto de un documento trackeado que sea symlink o resuelva fuera de la raíz; toda lectura pasa por `sldb.store.source_read` y toda escritura abre con `O_NOFOLLOW`. Resultado observable: r1–r6 cumplidos —lecturas guardadas en edges, records, views, serve, links, segments, sections show, model_registry y structured_doc; escrituras y llamadores de `provenance_stamp.stamped_file` nombran el hallazgo en vez de propagar ELOOP; TOCTOU de `replace_text` cerrado; mensaje de `stores update` corregido; informe con tabla archivo:línea y grep final vacío o con excepciones justificadas; tests de audit hook por superficie verdes, más `test_clean_code_rules` y `tools/check.sh --fast`; CHANGELOG y docs actualizados. Límites: fuera de alcance lo ya cubierto por SEGURIDAD resto (stores check/update/build, docs track/update), el comportamiento stale/rebuild y la forma de los hallazgos existentes (`store/path-outside-root`, `store/symlink-not-read`).

## AMBIGUEDADES

1. «a confirmar y completar por grep» (Implementation Path): la lista de lecturas puede ser incompleta; el ejecutor debería inventar el criterio de completitud y qué sitios adicionales entran.
2. «falla con error claro cuando el documento es el objetivo único del comando» (r1): no define código, mensaje ni código de salida; obliga a inventar el contrato de error.
3. «abren con O_NOFOLLOW (o por source_read)» (r3): dos alternativas sin criterio de elección; obliga a inventar cuál es la canónica.
4. «necesita eje en contracts/layers.toml» (r6): no indica qué eje asignar a un archivo nuevo; obliga a inventar su clasificación.
5. «Los grados medidos de unidad se actualizan con comentario fechado si cambian» (r6): no dice dónde se registran esos grados; obliga a inventar la ubicación.

## DRY-RUN

Lecturas previstas: TaskDoc, commit base, los archivos listados en `files:`, `sldb.store.source_read`, `provenance_stamp`, tests de seguridad existentes, `contracts/layers.toml` y `tools/check.sh`. Cambios previstos: r1 en 17 puntos de lectura; r2 en `model_drafts/backfill.py`, `edges/builtin_relation_writes.py` y escrituras; r3 en `api/documents/replace_text.py`; r4 en `cli/commands/store_update.py`; r5 tests nuevos por superficie e informe; r6 límites de clean code. Dependencias: contrato de `source_read`, códigos de hallazgo existentes, helper de audit hook en subproceso y `test_clean_code_rules`. Validaciones futuras: pytest de superficies tocadas, `test_live_stale_security.py`, `test_tracked_reads_guarded.py`, `test_clean_code_rules`, `tools/check.sh --fast` y grep final. Nada ejecutado.

## FUTURO

El coordinador ejecuta los 7 pasos del workflow en clon limpio y decide la aceptación; un humano revisa el informe, el inventario y las excepciones del grep. Otro nodo integra el resultado.
