# Resultado — executor deskops-e-e737091e8bcb-a2 (corrección 1 de C3 Python)

Task: `task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre`.
Pills: ninguno. El motivo de la corrección es la FALLA del tester (`runs/subagents/20261116-test-k3/result-summary.md`): un `x = 1` en `pkg/__init__.py` le quitaba el id `pkg.x` al módulo `pkg/x.py`. La regla aplicada viene del coordinador: los facts existentes (module, class, function, method) conservan siempre el id de HEAD; `assignment` y `call` toman su id en una segunda pasada sobre todo el árbol y, si chocan, son ellos los que llevan `~N`.

## Cambios de esta corrección (sobre el diff del intento 1, que sigue en el árbol)

- `src/sldb/code/ids.py`, clase `Ids`:
  - `take_late(candidate, fact)` encola un fact con `id` None.
  - `flush(facts=None)` es la segunda pasada: da los ids en orden de cola, después de todos los `take`, y devuelve `facts`.
  - Docstring del módulo actualizado.
- `src/sldb/code/py_statements.py`, `_fact`: usa `idgen.take_late(...)` en vez de `idgen.take(...)`. Docstring actualizado.
- `src/sldb/code/scan.py`:
  - `scan_tree` llama a `idgen.flush(facts)` antes de ordenar.
  - `scan_file`: sin `idgen`, crea uno, se llama a sí mismo y hace `flush` antes de devolver (`record_anchor` sigue recibiendo ids completos). Con el `idgen` del llamador, los ids de las sentencias esperan al `flush` del llamador.
  - El cuerpo de Python pasa a `_scan_python`, por la regla de 10 líneas.
  - `_module_fact` sale a `src/sldb/code/py_module.py` como `module_fact`, sin cambios, por la regla de 80 líneas. `scan.py` queda en 79 líneas efectivas.
  - Docstring del módulo compactado.
- `src/sldb/api/code/code_facts.py`, `code_facts`: envuelve la lista en `idgen.flush(...)`. Lo pide la regla del coordinador ("en scan_tree y también en code_facts").
- `tests/selfdoc/test_treesitter_symbols.py`, dos tests nuevos y un helper `_clashing_tree`:
  - `test_a_module_assignment_named_like_a_sibling_module_does_not_take_its_id`: el caso del tester, por `scan_tree` y por `code_facts`. Comprueba que `pkg.x` es el módulo, que `pkg.x.f` está contenido en `pkg.x` y que la asignación es `pkg.x~2`. Comprueba también que `scan_file` sin `idgen` da los ids.
  - `test_with_clashes_existing_ids_are_those_of_a_scan_without_the_new_kinds`: un árbol con choques (asignación frente a módulo hermano, llamada de módulo frente a módulo hermano, atributo de clase frente a método). Compara los ids de module, class, function y method de `scan_tree` y de `code_facts` con un escaneo que no emite los kinds nuevos (`statement_facts` parcheado a `[]`): son idénticos. Comprueba además que los nuevos llevan `~2`.
- `CHANGELOG.md`: la entrada de 0.1.13 describe la segunda pasada, el ejemplo `pkg.x~2` y el traslado a `py_module.py`.

## Done When
- Validation: los 7 comandos con rc=0 (`validation.log`).
- Los puntos del fixture blog_app siguen cubiertos por los tests del intento 1, que pasan.
- Las anclas existentes no cambian de estado. Las huellas y `NORMALIZATION` no se tocan. Los ids de los facts existentes son idénticos a HEAD en `/dev/shm/k3t-edge/t`, blog_app, pytree y `src/sldb` (5674 facts); ver `validation.log`.
- CHANGELOG: hecho.
- Commit y aviso a IR: no hechos, por instrucción del coordinador.

## Comandos (todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)
| Comando | rc |
|---|---|
| pytest -q tests/selfdoc/test_treesitter_symbols.py (24 passed) | 0 |
| pytest -q tests/selfdoc/test_treesitter_agreement.py | 0 |
| pytest -q tests/selfdoc/test_fingerprints.py | 0 |
| pytest -q tests/notations/test_component_spec_python.py | 0 |
| pytest -q tests/api/test_anchors.py | 0 |
| pytest -q tests/test_clean_code_rules.py | 0 |
| bash tools/check.sh --fast | 0 |
| extra: pytest -q tests/api/test_doc_anchors.py | 0 |

La suite completa y `sldb stores build --check` quedan delegadas al integrador. `tests/api/test_code_facts.py` no existe (rc=4 en el log): fue un intento extra mío y no forma parte de Validation.

## Archivos tocados en esta corrección
- `src/sldb/code/ids.py` (M). Desvío: no está en la lista de archivos del contrato. Hacía falta para la segunda pasada que pide la regla del coordinador.
- `src/sldb/api/code/code_facts.py` (M). Desvío: autorizado de forma explícita por la regla del coordinador.
- `src/sldb/code/py_module.py` (nuevo). Lo cubre el Implementation Path (módulos nuevos del paquete por la regla de 80 líneas).
- `src/sldb/code/scan.py` (M), `src/sldb/code/py_statements.py` (nuevo desde el intento 1, M).
- `tests/selfdoc/test_treesitter_symbols.py` (M) y `CHANGELOG.md` (M).
- `runs/subagents/20261116-exec-k3-c1/{validation.log,result-summary.md}`.

## Dudas
- Entre los facts tardíos, `~N` sigue el orden de cola: archivos en el orden de `find_files` y, dentro de cada archivo, el orden de fuente. El `id` de un fact tardío es None hasta el `flush`. Quien llame a `scan_file` con su propio `Ids` y no haga `flush` verá None; dentro de `src/` solo lo hacen `scan_tree` y `code_facts`, y los dos hacen `flush`.
