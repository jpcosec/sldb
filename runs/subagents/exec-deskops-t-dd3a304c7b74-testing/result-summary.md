FALLA

# Testing — retiro de `incomplete` del lenguaje de predicados

- Task: `task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato`
- Commit del ejecutor: `22cfafb2c29e62a391d23be53d690a21955fe0ee`
  («Retira incomplete del lenguaje de predicados (inalcanzable con datos reales)», con el trailer `Task-Id` de la tarea).
- Archivos del commit: 20 (código de `api/rules`, `api/where`, lenguaje del grafo, CLI/modelo de reglas,
  tests y docs).
- Log completo: `runs/subagents/exec-deskops-t-dd3a304c7b74-testing/validation.log`.

## Veredicto

**FALLA.** Hay dos motivos, en orden de dureza:

1. **Puerta rápida obligatoria en rojo.** `bash tools/check.sh --fast` termina con **rc 1**: la puerta
   `identidad` rechaza `workbench_demo` («directorio versionado sin clasificar en la raíz»). El
   preflight-2 de la tarea autoriza esa roja preexistente (`f055723d`), pero el prompt del rol es
   explícito: rc distinto de 0 en `--fast` ⇒ FALLA. Las demás puertas (`núcleo aislado`, `capas`,
   `ejes`, `superficie`) pasan. La roja también se reproduce en un worktree limpio del padre
   `25d5bb3f`, así que no la introduce el commit.
2. **El retiro quedó incompleto en la documentación.** El Goal pide retirar `incomplete` del lenguaje,
   de la API **y de la doc**, pero quedan documentos que lo siguen describiendo como vigente:
   - `docs/architecture/graph-backend.md:44` («… e `incomplete` en el borde de links») y líneas 51-52
     (`unavailable` marca un elemento `incomplete`). Contradice directamente
     `docs/architecture/rules-language.md` §3/H4 y el código ya retirado.
   - `knowledge/commands/cmd-sldb-rules-explain.md:10,20` sigue diciendo «exit 0 true, 1 false,
     2 incomplete, 3 not applicable», y `knowledge/symbols/python-sldb-sldb-api-rules-rules_explain-explain_exit.md`
     repite «2 incomplete». `sldb selfdoc check` reporta `knowledge/commands/cmd-sldb-rules-explain.md`
     con alerta `selfdoc/changed` («its generated fields are stale»), aunque su rc sea 0.
3. **Se eliminó un test ajeno al retiro.** El commit borra también
   `tests/api/test_rules.py::test_save_document_payload_returns_the_on_write_alerts_without_a_listener`,
   que no menciona `incomplete`. Lo reconstruí desde el padre y **pasa contra el commit** (1 passed),
   de modo que el borrado no era necesario y reduce cobertura fuera de alcance.

## Validación ejecutada

No existe `/tmp/ws-venv` en este contenedor; usé el Python del venv del repo
(`.venv/bin/python`, Python 3.13.18), con `TMPDIR=/tmp`. Tests de a uno; no se corrió la suite completa.

| Comando (archivo del commit o relacionado al módulo tocado) | Resultado |
|---|---|
| `pytest -q tests/api/test_rules.py` | 12 passed, rc 0 |
| `pytest -q tests/api/test_rules_evaluation.py` | 13 passed, rc 0 |
| `pytest -q tests/test_rules_language_spec.py` | 52 passed, rc 0 |
| `pytest -q tests/test_predicates_cli.py` (Validation) | 4 passed, rc 0 |
| `pytest -q tests/test_clean_code_rules.py` (Validation) | 1235 passed, rc 0 |
| `pytest -q tests/store/test_predicate_language.py` | 16 passed, rc 0 |
| `pytest -q tests/store/test_graph_language.py` | 3 passed, rc 0 |
| `pytest -q tests/store/test_graph_backend.py` | 9 passed, rc 0 |
| `pytest -q tests/store/test_where_empty_and_errors.py` | 25 passed, rc 0 |
| `pytest -q tests/store/test_where_retired.py` | 4 passed, rc 0 |
| `pytest -q tests/api/test_rules_end_to_end.py` | 1 passed, rc 0 |
| `pytest -q tests/api/test_rules_linked_reach.py` | 4 passed, rc 0 |
| `pytest -q tests/api/test_transaction_rules_dirty.py` | 4 passed, rc 0 |
| `PATH=.venv/bin:$PATH TMPDIR=/tmp bash tools/check.sh --fast` | **rc 1**, FAIL solo `identidad` por `workbench_demo` |

No existe `tests/test_<modulo>.py` para los módulos tocados (`fixpoint`, `rule_subjects`, `rules_check`,
`rules_explain`, `where`, `predicate_*`, etc.); corrí los tests de superficie más cercanos, listados
arriba.

## Sobre el test de alcance/retiro

`tests/api/test_rules_evaluation.py::test_a_reference_to_a_linked_store_that_is_gone_is_false_never_incomplete`
arma el caso real en `tmp_path` pedido por el contrato: store enlazado, documento `near` que referencia
`other:X:far`, borrado del store enlazado, índice recompuesto, y evaluación pública con
`where_findings(... include_linked=True)` y `rules_on_check`. Comprueba que no quedan aristas
`unavailable`, que `any` da `false`, `all`/`none`/`count` quedan dentro de `{true,false}`, y que
`rules check` emite un error ordinario `rules/deps`, no `rules/deps/incomplete`. El test pasa en el
commit.

El ejecutor eligió **retirar** y documentó en su `result-summary.md` el grep de productores de
`incomplete` y el intento real fallido, como pedía el preflight-2. La parte de código del retiro es
coherente: `git grep -n incomplete -- src/sldb` ya no encuentra usos del valor del lenguaje.

## Qué falta para poder cerrar

- Actualizar `docs/architecture/graph-backend.md` para que no describa `incomplete` ni
  `metadata.unavailable` como parte de la vista/evaluador vigentes.
- Regenerar la referencia de la CLI (`sldb selfdoc sync` o el mecanismo que corresponda) para
  `cmd-sldb-rules-explain` y la referencia del docstring de `explain_exit`.
- Restaurar `test_save_document_payload_returns_the_on_write_alerts_without_a_listener` en
  `tests/api/test_rules.py` (pasa tal cual contra este commit).
- Si el coordinador acepta formalmente la excepción `identidad`/`workbench_demo` del preflight-2, el
  rc 1 de `--fast` deja de ser bloqueo; los puntos documentales y el test eliminado siguen siendo
  correcciones pendientes antes de cerrar.
