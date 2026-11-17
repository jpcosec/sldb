# Tester deskops-t-e9903b561d98: corrección 2 de C3 Python

Task: `task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre` (sin pills).

**Veredicto: PASA.** La FALLA de la corrección 1 (`urlpatterns += [...]` / `+= static(...)` perdidos sin aviso) está resuelta. Los facts existentes siguen idénticos a HEAD en todos los árboles y choques. Los tests de SQL/pglast de C4 pasan, y spec, selfdoc y store no cambian. Salida completa en `validation.log`; scripts y árboles en `/dev/shm/k3t3/`.

## Validation (corrida propia, `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)
| Comando | Resultado |
|---|---|
| pytest -q tests/selfdoc/test_treesitter_symbols.py | PASA, 45 passed |
| pytest -q tests/selfdoc/test_treesitter_agreement.py | PASA, 2 passed |
| pytest -q tests/selfdoc/test_fingerprints.py | PASA, 4 passed |
| pytest -q tests/notations/test_component_spec_python.py | PASA, 5 passed |
| pytest -q tests/api/test_anchors.py | PASA, 23 passed |
| pytest -q tests/test_clean_code_rules.py | PASA, 1201 passed |
| bash tools/check.sh --fast | PASA, rc=0 |

`uv` funcionó sin necesitar el plan B. La suite completa y `sldb stores build --check` no figuran en Validation; quedan delegadas al integrador.

**Regresiones vecinas.** Los tests que importan `sldb.code` o `sldb.api.code` son `test_anchors`, `test_component_spec_python`, `test_fingerprints`, `test_treesitter_agreement` y `test_treesitter_symbols`. Son los mismos de Validation y todos pasan.

## (1) Sondas de los testers anteriores: PASA
`probe.py`/`cmp.py` de c1 corridos con el `src` de HEAD (`git archive` en `/dev/shm/k3t3/head`) y con el del árbol. Los árboles de choque de c1 ya no existían en /dev/shm y los recreé: clash, callsub, attr, nested y rootinit. Añadí cuatro árboles nuevos: aug, chain, dj y trees2.

- **15 árboles, todos OK.** Facts module/class/function/method idénticos, con id, `contained-in` y huellas. Los ids de `scan_file` por archivo y `record_anchor` también son iguales a HEAD. `code_facts` da lo mismo que `scan_tree` y no queda ningún id None. Los árboles: `src/sldb` (5707), blog_app, frontend, pytree, pytree_ts, sql, `k3t-edge/t` y los 8 de choque.
- **Kinds TS y SQL:** idénticos a HEAD (blog_app 9, frontend 9, sql 41).
- **Choques:** en cada choque el fact existente conserva su id y el nuevo lleva el `~N`.
  - `pkg.x~2`, `pkg.y~2`, `m.A.foo~2`, `m.main~2`/`~3`, `a.b~2`, `a.b.c~2`, `z~2`, como en c1.
  - Nuevos con `+=`: `pkg.x~2` (`x += 1` frente a `pkg/x.py`) y `pkg.k~2` (`k -= f()` frente a `def k`).
  - Nuevos con cadena: `m.A.a~2`/`m.A.b~2` (`a = b = 1` frente a los métodos `a` y `b`) y `m.c~2` (`c = d = make()` frente a `def c`).
- **`urlpatterns += [path(...), path(...)]`:** da `urlpatterns~2` con `op: '+='` y dos `items` `{func: path, ...}`. `+= static(...)` da `urlpatterns~3` con `call`.

## (2) Precisiones de corrección 2: PASA
- **Operadores aumentados:** `+=`, `-=`, `*=` y `|=` dan cada uno un `assignment` con `attrs.op` y su valor (`call`, `items` o `value`), también en una `Meta` anidada (`ordering += ["-id"]`). El `=` normal no lleva `op`.
- **Asignación encadenada:**
  - `created = updated = models.DateTimeField(auto_now=True)` da `Post.created` y `Post.updated` con la misma `call`.
  - `x = obj.attr = y = 3` da solo `x` e `y`.
  - `p, q = f()` y `tags: list` no dan fact, como dice el docstring.
