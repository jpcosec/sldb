# result-summary — deskops-e-ddef8b98ace9 (task-ci-el-test-de-graph-path-explicado-…)

## Qué cambié
Archivo único: `tests/api/test_api_graph_analysis.py`.
- `MODELS`: se añade una segunda clase `Card` (`__references__ = ["about"]`) al módulo de modelos del test. AnalysisWorld solo registra `Spec`, así que los demás tests no la ven.
- Se elimina `test_explain_over_the_repo_own_index_names_origin_and_relation_doc` (leía el `.sldb` del repo y dependía de `.sldb_cache`).
- Se añade `test_explain_names_origin_and_relation_doc_or_field_over_a_store_built_in_tmp(world)`: sobre el AnalysisWorld en tmp_path registra `Card` con `api.add_model`, crea `Card:c1` con `about: Spec:s3` y pide `graph_path(Card:c1 → Spec:s1, relations=["references","refines"], explain=True, include_linked=False)`. Comprueba: los orígenes son exactamente {schema, relation_doc}; la primera arista es `{origin: schema, field: about}` y las siguientes `_refines("s3-s2")`, `_refines("s2-s1")`; y la misma propiedad del test original (cada arista trae origin y relation_doc o field).

## Por qué un fixture extra (aclaración 1 del coordinador)
AnalysisWorld ya tenía aristas `relation_doc` (refines), pero sus aristas `schema` (has_field, extends, applies_to_*) no llevan `field`, así que no cubren la propiedad "relation_doc o field". Se añadió lo mínimo: un modelo con una referencia declarada, que produce `references` con `origin: schema, field: about`.
Nota: `references` no es relación "authored" por defecto en el análisis, por eso el test pasa `relations=["references","refines"]` explícito. No se tocó src/.

## Done When
- Comandos de Validation: los tres con rc 0 (ver validation.log): test file 10 passed; clean_code_rules 1177 passed; `tools/check.sh --fast` TODAS LAS PUERTAS PASAN.
- Clon limpio: `git clone` del checkout a /dev/shm/ci1-clon (copiado encima solo el test modificado, aún sin commit), sin `.sldb_cache` (verificado: no existe), XDG_CACHE_HOME=/dev/shm/ci1-xdg vacío, `uv run --frozen --extra code --extra dev pytest -q -p no:cacheprovider tests/api/test_api_graph_analysis.py` → rc 0. Salida abajo.
- Commit: no lo hago (aclaración 5: lo hace el coordinador).

## Comandos y rc
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py` → rc 0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` → rc 0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` → rc 0
- En el clon: `XDG_CACHE_HOME=/dev/shm/ci1-xdg TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q -p no:cacheprovider tests/api/test_api_graph_analysis.py` → rc 0
- No se corrió la suite completa ni `sldb stores build --check` (no figuran en Validation; delegados al integrador).

## Archivos tocados
- tests/api/test_api_graph_analysis.py
- runs/subagents/20261116-exec-ci1/validation.log, result-summary.md (entrega)
Clon /dev/shm/ci1-clon y /dev/shm/ci1-xdg borrados al terminar.

## Salida en el clon limpio
```
Using CPython 3.13.18
Creating virtual environment at: .venv
   Building structuredlanguagedb @ file:///dev/shm/ci1-clon
      Built structuredlanguagedb @ file:///dev/shm/ci1-clon
warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 28 packages in 172ms
..........                                                               [100%]
=============================== warnings summary ===============================
.venv/lib/python3.13/site-packages/_pytest/config/__init__.py:1464
  /dev/shm/ci1-clon/.venv/lib/python3.13/site-packages/_pytest/config/__init__.py:1464: PytestConfigWarning: Unknown config option: asyncio_default_fixture_loop_scope
  
    self._warn_or_fail_if_strict(f"Unknown config option: {key}\n")

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
10 passed, 1 warning in 7.51s
rc=0
```
