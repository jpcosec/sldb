## REFORMULACION
Propósito: hacer visible en el nombre qué parte del store se versiona y cuál se regenera. Resultado: stores nuevos en `.sldb_store/` (store.yaml, core/, README.md versionados) con cache en `.sldb_cache/` (ignorado); constantes `STORE_DIR_NAME`/`LEGACY_STORE_DIR_NAME` en `src/sldb/store/layout.py` y sustitución de literales; lectura del layout viejo con alerta `store/legacy-layout`; `sldb stores migrate-layout` con `git mv`, idempotente; `stores init` crea `.sldb_store/`; migrar el store de este repo; docs, CHANGELOG, avisos y tests en `tests/store/test_legacy_layout_migration.py`. Repo: `/mnt/ssd/proyectos/SLDB_1` (sldb). Límites: no migra stores de otros repos, no retira la lectura del layout viejo, no cambia formatos.

## AMBIGUEDADES
1. «preferir .sldb_store; si solo existe .sldb, usarlo»: no define qué hacer si coexisten ambos; obliga a inventar precedencia o error.
2. «quita .sldb/.config si está vacío»: no define el caso no vacío; obliga a inventar (¿abortar, avisar, dejarlo?).
3. «las rutas .sldb/ de .gitattributes si existen»: no identifica archivo ni entradas; obliga a inventar alcance.
4. «`grep -rn '"\.sldb"' src/sldb` solo deja la constante LEGACY_STORE_DIR_NAME» contradice «un literal que forma parte de ".sldb_cache" no cuenta» (el patrón también casa `.sldb_cache`); obliga a inventar el criterio de éxito.
5. «la fecha desde la cual el layout viejo solo se lee con alerta»: fecha no fijada; obliga a inventarla.
6. «para un repo que no esté en el registro»: "registro" no definido; obliga a inventar dónde se consulta.
7. «mismo store_hash»: no aclara si el hash es independiente de la ruta; obliga a asumirlo.

## DRY-RUN
Lecturas: `layout.py`, `migration.py`, parser de `migrate-layout`, `init_store.py`, `store_discovery.py`, `store_declaration.py`, tests, docs y CHANGELOG. Cambios previstos: constantes y reemplazo de ~35 literales; fallback con alerta; `migrate-layout`; `init`; tests; migración de este repo en el mismo commit; docs y avisos. Dependencias: `depends_on task-merge-...` (escribe rutas `.gitattributes`). Validaciones futuras: tres `pytest -q` y `sldb stores build --check --store .sldb_store` bajo `flock /dev/shm/sldb1-tests.lock`. Nada ejecutado.

## FUTURO
El nodo del merge driver produce las rutas `.gitattributes` previas; un humano decide las ambigüedades 1–6; los coordinadores de otros repos ejecutan `migrate-layout` al recibir el aviso; deskops entrega los mensajes.
