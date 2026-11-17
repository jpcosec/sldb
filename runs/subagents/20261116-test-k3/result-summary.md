# Tester deskops-t-5f3f1737becc — task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre

**Veredicto: FALLA.** Un solo motivo, un caso que el ejecutor señaló como riesgo pero dejó sin resolver.

Una asignación de módulo en `pkg/__init__.py` cuyo nombre coincide con un submódulo hermano (`pkg/x.py`) le quita el id al fact de módulo que ya existía. Ese fact pasa de `pkg.x` a `pkg.x~2`, y la relación `contained-in` de sus definiciones (`pkg.x.f`) apunta ahora a `pkg.x~2`. Esto incumple la aclaración (3) del coordinador: los facts que ya existían tienen que ser idénticos a HEAD salvo las relaciones y los attrs nuevos.

Todo lo demás pasa: Validation, Done When, src/ y los fixtures sin cambios en los facts existentes, el spec, selfdoc y el store.

Salida completa en `validation.log`. Scripts y árboles de prueba en `/dev/shm/k3t-*`.

## Validation (corrida propia, todo con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)

| Comando | Resultado |
|---|---|
| `pytest -q tests/selfdoc/test_treesitter_symbols.py` | PASA: 22 passed, rc=0 |
| `pytest -q tests/selfdoc/test_treesitter_agreement.py` | PASA: 2 passed, rc=0 |
| `pytest -q tests/selfdoc/test_fingerprints.py` | PASA: 4 passed, rc=0 |
| `pytest -q tests/notations/test_component_spec_python.py` | PASA: 5 passed, rc=0 |
| `pytest -q tests/api/test_anchors.py` | PASA: 22 passed, rc=0 |
| `pytest -q tests/test_clean_code_rules.py` | PASA: 1195 passed, rc=0 |
| `bash tools/check.sh --fast` | PASA: rc=0 |

No corrí la suite completa ni `sldb stores build --check`: los corre el integrador.

## Done When, punto por punto

Comprobado con `code_facts` sobre `tests/fixtures/treesitter/blog_app` (script `/dev/shm/k3t-scripts/ir.py`):

- **Bases:** PASA. `Post` da `models.Model`, `Post.Status` da `models.TextChoices`, `PostSerializer` da `serializers.ModelSerializer`, `PostViewSet` da `viewsets.ModelViewSet`, y además `Migration` y `BlogConfig`. Salen como relación `extends` y en `attrs.bases`.
- **@action con argumentos:** PASA. `PostViewSet.publish` lleva `{name: action, kwargs: {detail: 'True', methods: "['post']"}}`.
- **Cadena handler -> método -> función:** PASA. `PostViewSet.publish` llama a `post.publish` (línea 24). `Post.publish` llama a `can_publish` (línea 26). `can_publish` es kind function y llama a `user.has_perm`. Hay relaciones `calls` por destino.
- **Campos de modelo como assignment con su llamada:** PASA. `Post.author`, `title`, `body`, `status` y `published_at` salen con `attrs.call` de `models.*` y sus kwargs: `choices`, `on_delete`, `related_name`, `max_length` y `default`.
- **Meta:** PASA. `Post.Meta.db_table='posts'`, `PostSerializer.Meta.model=Post` y `PostSerializer.Meta.fields` (6 items más `value`) son facts contenidos en su `Meta`.
- **path() y router.register():** PASA.
  - `blogsite.urls.urlpatterns` tiene en `items` `path('', include('blog.urls'))`.
  - `blog.urls.router.register` es kind `call` con `args ['posts', PostViewSet]` y `kwargs {basename: 'post'}`.
  - `blog.urls.router` es `SimpleRouter(trailing_slash=False)`.
- **Las anclas existentes no cambian de estado:** PASA.
  - Las huellas de los facts existentes son idénticas a HEAD (ver aclaración 3).
  - `NORMALIZATION` sigue en 1.
  - `record_anchor` escanea un solo archivo con su propio `Ids`, así que el caso de la FALLA no lo alcanza. `reconnect` excluye kind module.
- **CHANGELOG:** PASA. Hay una entrada en 0.1.13. Cuadra con el código: kinds, attrs, ids `~N` y `NORMALIZATION`. La puerta de afirmaciones de `check.sh --fast` pasa.
- **Commit y aviso a IR:** no hechos, como corresponde. El brief prohíbe el commit y quedan para el coordinador.

## Aclaraciones del coordinador

1. **Archivos del cambio:** asumidos como parte del cambio `py_calls.py`, `py_statements.py` (67 y 68 líneas) y el fixture `blog_app` (13 archivos).
2. **Desvío en `test_treesitter_agreement.py`:** PASA. La única línea que cambia es el filtro: `kind != "module"` pasa a `kind in ("class", "function", "method")`. En HEAD, los árboles que usa (`pytree` y `pytree_ts`) solo dan los kinds module, class, method y function. Por eso el filtro nuevo excluye exactamente lo mismo que antes más `assignment` y `call`, y no debilita ninguna comparación existente. Lo confirma el recuento por kind de HEAD en `validation.log`.
3. **Facts existentes frente a HEAD:** sobre src/ y los fixtures, PASA; en general, FALLA (motivo del veredicto).
   - Corrí los escáneres de HEAD y del cambio sobre el mismo árbol (`git archive HEAD` en `/dev/shm/k3t-head`). Quité de los facts nuevos solo `extends`, `calls`, `decorators` y `bases`.
   - Resultado en `pytree`, `pytree_ts`, `frontend`, `sql`, `blog_app` y `src/sldb`: 0 facts faltantes y 0 cambiados.
   - Se añaden facts `assignment` y `call`: 3, 3, 0, 0, 30 y 1928 respectivamente.
   - Como se ve en el caso propio de abajo, el invariante no se cumple en general.
