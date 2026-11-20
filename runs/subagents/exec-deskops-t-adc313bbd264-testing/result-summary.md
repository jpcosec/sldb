FALLA

# Testing — `sldb stores add` guarda tal cual `/`, `~` y `$VAR`

Commit verificado: `94d9f554f4f68556bb8d011046ccb72dccceafb2`
("sldb stores add guarda tal cual un enlace absoluto, con ~ o con variable de entorno",
con `Task-Id: task-sldb-stores-add-guarda-tal-cual-un-enlace-absoluto-con-o-con-variable-de-entorno`).
HEAD al probar: `130f2330`; `git diff 94d9f554..HEAD -- src tests CHANGELOG.md docs` está vacío.

## Veredicto

**FALLA por la puerta rápida obligatoria.** `bash tools/check.sh --fast` termina con **rc 1**
porque la puerta `identidad` rechaza el directorio versionado `workbench_demo`
("directorio versionado sin clasificar en la raíz"). La regla del rol es explícita: rc distinto
de 0 en `check.sh --fast` ⇒ FALLA. Las demás puertas (`núcleo aislado`, `capas`, `ejes`,
`superficie`) pasan.

La roja es **preexistente y ajena a este commit**. La reproduje en un worktree limpio del padre
`94d9f554^` (`eb42a49e`), fuera del árbol sucio de trabajo:

    cd /tmp/sldb-parent-check   # worktree --detach 94d9f554^
    PATH=/mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin:$PATH bash tools/check.sh --fast
    FAIL: identidad — ... 1 violaciones
    rc=1

`workbench_demo` entró versionado en `562847e2`, anterior al commit del ejecutor;
`contracts/identity.toml` no lo clasifica. El commit no toca ni ese directorio ni el contrato
de identidad.

**Veredicto funcional: PASA.** No encontré un defecto en el comportamiento pedido: los tres
comandos de Validation pasan, los cuatro casos nuevos existen y discriminan (fallan con el código
padre), y CHANGELOG/doc están. Si el coordinador acepta formalmente la roja preexistente de
`identidad` como excepción, no veo nada que impida cerrar la tarea.

Nota de entorno: `/tmp/ws-venv` no existe en este contenedor; usé el venv real del repo
(`/mnt/ssd/proyectos/SLDB_1/sldb/.venv`, Python 3.13).

## Comandos de Validation

Salida completa en `validation.log` (de a un archivo, `TMPDIR=/dev/shm`, `-p no:cacheprovider`).

| Comando | rc | Resultado |
|---|---:|---|
| `pytest -q tests/api/test_api_stores.py` | 0 | **18 passed** |
| `pytest -q tests/api/test_unlink_store.py` | 0 | **5 passed** |
| `pytest -q tests/store/test_stores_build.py` | 0 | **35 passed** |

Los tres pasan.

## Tests nuevos: existen y discriminan

Los cuatro casos de `tests/api/test_api_stores.py`:

- `test_stores_add_keeps_an_absolute_path_absolute`: guarda `str(other)` y `_linked_stores` lo resuelve.
- `test_stores_add_keeps_a_home_path_as_written_and_reads_it_with_home`: guarda `~/other/.sldb` y lo resuelve con `HOME` parcheado.
- `test_stores_add_keeps_a_variable_path_as_written_and_reads_it_with_the_variable`: guarda `$SLDB_TEST_ROOT/...` y `${...}`, lee con la variable puesta, y `stores remove` funciona.
- `test_stores_add_keeps_a_relative_path_relative_to_the_root`: sigue guardando relativo a la raíz.

Comprobación contra el código padre (`/tmp/sldb-parent-check`, copiando el test nuevo al worktree
de `94d9f554^`), en `pytest-new-tests-on-parent.log`:

    test_stores_add_keeps_an_absolute_path_absolute                                   FAILED
    test_stores_add_keeps_a_home_path_as_written_and_reads_it_with_home               FAILED
    test_stores_add_keeps_a_variable_path_as_written_and_reads_it_with_the_variable   FAILED
    test_stores_add_keeps_a_relative_path_relative_to_the_root                        passed
    3 failed, 1 passed

Es lo esperado: los tres casos nuevos fallan con la implementación vieja y pasan con la nueva;
el relativo pasaba antes y sigue pasando.

## Regresiones vecinas y limpieza

Salida en `regressions.log`:

| Comando | rc | Resultado |
|---|---:|---|
| `pytest tests/store/test_cli_store.py tests/store/test_export_contract_frozen.py tests/store/test_store_context_audit.py` | 0 | **44 passed** |
| `test_clean_code_rules` sobre `link_store.py`, `store_add.py` y `store/query.py` | 0 | **3 passed** |

No corrí la suite completa; queda para el host, como pide el rol.

## Revisión del contrato

- **Guardar según el texto original:** `link_store(..., raw=...)` recibe el texto del comando;
  `kept_as_written` decide por los prefijos `/`, `~`, `$` y `record_store_link` guarda `raw` tal
  cual o el `relpath` de siempre. El CLI `src/sldb/cli/commands/store_add.py` pasa
  `raw=str(args.path)`. PASA.
- **Validar con la ruta expandida, guardar sin expandir:** `link_store` resuelve
  `os.path.expandvars(os.path.expanduser(raw))` para `_check_other_exists`/`_check_not_self`;
  lo que se persiste es `raw`. Es lo que fija el pill. PASA.
- **Leer expandiendo `~` y variables:** `_linked_stores` aplica `expandvars`/`expanduser` antes de
  `_resolve_path`; no se amplió `_resolve_path` general. PASA.
- **`stores remove` y `stores add --replace` con las tres formas:** cubiertos por el test de
  variable; `unlink_store` opera por nombre y los 5 tests siguen verdes. PASA.
- **CHANGELOG:** una línea en español bajo `## 0.1.13 — not released yet`, al estilo de las
  vecinas. PASA.
- **Doc:** sección "Links: how `sldb stores add` records the path" en
  `docs/architecture/store-declaration.md` (el archivo que fija Precisiones). PASA.

## Observaciones (no bloquean el comportamiento)

- `tests/store/test_stores_build.py` no está en la lista `files` del contrato, pero el ejecutor
  cambió tres llamadas de `stores add` de ruta absoluta a `os.path.relpath(...)`. Es necesario
  para que esos tests sigan comprobando el enlace relativo que declaran (`../../../owner/.sldb`)
  bajo el contrato nuevo; no se debilitó la aserción del camino ni la comprobación de que el
  enlace se alcanza. Lo anoto porque es un archivo de test fuera de la lista.
- La roja de `identidad` por `workbench_demo` es el único motivo del FALLA formal; requiere una
  decisión aparte sobre la clasificación del directorio.

## Evidencia en este directorio

- `validation.log` — los tres comandos de Validation.
- `check-fast.log` — `check.sh --fast` en el commit (rc=1, solo `identidad`).
- `check-fast-parent.log` — la misma puerta en `94d9f554^` (rc=1, misma roja; preexistente).
- `pytest-new-tests-on-parent.log` — los tests nuevos contra el código padre (3 failed, 1 passed).
- `regressions.log` — tests vecinos y clean code de los módulos tocados.
