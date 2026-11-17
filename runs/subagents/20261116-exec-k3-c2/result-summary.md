# Resultado: executor deskops-e-fc2bbe7745a8 (corrección 2 de C3 Python)

Task: `task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre`. No hay pills atados.

Motivo de la corrección: la FALLA del tester de la corrección 1 (`runs/subagents/20261116-test-k3-c1/result-summary.md`). `urlpatterns += [...]` y `+= static(...)` se perdían sin aviso. También se cubren sus bordes: la asignación encadenada y lo que queda fuera sin documentar. Se aplicó lo que pide la sección "Precisiones (corrección 2)" del Scope y el mensaje del coordinador.

## Punto de partida
`git apply --exclude=CHANGELOG.md runs/subagents/20261116-exec-k3-c1/executor-diff-c3py-c1.patch`, que contiene el intento 1 y la corrección 1.
- El parche entero no aplicaba en `CHANGELOG.md`, porque HEAD ya trae C4. Esa entrada se reescribió a mano (ver abajo).
- El resto aplicó limpio, también en `tests/selfdoc/test_treesitter_symbols.py`. Los tests de SQL/pglast de C4 siguen ahí y pasan: 45 passed en ese archivo.

## Cambios de esta corrección
- **`src/sldb/code/py_statements.py`**
  - `_read` pasa a llamarse `_reads` y devuelve una lista de `(kind, name, attrs)`.
  - **Asignación aumentada:** un `augmented_assignment` es `assignment` con `attrs.op` (el operador tal cual: `'+='`, `'-='`, …). Su valor se lee con `value_attrs`, igual que con `=`. Así, `urlpatterns += [path(...), path(...)]` da `items` y `+= static(...)` da `call`.
  - **Asignación encadenada:** la función nueva `_chain` recorre `a = b = valor` y devuelve los destinos de izquierda a derecha y el valor. Sale un fact por cada destino que es un nombre, todos con el mismo valor.
  - Un destino que no es un nombre (`obj.attr`, `p, q`, `x[0]`) no da fact. Dentro de una cadena solo se omite ese destino.
  - `statement_facts` hace `extend` sobre `_reads`. La constante nueva es `_ASSIGNMENTS`.
  - El docstring del módulo documenta `attrs.op`, la cadena y lo que no da fact: un destino que no es nombre, una anotación sin valor (`y: int`), una expresión que no es llamada y lo que está bajo `if`/`for`/`with`/`try`/`def`.
  - Los ids siguen tardíos (`take_late`). Un segundo `urlpatterns` en el mismo módulo es `urlpatterns~2`, `~3`.
- **`tests/selfdoc/test_treesitter_symbols.py`**
  - `test_statements_and_calls_edge_cases`: ahora `a = b = 2` da `mod.a` y `mod.b`. Se actualizaron la lista esperada y el mensaje.
  - Fixture nuevo `urls` (fuente `URLS`) y tres tests nuevos:
    - `test_an_augmented_list_assignment_gives_its_items_and_its_operator`: `urlpatterns += [path("b/", b), path("c/", c)]` da `{op: '+=', items: [...]}`, con `native_kind: augmented_assignment`, su span y `contained-in`. El `=` inicial no lleva `op`.
    - `test_an_augmented_call_assignment_gives_its_call_and_any_operator_is_kept`: `urlpatterns += static(settings.MEDIA_URL, document_root=...)` da `{op: '+=', call: {...}}`, y `count -= 1` da `{op: '-=', value: '1'}`.
    - `test_a_chained_assignment_gives_one_fact_per_name_with_the_same_value`: `created = updated = models.DateTimeField(auto_now=True)` en una clase da `Post.created` y `Post.updated` con la misma `call`. `x = obj.attr = y = 3` da solo `x` e `y`. `p, q = f()` y `z: int` no dan fact.
