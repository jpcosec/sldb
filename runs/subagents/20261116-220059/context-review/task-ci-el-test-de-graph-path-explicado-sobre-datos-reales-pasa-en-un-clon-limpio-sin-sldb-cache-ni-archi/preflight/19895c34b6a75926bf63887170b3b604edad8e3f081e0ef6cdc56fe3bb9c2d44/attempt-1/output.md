## REFORMULACION

Encargo (`task.code`, nodo `ritual-execution`, repo SLDB_1): reescribir en `tests/api/test_api_graph_analysis.py` el test que ejercita `graph_path(..., explain=True)` —hoy `test_explain_over_the_repo_own_index_names_origin_and_relation_doc`— para que deje de leer el `.sldb` del repo y construya en `tmp_path` un store propio con documentos y al menos una arista `origin: relation_doc` y otra `origin: schema`, verificando que cada step trae su `origin` y su `relation_doc`/`field`. Resultado esperado: el test pasa tanto en un clon limpio (sin `.sldb_cache`, sin `knowledge/symbols`, `XDG_CACHE_HOME` vacío) como en el checkout. Límite: no modificar `src/`; si aparece dependencia espuria de la caché, se documenta y decide el coordinador.

## AMBIGUEDADES

1. "puede reutilizar el AnalysisWorld del mismo archivo si ya las tiene, o un fixture mínimo" — obliga a inventar qué opción elegir y si `AnalysisWorld` ya cubre ambas aristas.
2. "sin knowledge/symbols generados" — no aclara si hay que impedir su generación, borrarlos o basta con que no existan; obliga a inventar el criterio de comprobación.
3. "se anota en result-summary.md" — no aparece en `files:` ni se define ruta/formato; obliga a inventar ubicación y contenido.
4. "commit" — sin rama, mensaje ni política; obliga a inventar convención.
5. "Borrar el clon de /dev/shm" — sin ruta concreta; obliga a inventar directorio.
6. Los comandos de Validation no fijan `XDG_CACHE_HOME` ni clon limpio, pese a exigirlo "Done When"; obliga a inventar si se añaden.

## DRY-RUN

Lecturas: `tests/api/test_api_graph_analysis.py` (test y `AnalysisWorld`), API pública de construcción de store/índice. Cambios previstos: solo ese archivo de test, usando `tmp_path` y API pública. Dependencias: `uv` con `--extra code --extra dev`, `git`, `/dev/shm`, `tools/check.sh`. Validaciones futuras: los tres comandos de Validation, más la corrida en clon limpio con `XDG_CACHE_HOME` vacío. Nada ejecutado.

## FUTURO

Decisión humana/coordinador si el test revela dependencia de caché en `src/`; ejecución real del clon limpio y de `check.sh`; commit y resultado del CI de GitHub; revisión del diff.