- **Ids tardíos:** con `take_late` y `flush` en `scan_tree`, `scan_file` y `code_facts`, como pide (1) de la corrección 2.
- **Docstring de `py_statements.py`:** documenta `op`, la cadena y lo que no da fact.

## (3) SQL/pglast de C4: PASA
`test_treesitter_symbols.py` solo añade líneas frente a HEAD: +195, sin borrar ningún test (comparé los nombres `def test_*` de HEAD con los actuales). `-k 'sql or pg or postgres'` da 10 passed, y el archivo entero 45 passed.

## (4) Spec, selfdoc y store: PASA
Hice dos copias completas del árbol en `/dev/shm/k3t3/store-{old,new}` (sin `.venv` ni `.git`). La única diferencia entre ellas es `src/`: la de HEAD en una y la del cambio en la otra.
- **`sldb stores update`:**
  - `.sldb` y `.sldb_cache` quedan idénticos (`diff -rq` vacío).
  - Las dos copias dan rc=1 con la misma lista de "Skipped broken models". Viene de la copia, no del cambio, igual que en c1.
- **`sldb selfdoc check`:** rc=0 en las dos, con logs idénticos.
- **`component_spec_from_python(..., root_package="sldb")`:** idéntico byte a byte con el escáner de HEAD y con el nuevo, sobre el `src` de cada copia.

## Done When
- **Validation:** PASA.
- **Fixture blog_app:** PASA, verificado con mi propio volcado.
  - Bases: `models.Model`, `viewsets.ModelViewSet`, `serializers.ModelSerializer`, `models.TextChoices`.
  - Decorador: `@action` con `{detail: 'True', methods: "['post']"}`.
  - Llamadas: `PostViewSet.publish` -> `post.publish`, y `Post.publish` -> `can_publish`.
  - Campos: `title`, `status` y `author` (ForeignKey) salen como `assignment` con su `call`.
  - `Meta.db_table`, `Meta.model` y `Meta.fields` (con `items`).
  - Rutas: `path()` en `blogsite.urls.urlpatterns` y `router.register` como hecho `call`.
- **Anclas existentes:** PASA. `NORMALIZATION` sigue en 1 y `record_anchor` da lo mismo que en HEAD en los 15 árboles.
- **CHANGELOG:** PASA. La entrada describe `op`, la cadena, lo que no da fact y la segunda pasada, y la puerta de `check.sh --fast` pasa.
- **Commit y aviso a IR:** no corresponden a esta corrida.

## Archivos fuera del contrato
- `ids.py`, `api/code/code_facts.py`, `test_treesitter_agreement.py` (solo el filtro por kind), `py_calls.py`, `py_module.py`, `py_statements.py` y el fixture `blog_app/` están fuera de la lista `files`. El coordinador dice que todo el diff es de esta tarea, así que los acepto.
- `readers.py` está en la lista pero no cambia.
- El diff de `.sldb/` contiene solo los RunDoc del despacho (`run-deskops-e-…` y `run-deskops-t-…`), no al ejecutor.
- No hay nada más tocado.

## Bordes probados que el ejecutor no cubrió (trees2, dj)
| Caso | Resultado | Clase |
|---|---|---|
| `@admin.register(Post, site=s)` en clase; `metaclass=M` | decorador con args y kwargs; `metaclass` no es base | correcto |
| `@property` + `@functools.lru_cache(maxsize=None)` | los dos decoradores, en orden | correcto |
| `title: str = Field(...)`, `list_display: tuple = (...)` | `assignment` con `call` o con `items` | correcto |
| `urlpatterns += router.urls` | `op '+='`, `value: router.urls` | correcto |
| `urlpatterns = urlpatterns + [path(...)]` | solo `value`, con su texto | límite documentado (Scope b) |
| `if settings.DEBUG: urlpatterns += static(...)` | no da ningún fact | **límite documentado** (docstring y CHANGELOG: "bajo `if`"). Es un modismo frecuente en Django; se anota para IR/coordinador, pero no es una pérdida sin aviso |
| `r"posts"` en args | sale `r"posts"`, sin normalizar el prefijo | observación ya conocida |
