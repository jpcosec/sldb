REFORMULACION
Propósito: que el nombre del directorio diga qué se versiona (`.sldb_store`: `store.yaml`, `core/`, `README.md`) y qué se regenera (`.sldb_cache`, ignorado), sustituyendo el literal `.sldb`. Resultado: constante `STORE_DIR_NAME`/`LEGACY_STORE_DIR_NAME` en `src/sldb/store/layout.py` y reemplazo de literales; descubrimiento con fallback a `.sldb` y alerta `store/legacy-layout`; `sldb stores migrate-layout` con `git mv` y ajuste de `.gitignore`/`.gitattributes`; `stores init` creando `.sldb_store`; store de este repo migrado y commiteado con docs, CHANGELOG y avisos; tests en `tests/store/test_legacy_layout_migration.py`. Repo: `/mnt/ssd/proyectos/SLDB_1` (sldb). Límites: no migra stores de otros repos, no elimina la lectura del layout viejo, no cambia el formato de archivos.

AMBIGUEDADES
1. "los que tengan store": no define cómo se comprueba; obliga a inventar criterio (registro global, ruta hermana o existencia de `.sldb`).
2. "el aviso va como línea \"Aviso a <repo>\" en result-summary.md": no fija ruta, formato ni quién lo escribe.
3. "con el repo en git, `git mv .sldb .sldb_store` (sin git, rename)": no dice cómo detectar git ni qué hacer con árbol sucio.
4. "emitir la alerta store/legacy-layout": no fija severidad, exit code ni texto exacto (solo un ejemplo entrecomillado).
5. "resuelve también a ../repo/.sldb_store si el primero no existe": no cubre el caso de que existan ambos.
6. "quita .sldb/.config si está vacío": no aclara si vacío = sin entradas o sin archivos.
7. "actualiza ... las rutas .sldb/ de .gitattributes si existen": no enumera rutas ni formato.
8. "grep ... solo deja la constante LEGACY_STORE_DIR_NAME": no aclara si se conservan las claves legacy-shaped de `sections_index` (`.sldb/runtime/...`).

DRY-RUN (hipotético, sin ejecutar)
Lecturas: `layout.py`, `migration.py`, parser `stores.py`, `store_discovery.py`, `store_declaration.py`, `init_store.py`, tests, docs y CHANGELOG; inventario con el `grep`. Cambios: constantes y reemplazos; fallback con alerta; ampliación de `migrate-layout`; init; migración del repo; docs/CHANGELOG; avisos; tests. Dependencias: `depends_on` del merge driver (escribe `.gitattributes`), `flock /dev/shm/sldb1-tests.lock`, deskops para avisos. Validaciones futuras: los cuatro comandos de Validation más el `grep` y `stores check`.

FUTURO
Deciden o producen otros: la ejecución real de `migrate-layout` y el commit; el envío de avisos vía deskops; cada coordinador migra su store; otra tarea retira la lectura legacy; un humano aprueba mensaje de commit y CHANGELOG.
