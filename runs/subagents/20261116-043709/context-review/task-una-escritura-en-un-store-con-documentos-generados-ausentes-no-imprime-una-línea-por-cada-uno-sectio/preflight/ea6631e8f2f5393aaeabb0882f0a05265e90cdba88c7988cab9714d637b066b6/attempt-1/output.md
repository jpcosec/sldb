## REFORMULACION

**Propósito:** eliminar el ruido de miles de avisos “Sections rebuild: doc ... missing” al escribir en el desk cuando existen PythonSymbolDoc indexados pero no generados en disco.

**Resultado:** que una reconstrucción con N documentos ausentes emita como máximo un `logger.warning` con el número total, desglose por modelo y hasta 3 rutas de ejemplo.

**Repo:** `/mnt/ssd/proyectos/SLDB_1`.

**Límites:** tocar `src/sldb/store/section_sync.py`, añadir test en `tests/store/test_semantic_rebuild.py` y actualizar `CHANGELOG.md`; no cambiar las rutas llamadoras ni limitar la reconstrucción a documentos de la transacción, ni modificar `stores check`.

## AMBIGUEDADES

1. “acumular los ausentes durante la reconstrucción y emitir un solo logger.warning al final” y “una lista que vive durante la llamada de nivel superior”: no se nombra la función superior ni el mecanismo de acumulación; obliga a inventar si será parámetro, contexto, atributo o variable local.
2. “con el formato "Sections rebuild: <n> documents missing on disk (<modelo>: <n>, ...); e.g. <ruta1>, <ruta2>, <ruta3>"”: “modelo” y los “...” no están definidos; obliga a inventar agrupación, orden, deduplicación, plurales y rutas absolutas/relativas.
3. “un store de prueba con 5 documentos trackeados cuyo archivo se borró”: no se indican fixtures ni cómo construirlo; obliga a inventar el montaje del test.
4. “`deskops edit task <una tarea> summary "x" --root sldb` en un worktree limpio”: hay placeholders y no se define el worktree; obliga a inventar comando, tarea y preparación, o a omitir la comprobación.
5. “CHANGELOG y commit.”: no se precisa entrada, sección ni mensaje de commit; obliga a inventar su contenido.

## DRY-RUN

**Lecturas:** TaskDoc, `section_sync.py` completo, llamadas en `payload_save_steps.py:112`, `untrack_document.py:68`, `rebuild_edges.py:37`, test existente y `CHANGELOG.md`.

**Cambios previstos:** acumular ausencias en el ámbito de la reconstrucción; sustituir el aviso por documento por un resumen final; añadir test con `caplog`; documentar el cambio.

**Dependencias:** logger y firma actuales de `_missing_doc`, flujo de `_sync_one_section`, fixtures del store.

**Validaciones futuras:** `TMPDIR=/dev/shm pytest -q tests/store/test_semantic_rebuild.py`; comprobación manual del desk; inspección de que solo hay un warning y dice 5; revisión de CHANGELOG y diff.

## FUTURO

El ejecutor producirá diff, test y breve informe con resultados. Un humano decidirá el formato exacto del resumen, la entrada de CHANGELOG y el mensaje/alcance del commit.
