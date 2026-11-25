## REFORMULACION

Encargo ejecutable sobre el repo SLDB_1: hacer que `sldb stores add <ruta>` conserve el texto original cuando empieza por `/`, `~` (incl. `~user`) o `$` (`$VAR`/`${VAR}`), y lo guarde relativo a la raíz del proyecto en cualquier otro caso (comportamiento actual). La lectura (`_resolve_path`/`_linked_stores` en `src/sldb/store/query.py`) debe aplicar `os.path.expandvars` y `os.path.expanduser` antes de resolver. Resultado: cambios en `src/sldb/api/stores/link_store.py`, `src/sldb/store/query.py`, el comando `stores add` en `src/sldb/cli/commands/`, tests nuevos en `tests/api/test_api_stores.py`, actualización de `docs/architecture/store-declaration.md` y una línea en `CHANGELOG.md` bajo `## 0.1.13 — not released yet`. Límites: no resolver contra el git common dir, no migrar enlaces ya guardados, no push (commit lo hace el coordinador con `deskops closeout commit`).

## AMBIGUEDADES

1. "la función de API a la que llama; se agrega un parámetro keyword-only raw: str | None = None" — no nombra la función; obligaría a inventar cuál recibe `raw` si hay envoltorios.
2. "la sección de enlaces o links" en `docs/architecture/store-declaration.md` — no fija encabezado exacto; obligaría a inventar el título de sección.
3. "con el estilo de las entradas vecinas" (CHANGELOG) — exige inspeccionar vecinas; si no existieran, obligaría a inventar formato.
4. "deskops message send --to <repo>" / "aviso a AntonIA con deskops message send --to AntonIA" — no aclara el identificador exacto del repo; obligaría a inventar el literal.
5. "los números de línea citados son orientativos a HEAD 7288d93e" — el HEAD real no se da; obligaría a asumir que coincide.

## DRY-RUN

Lecturas: `link_store.py` (`record_store_link`), comando `stores add` (grep `record_store_link|link_store` en `src/sldb/cli`), `query.py:100-120`, `tests/api/test_api_stores.py` (fixtures), docs y CHANGELOG. Cambios previstos: parámetro `raw` keyword-only propagado desde CLI; regla de prefijo sobre `raw`; expansión `~`/vars al leer; cuatro tests; doc y CHANGELOG. Dependencias: `deskops message send`/registro de AntonIA y commit del coordinador. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/api/test_api_stores.py`, `tests/api/test_unlink_store.py`, `tests/store/test_stores_build.py`. Nada ejecutado.

## FUTURO

El coordinador ejecuta `deskops closeout commit`, envía el aviso y cierra. Un humano decide el fallback si AntonIA no está registrada (línea "Aviso a AntonIA" en `runs/subagents/<run-dir>/result-summary.md`).
