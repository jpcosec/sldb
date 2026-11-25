REFORMULACION
Encargo ejecutable (task.code) en el repo sldb: que un merge o rebase de dos ramas que tocaron .sldb termine sin intervención. Resultado: `rebuild-index` regenera store_index.yaml y models/*.yaml desde shards y contrato, ignorando índices ilegibles; `merge-driver` deja %A en derivados y sale 0, une includes de store.yaml y sale 1 en otros archivos; `--install` escribe .gitattributes y merge.sldb.driver, idempotente; error exacto en load_store_index/load_models_index; aviso en stores init; AGENTS.md, docs y help; tests y CHANGELOG; respuesta a MEPU. Límites: no H1/H3/H4, no cambiar qué se versiona, no usar stores build como reemplazo. Rutas: src/sldb/store/io/__init__.py, src/sldb/api/stores/update_store_indexes.py, src/sldb/cli/parsers/stores.py, tests/store/, docs/versionado-y-colaboracion.md, CHANGELOG.md.

AMBIGUEDADES
1. «deja en %A la versión de la rama actual y sale 0 (el índice correcto lo deja rebuild-index)» frente a «el merge driver de sldb resuelve store_index.yaml y models/*.yaml»: ¿regenera o solo acepta %A? Obliga a inventar si invoca rebuild-index.
2. «une las listas include de las dos ramas (por model, sin duplicar rutas)»: no define estructura ni orden de store.yaml; obliga a inventar el algoritmo de unión.
3. «avisa con una alerta si git ls-tree de otra rama local del mismo repo ya tiene .sldb/store.yaml»: no dice qué ramas ni formato de alerta; obliga a inventar alcance y mensaje.
4. «<ruta> is a derived index that git could not merge...»: no aclara si «<ruta>» se sustituye ni qué significa «no parsea»; obliga a inventar formato y criterio de excepción.
5. Tests en dos archivos sin reparto de casos; Validation añade test_stores_build.py no listado en files. Obliga a inventar la asignación.
6. «AGENTS.md nuevo en la raíz del repo de sldb»: ¿raíz del workspace o del subrepo? Obliga a elegir ubicación.

DRY-RUN
Lecturas: archivos citados y funciones de hash localizadas por grep. Cambios: API rebuild-index; subcomandos CLI; errores de carga; aviso en init; .gitattributes/config; docs, help, tests, CHANGELOG. Dependencias: formato real de store.yaml, API de hashes, git disponible. Validaciones futuras: tres pytest indicados, prueba manual en /dev/shm con y sin driver, help y docs. Sin ejecutar.

FUTURO
JP o un humano confirma la semántica del driver si persiste la ambigüedad 1; la tarea de separar .sldb_store/.sldb_cache depende de esta; MEPU recibe la nota; CI y el revisor ejecutan validaciones y commit.
