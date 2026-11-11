# dbltrack-worker: un documento en el glob de un modelo padre y en los paths de un modelo hijo se trackea una sola vez

TaskDoc: `desk/tasks/task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez.md` (task.debug).
Rama `wt/dbltrack`, base `5e55de42`. Fecha: 2026-11-11.
Reproducción del coordinador: `~/proyectos/SLDB_1/coord2-ccconfig/dbltrack/repro.log`.

## Causa raíz

`src/sldb/api/stores/declared_files.py::declared_files` devuelve la concatenación de las filas
`(model, path, name)` de cada regla `include`, regla por regla, sin mirar si otra regla ya nombra
el mismo path. Con `model: TaskDoc, glob: desk/tasks/task-*.md` y la misma tarea en los `paths`
de `TaskCodeDoc`, salen dos filas para un path: `(TaskDoc, p, n)` y `(TaskCodeDoc, p, n)`.

`apply_declaration.apply_includes` trackea toda fila que no esté ya en `tracked_rows`, así que en
un build en limpio (sin caché, sin índice) el archivo se trackea bajo los dos modelos.
`undeclared` tampoco lo detecta, porque las dos filas están declaradas. `stores check` no tiene
ninguna regla sobre paths repetidos, así que el store pasa.

El síntoma en deskops viene de `resolve_indexed_document._family_hits`. `TaskDoc:<name>` busca el
nombre en `TaskDoc` y en cada modelo cuyas `base_models` incluyen `TaskDoc`. Encuentra dos filas
con el mismo path, y deskops responde `Ambiguous task selector`. Con una caché vieja no se ve: el
store ya tenía la fila del hijo y el glob se añadió después. La fila del padre solo aparece en un
build desde cero (clon nuevo o CI).
