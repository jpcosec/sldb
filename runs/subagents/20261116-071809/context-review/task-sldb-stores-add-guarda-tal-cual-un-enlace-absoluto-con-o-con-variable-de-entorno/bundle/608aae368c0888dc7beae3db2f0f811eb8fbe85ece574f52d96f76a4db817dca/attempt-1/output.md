## REFORMULACION

Propósito: corregir que `sldb stores add` guarda siempre el enlace relativo a la raíz y no resuelve igual desde clones y worktrees a distinta profundidad. Resultado: guardar la ruta tal como la escribió el usuario si empieza por `/`, `~` o `$`, y relativa a la raíz en cualquier otro caso; al leer, expandir `~` y variables de entorno. Repo: SLDB_1, HEAD orientativo 7288d93e. Límites: no resolver contra el git common dir ni migrar enlaces ya guardados; toca `link_store.py`, `query.py`, el comando `stores add` en `src/sldb/cli/commands/`, `tests/api/test_api_stores.py`, `docs/architecture/store-declaration.md` y `CHANGELOG.md`.

## AMBIGUEDADES

1. “se agrega un parámetro keyword-only raw: str | None = None”: no dice a qué función (¿`record_store_link`?, ¿`link_store`?) ni si el CLI lo atraviesa por `link_store`; obliga a inventar firma y punto de paso.
2. “en _resolve_path / _linked_stores ... aplicar os.path.expandvars y os.path.expanduser antes de resolver”: `_resolve_path` sirve a más rutas; no dice si la expansión es global o solo para enlaces; obliga a elegir alcance.
3. “guarda la ruta como la escribió el usuario” junto a `link_store`, que hace `Path(other_store).resolve()` y `_check_other_exists`: con `~/x` o `$VAR/x` literales la validación fallaría; no dice que la validación expanda; obliga a inventar dónde expandir antes de comprobar.
4. “la función de API a la que llama”: no nombra el archivo del comando `stores add` (solo `link_store.py`/`query.py` en `files`); obliga a localizarlo por grep.

## DRY-RUN

Lecturas: `src/sldb/api/stores/link_store.py` (`record_store_link` y llamador), `src/sldb/store/query.py:100-120`, comando `stores add` vía `grep -rn "record_store_link\|link_store" src/sldb/cli`, `tests/api/test_api_stores.py` (fixtures/helpers), doc de enlaces y CHANGELOG. Cambios previstos: pasar el texto original desde el CLI; aceptar `raw` keyword-only en la API; en `record_store_link`, decidir por prefijo (`/`, `~`, `$`) y guardar tal cual, o `os.path.relpath` en el resto; expandir en `_resolve_path`/`_linked_stores`; cuatro tests nuevos; doc y línea de CHANGELOG. Dependencias: `api_store`, `HOME` y variable de entorno parcheadas, `$SLDB_TEST_ROOT`; `test_unlink_store.py` debe seguir verde. Validaciones futuras: los tres `pytest` con `TMPDIR=/dev/shm`. Sin ejecutar nada.

## FUTURO

El ejecutor produce `result-summary.md`; el coordinador hace `deskops closeout commit` y no hay push; el aviso a AntonIA se envía o queda como línea en el informe si el repo no está registrado.
