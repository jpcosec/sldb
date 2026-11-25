REFORMULACION
Propósito: que el nombre del directorio diga qué parte del store se versiona y qué se regenera. Resultado: stores nuevos en `.sldb_store/` (store.yaml, core/, README, versionado) con `.sldb_cache/` ignorado; `sldb stores migrate-layout` migra con `git mv`; todo comando sigue leyendo `.sldb/` con alerta; el store de sldb queda migrado; avisos enviados. Repo: sldb (src/sldb/store, api/stores, cli, tests, docs, CHANGELOG). Límites: no migra stores de otros repos, no elimina la lectura legacy, no cambia el formato de archivos; los literales de `.sldb_cache` quedan fuera.

AMBIGUEDADES
1. "mismo contenido versionado (mismo store_hash)": migrate cambia las rutas relativas que registra `core/`; habría que inventar si `store_hash` debe permanecer idéntico pese al rename o solo el contenido lógico.
2. "deskops message send a deskops, IR, pron, graph_ui, spec2viz, scion y mepu": "IR" no está identificado; obligaría a inventar repo, destinatario y si tiene store.
3. "para un repo que no esté en el registro, el aviso va como línea ... en result-summary.md": no se nombra el registro ni la ruta de result-summary; habría que inventar ambos.
4. "la fecha desde la cual el layout viejo solo se lee con alerta": el input no la fija; obligaría a inventar la fecha.

DRY-RUN
Lecturas: `layout.py`, `migration.py`, `init_store.py`, `store_declaration.py`, `store_discovery.py`, `cli/parsers/stores.py`, tests citados, `.gitignore`/`.gitattributes`. Cambios previstos: constantes `STORE_DIR_NAME`/`LEGACY_STORE_DIR_NAME`; reemplazo de literales; descubrimiento con fallback y alerta `store/legacy-layout`; error `store/ambiguous-layout`; `migrate-layout` (git mv/rename, `.config` vacío, `.gitignore`, `.gitattributes`); init en `.sldb_store`; tests; migración del repo; docs, CHANGELOG; avisos. Dependencias: la tarea del merge driver (escribe rutas `.sldb/` en `.gitattributes`). Validaciones futuras: los cuatro comandos, `grep -rn '"\.sldb"'`, `stores check`.

FUTURO
Otro nodo ejecuta la implementación, migración y commit. Cada coordinador de repo migra su store al recibir el aviso. Un humano decide la fecha y el destinatario "IR". Otra tarea futura retirará la lectura del layout viejo.
