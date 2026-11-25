REFORMULACION
Propósito: eliminar la dependencia del test `test_explain_over_the_repo_own_index_names_origin_and_relation_doc` del `.sldb` del checkout y de `.sldb_cache`. Resultado: test reescrito en `tests/api/test_api_graph_analysis.py` que construye en `tmp_path` un store propio con documentos y aristas de origin `relation_doc` y `schema`, y comprueba que cada arista de los steps trae `origin` y `relation_doc` o `field`; debe pasar en clon limpio con `XDG_CACHE_HOME` vacío y en el checkout. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: solo ese archivo de test; no tocar `src/` (`path_steps`, `analyze`); si aparece dependencia de caché, anotarla en `result-summary.md` y decidir el coordinador; borrar el clon de `/dev/shm`. No es agregado ni paquete: es `task.code` ejecutable.

AMBIGUEDADES
1. “con aristas de origin relation_doc y schema reales” / “al menos una arista de origin relation_doc y otra de origin schema”: no aclara si ambas deben estar en el mismo path/steps o pueden probarse en caminos distintos. Obligaría a inventar la topología y el alcance de la aserción.
2. “puede reutilizar el AnalysisWorld del mismo archivo si ya las tiene, o un fixture mínimo”: no especifica si `AnalysisWorld` ya contiene una arista `schema` ni si modificarlo es aceptable. Obligaría a decidir sin criterio si se toca un fixture compartido.
3. “sin knowledge/symbols generados”: no define qué rutas concretas deben faltar o limpiarse. Obligaría a inventar una lista de artefactos generados.

DRY-RUN
Lecturas: `tests/api/test_api_graph_analysis.py` (test actual y `AnalysisWorld`), API pública de store/graph y `path_steps`. Cambios previstos: reescribir solo ese test para crear un store en `tmp_path` con documentos y aristas `relation_doc` y `schema`; si hace falta, construir el índice con API pública; ajustar aserciones a `origin` y `relation_doc`/`field`. Dependencias: `api.init_store`, `add_model`, `init_relations`, `create_document`, `graph_path`/`explain_path`, fixture `tmp_path`. Validaciones futuras: los tres comandos del TaskDoc; además clon limpio en `/dev/shm` con `XDG_CACHE_HOME` vacío y pytest del archivo; borrar el clon; guardar salida rc 0 en `result-summary.md`.

FUTURO
El ejecutor producirá el test reescrito y `result-summary.md`; testing/closeout validarán y se hará commit. El coordinador decide si el test revela dependencia de `src/` en la caché. No es ambigüedad.
