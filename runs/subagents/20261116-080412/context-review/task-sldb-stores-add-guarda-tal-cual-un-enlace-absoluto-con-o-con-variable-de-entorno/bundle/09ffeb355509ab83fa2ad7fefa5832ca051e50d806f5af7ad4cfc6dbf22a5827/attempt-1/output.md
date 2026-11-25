## REFORMULACION

Propósito: que `sldb stores add <ruta>` conserve el enlace tal como lo escribió el usuario cuando empieza por `/`, `~` o `$`, y lo guarde relativo a la raíz del proyecto en el resto de casos; la lectura debe expandir `~` y variables de entorno. Resultado: cambio en `link_store`/`record_store_link` (parámetro keyword-only `raw`), expansión en `_linked_stores`, tests nuevos, entrada de CHANGELOG y actualización de `docs/architecture/store-declaration.md`. Repo: sldb, HEAD 7288d93e. Límites: no resolver contra el git common dir, no migrar enlaces existentes, no push; superficie acotada a los archivos y comandos nombrados.

## AMBIGUEDADES

1. «la función de API a la que llama» — no nombra la firma que recibe `raw`; obligaría a inventar si es `link_store` o `record_store_link`. El pill la fija en `link_store`.
2. «la sección de enlaces en docs/ (grep "stores add" docs/)» frente a «docs/architecture/store-declaration.md» — dos ubicaciones posibles; sin la precisión habría que inventar cuál editar.

## DRY-RUN

Lecturas: `src/sldb/api/stores/link_store.py`, `src/sldb/cli/commands/store_add.py` (localizado por grep), `src/sldb/store/query.py` (100-120), `tests/api/test_api_stores.py`, `tests/api/test_unlink_store.py`, CHANGELOG y doc de store-declaration. Cambios previstos: añadir `raw` keyword-only y propagarlo; decidir prefijo sobre el texto original; guardar `raw` sin expandir; en `_linked_stores` expandir `os.path.expandvars(os.path.expanduser(...))` solo para resolver/validar; tests de los cuatro casos; CHANGELOG bajo «## 0.1.13 — not released yet». Dependencias: fixtures/helpers existentes del archivo de test; `HOME` y `SLDB_TEST_ROOT` parcheados. Validaciones futuras: los tres comandos pytest indicados, más `stores check`, `tools/check.sh` y `tools/check_claims.py` si aplica por tocar store/docs. Nada se ejecuta aquí.

## FUTURO

El ejecutor produce `runs/subagents/<run-dir>/result-summary.md` con cambios y commit; el coordinador hace `deskops closeout commit` con el título corto y decide el cierre; el aviso a AntonIA se envía con `deskops message send --to AntonIA` o, si el repo no está registrado, queda como línea «Aviso a AntonIA» en el informe. El humano valida el resultado conjunto y el commit.