4. **Spec, selfdoc y store:** PASA en las tres comprobaciones.
   - `component_spec_from_python(src, root_package="sldb")` es idéntico byte a byte con el escáner viejo y con el nuevo, sobre el árbol de HEAD y sobre el árbol del cambio.
   - `sldb selfdoc check`: rc=0 en los dos, con la misma salida.
   - `sldb stores update` en copias de /dev/shm (`k3t-store-old` y `k3t-store-new`):
     - `.sldb` y `.sldb_cache` quedan idénticos (`diff -rq` vacío). El store no consume `sldb.code`.
     - El rc=1 sale igual en las dos copias y se debe a la copia: excluí `runs/`, así que faltan 78 RunDoc y quedan modelos rotos. No viene del cambio.
     - Tiempo: 63 s frente a 83 s en frío; en caliente, 5 s. Lo atribuyo a ruido de caché.
   - Tamaño de `code_facts`:

     | Árbol | Facts (antes → después) | Bytes JSON (antes → después) | Tiempo (antes → después) |
     |---|---|---|---|
     | `src/sldb` | 5656 → 7600 | 5,99 MB → 9,37 MB (+56 %) | 5,6 s → 5,9 s |
     | `blog_app` | 33 → 63 | 28 KB → 57 KB | — |

     En `src/sldb` el aumento es de 1921 `assignment` y 7 `call`.
5. **Mejora para IR sobre `blog_app` (HEAD → cambio):**

   | Hecho | HEAD | Cambio |
   |---|---|---|
   | `path()` en urlpatterns | 0 | 1 |
   | `router.register` | 0 | 1 |
   | `@action` | 0 | 1 |
   | Campos de modelo | 0 | 5 |
   | Hechos de Meta | 0 | 4 |
   | Llamadas registradas | 0 | 14 |
   | Clases con bases | 0 | 6 |

   Antes de este cambio IR no podía derivar nada de eso.

## Caso propio (no cubierto por el ejecutor)

Árbol en `/dev/shm/k3t-edge/t`, script en `/dev/shm/k3t-scripts/edge.py`.

- **FALLA, colisión de ids entre archivos:** `pkg/__init__.py` contiene `x = 1` y existe `pkg/x.py` con `def f()`.
  - En HEAD: `pkg.x` es module.
  - Con el cambio: `pkg.x` es la assignment y el módulo pasa a `pkg.x~2`. `pkg.x.f` mantiene su id, pero su `contained-in` apunta a `pkg.x~2`.
  - Afecta a `scan_tree` y a `code_facts`, que es justo lo que consume IR, y por lo tanto a cualquier consumidor que use el id de un módulo. No afecta a las anclas ni al component spec, que usa `qualified_name`.
  - El ejecutor lo declaró en sus riesgos y lo atribuyó a la decisión (2). Si el coordinador acepta ese riesgo, el resto queda en PASA.
  - Arreglo posible, sin implementar: tomar los ids de los facts nuevos después de los de todas las definiciones del árbol, o darles un espacio de ids propio.
- **PASA, resto de casos borde:**
  - `async def` con `await`.
  - Decoradores `@functools.lru_cache(maxsize=None)` y `@a.b(c)(d)` (name `a.b(c)`, args `[d]`).
  - `@dataclass(frozen=True)` en una clase.
  - Bases `Generic[T]` y `Base` con coma final.
  - `@property`.
  - kwargs multilínea con comentario, normalizados por `py_norm`.
  - `y: int` sin valor, `z += f()` e `i, j = 1, 2` no dan fact.
  - Una lista con `*more` da `{value: '*more'}`.
- **Observaciones, no bloquean:**
  - Una assignment de clase con el mismo nombre que un método toma `~2` (`P.title~2`). Las definiciones van primero, así que el método conserva su id.
  - Una lambda invocada en el acto aparece como callee con su texto (`(lambda: k())`), además de `k`. Es ruido sintáctico aceptable según el Scope, que pide el texto tal cual.

## Alcance de archivos

PASA. Fuera de los archivos del contrato solo se tocaron:

- `py_calls.py` y `py_statements.py`: módulos nuevos, autorizados por el Implementation Path y por la aclaración 1.
- El fixture `blog_app`, que pide el Scope.
- `test_treesitter_agreement.py`: el desvío revisado en la aclaración 2.

`readers.py` no se tocó. En `CHANGELOG.md` se añade una sola línea. No hay otros cambios en `src/` ni en `tests/`. No revisé los cambios ajenos.

## Regresiones vecinas

PASA. El módulo cambiado es `src/sldb/code/scan.py` (más los dos nuevos). Los tests que lo usan son `test_anchors`, `test_component_spec_python`, `test_treesitter_agreement`, `test_treesitter_symbols` y `test_fingerprints`. Agregué `tests/api/test_doc_anchors.py` (24 passed). Todos pasan, corridos archivo por archivo. No hay fallas nuevas respecto de HEAD.