- **`CHANGELOG.md`:** la entrada de 0.1.13 de esta tarea se reescribió a mano y va primera en la sección. Es la de la corrección 1 más `+=`/`attrs.op`, la cadena y la lista de lo que no da fact.
- Del parche de partida, sin cambios en esta corrección: `src/sldb/code/ids.py`, `scan.py`, `py_calls.py`, `py_module.py`, `src/sldb/api/code/code_facts.py`, `tests/selfdoc/test_treesitter_agreement.py` y el fixture `tests/fixtures/treesitter/blog_app/`.

## Done When
- **Validation:** los 7 comandos dan rc=0 (`validation.log`).
- **Fixture blog_app:** cubre las bases, `@action` con sus argumentos, handler -> `post.publish` -> `can_publish`, los campos como `assignment` con su llamada, `Meta.db_table`, `Meta.model` y `Meta.fields`, `path()` y `router.register()`. Lo prueban los tests `test_blog_*`, que pasan.
- **Las anclas existentes no cambian de estado:**
  - `NORMALIZATION` sigue en 1 y las huellas de las definiciones no se tocan.
  - Comprobación extra en `validation.log`: los ids de todos los facts que no son `assignment`/`call` son idénticos con y sin los kinds nuevos en `src/sldb` (5707), `blog_app` (35, con los de SQL) y `pytree` (28).
  - No queda ningún id None.
- **CHANGELOG:** hecho.
- **Commit y aviso a IR:** no hechos, por instrucción del coordinador.

## Comandos (todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)
| Comando | Resultado | rc |
|---|---|---|
| `pytest -q tests/selfdoc/test_treesitter_symbols.py` | 45 passed | 0 |
| `pytest -q tests/selfdoc/test_treesitter_agreement.py` | 2 passed | 0 |
| `pytest -q tests/selfdoc/test_fingerprints.py` | 4 passed | 0 |
| `pytest -q tests/notations/test_component_spec_python.py` | 5 passed | 0 |
| `pytest -q tests/api/test_anchors.py` | 23 passed | 0 |
| `pytest -q tests/test_clean_code_rules.py` | 1201 passed | 0 |
| `bash tools/check.sh --fast` | — | 0 |
| extra: comparación de ids de facts existentes | — | 0 |

`uv` funcionó y no hizo falta el plan B. Ni la suite completa ni `sldb stores build --check` figuran en Validation; los corre el integrador.

## Archivos tocados (todos los del diff de esta tarea)
- **Modificados:** `CHANGELOG.md`, `src/sldb/api/code/code_facts.py`, `src/sldb/code/ids.py`, `src/sldb/code/scan.py`, `tests/selfdoc/test_treesitter_agreement.py`, `tests/selfdoc/test_treesitter_symbols.py`.
- **Nuevos:** `src/sldb/code/py_calls.py`, `src/sldb/code/py_module.py`, `src/sldb/code/py_statements.py`, `tests/fixtures/treesitter/blog_app/` (13 archivos).
- **Run dir:** `validation.log`, `result-summary.md` y `executor-diff-c3py-c2.patch`, que es el diff completo de la tarea con los archivos nuevos incluidos.
- No se tocaron los cambios ajenos (`.sldb/`, `desk/runtimes/`, `uv.lock`, etc.) y no se hizo stage de nada.

## Desvíos y dudas
- `ids.py`, `code_facts.py`, `test_treesitter_agreement.py`, `py_*.py` y el fixture quedan fuera de la lista `files`. Vienen del parche de partida, que el coordinador declara de esta tarea; el Implementation Path autoriza los módulos nuevos. `readers.py` no cambia.
- Una cadena comparte el mismo dict de valor entre sus facts (`attrs` es un dict nuevo por fact, pero `items`/`call` son los mismos objetos). No afecta al JSON. Si un consumidor muta un fact en sitio, vería el cambio también en el otro.
- No se tocaron los límites que el tester clasificó como documentados u observación: `[...] + router.urls` da `value` con su texto, y `py_norm` no normaliza los prefijos `r"..."`.
