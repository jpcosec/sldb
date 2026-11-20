FALLA

# Testing — stores check: documentos generados ausentes como alerta

## Veredicto

**FALLA por la puerta rápida obligatoria.** `bash tools/check.sh --fast` termina con **rc 1** porque la
puerta `identidad` rechaza el directorio versionado `workbench_demo` ("directorio versionado sin
clasificar en la raíz"). La regla del rol de testing es explícita: rc distinto de 0 en
`check.sh --fast` ⇒ FALLA. Las demás puertas (`núcleo aislado`, `capas`, `ejes`, `superficie`) pasan.

La roja es **preexistente y ajena a esta tarea**: `workbench_demo` ya está versionado antes del commit
del ejecutor y `contracts/identity.toml` no lo clasifica. La reproduje también en un clon limpio de
HEAD, sin el árbol sucio de trabajo. Además, el propio informe del ejecutor
(`runs/subagents/exec-deskops-e-ddbd371d217b/result-summary.md`) la registra y el coordinador autorizó
commitear con ella.

**Veredicto funcional: PASA.** El comportamiento pedido está implementado y los dos comandos de
validación del contrato pasan. Si el coordinador acepta formalmente la roja preexistente de
`identidad` como excepción, no encontré un defecto que impida cerrar la tarea.

## Dónde está el trabajo

- Commit con el trailer de la tarea: `07450d10542ba9b884149c1cea928ff8e582adfc`
  (`stores check reporta los documentos generados ausentes como una alerta (CHANGELOG)`), pero
  `git show --name-only` solo lista `CHANGELOG.md`: es el commit de la línea del CHANGELOG.
- El código y el test efectivos están en `0f91540dfbaee9a0eae95b2c0a20b71db0ad1d78` (commit de otra
  tarea que arrastró el índice compartido; ya reportado por el ejecutor). Archivos efectivos:
  - `src/sldb/store/diagnostics.py`
  - `src/sldb/store/diagnostics_models/model_diagnosis.py`
  - `src/sldb/api/stores/store_findings.py`
  - `src/sldb/api/stores/store_check.py`
  - `src/sldb/cli/commands/store_check.py`
  - `src/sldb/cli/serve/stores_check.py`, `src/sldb/cli/serve/lint_routes.py`
  - `tests/store/test_diagnostics.py`, `CHANGELOG.md`
- HEAD al probar: `eb42a49e`. Los archivos de `src/` y `tests/` de esta tarea no cambiaron después de
  `0f91540d`.

## Revisión del comportamiento

- `diagnose_store(..., derived=())` recibe los prefijos declarados; `_is_generated_missing` compara por
  componentes de ruta (`Path(doc.path).parts`), no por texto, y exige que el documento no exista.
- Los documentos bajo un prefijo `derived` ausentes se excluyen del diagnóstico y se cuentan en
  `ModelDiagnosis.generated_missing`.
- `_generated_missing` emite una sola alerta `store/generated-missing` por modelo con sujeto el modelo y
  el texto del Goal, usando `alert()` de `sldb.core.finding`; sin `generated_missing` no emite nada.
- Los ausentes fuera de `derived` siguen siendo `store/missing` (error) y por tanto el exit code depende
  solo de esos errores.
- `derived_prefixes()` lee `StoreDeclaration.derived`; si no hay declaración legible devuelve `[]`.
- El test nuevo arma `derived: [gen/]`, 3 ausentes bajo `gen/` y 1 `genx.md` ausente fuera: espera una
  alerta que dice 3, un solo `store/missing` y que este sea de nivel error.

## Tests ejecutados (de a uno, con `TMPDIR=/tmp` y el Python 3.13.18 del `.venv`)

| Comando | rc | Resultado |
|---|---|---|
| `pytest -q tests/store/test_diagnostics.py` | 0 | 17 passed |
| `pytest -q tests/test_serve_stores_check.py` | 0 | 2 passed |

No existe un `tests/test_<modulo>.py` específico para `store_findings`, `model_diagnosis` ni para el
comando CLI `store_check`; la cobertura aplicable es la de los dos archivos anteriores.

## Clon limpio sin build (`/dev/shm/sldb-tester-check`, clon de HEAD)

- `sldb stores check --store .sldb` → **rc 1**.
  - **0 errores de `PythonSymbolDoc`** (antes eran 2453).
  - Una alerta: `alert: [store/generated-missing] PythonSymbolDoc: 2540 PythonSymbolDoc documents are
    generated and not on disk: run \`sldb stores build\``.
  - Quedan 75 errores ajenos (mayormente documentos `InboxNoteDoc` trackeados ausentes y modelos de
    deskops no importables en el clon, `store/model-unresolved`), por eso el rc no es 0. El contrato
    solo exige 0 errores de PythonSymbolDoc y que el rc dependa de los errores reales.
- `sldb stores build` → **rc 1**, `Unexpected: [Errno 2] No such file or directory:
  '.../knowledge/symbols/python-sldb-sldb-api-actor-set_actor.md'` porque `knowledge/symbols/` no existe
  en el clon. El ejecutor ya lo anotó como fallo de python-sync fuera de alcance; al crear el
  directorio el build pasa a ejecutarse pero supera el presupuesto de esta prueba (>20 min), así que no
  lo usé como evidencia.
- `sldb selfdoc check` (tras el build fallido) → **rc 0**; líneas con estado changed:
  - `"changed": ["knowledge/commands/cmd-sldb-notations-from-graph.md"]`
  - alerta `selfdoc/changed` sobre ese documento ("its generated fields are stale").
  Esa línea corresponde a la tarea de `notations from-graph` también presente en HEAD, no a este cambio.

## Puerta rápida del desk

    PATH=/workspace/sldb/.venv/bin:$PATH bash tools/check.sh --fast   -> rc 1

    PASS: núcleo aislado
    PASS: capas
    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"
    PASS: ejes
    PASS: superficie

La misma falla aparece en el clon limpio de HEAD, sin los cambios sin commitear del árbol compartido.
No proviene de esta tarea y no hay otra puerta en rojo.
