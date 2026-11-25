## REFORMULACION
Propósito: hacer visible la frontera entre lo versionado y lo regenerable del store. Resultado: stores nuevos en `.sldb_store/` (`store.yaml`, `core/`, `README.md`) y caché en `.sldb_cache/`; constantes de layout; lectura legacy de `.sldb/` con alerta; `sldb stores migrate-layout` idempotente; `stores init` crea `.sldb_store/`; store propio migrado y commiteado; tests, docs, CHANGELOG y avisos. Repo: SLDB_1 (`src/sldb`, `tests`, `docs`, `.gitignore`, `.gitattributes`, store propio). Límites: no migrar stores ajenos, no retirar aún la lectura legacy, no cambiar formatos; depende de la tarea del merge driver. Es una tarea ejecutable, no un agregado.

## AMBIGUEDADES
1. “con el comando de migración y la fecha desde la cual el layout viejo solo se lee con alerta”: no fija la fecha; obligaría a inventarla.
2. “correr stores check y stores build --check”: Validation solo detalla `stores build --check`; no da el comando exacto de `stores check`, obligando a inventar flags.
3. “para un repo que no esté en el registro”: no define qué registro ni cómo consultarlo; obligaría a inventar la fuente.
4. “los que tengan store”: no entrega inventario ni criterio de detección; obligaría a inventar el relevamiento.
5. “commitear el resultado en el mismo commit”: no fija mensaje ni granularidad; obligaría a inventar el mensaje.
6. “actualiza .gitignore (.sldb_store/ versionado, .sldb_cache/ ignorado…)”: no precisa cómo editar patrones previos; obligaría a inventar reglas de reescritura.

## DRY-RUN
Hipotético, sin ejecutar. Lecturas: `layout.py`, `migration.py`, CLI de `migrate-layout`, `init_store.py`, `store_discovery.py`, `store_declaration.py`, tests, docs, `.gitignore`, `.gitattributes` y registro de repos. Cambios previstos: crear constantes; reemplazar literales; resolver `.sldb_store` con fallback y alerta; error `store/ambiguous-layout`; migrar con `git mv` o rename, manejar `.config`, `.gitignore` y `.gitattributes`; ajustar `init`; añadir tests; migrar el store propio, documentar, actualizar CHANGELOG y enviar avisos. Dependencias: merge driver previo, git, `uv`, `flock`, registro/inbox. Validaciones futuras: los cuatro comandos de Validation, grep de literales, ausencia de `.sldb/`, avisos enviados/anotados y commit.

## FUTURO
El commit, los avisos y las líneas de `result-summary.md` quedan para coordinadores/CI; cada repo receptor decide cuándo ejecutar la migración. Otra tarea posterior retirará la lectura legacy. El nodo del merge driver entrega las líneas `.sldb/` de `.gitattributes` que esta tarea migra.
