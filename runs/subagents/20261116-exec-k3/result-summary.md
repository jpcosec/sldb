# Resultado — executor deskops-e-e737091e8bcb

Task: `task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre`.
Pills: ninguno. Se aplican las decisiones del coordinador recibidas a mitad de la ejecución, puntos (1) a (7).

## Cambios

- `src/sldb/code/py_calls.py` (nuevo):
  - `call_parts`: devuelve `{func, args, kwargs}` de un nodo `call`. `*x`, `**x` y un generador como argumento van a `args` como texto.
  - `decorators`: devuelve `{name, args, kwargs}` de cada decorador de una definición.
  - `bases`: las bases que escribe una clase, en orden. `metaclass=` y las demás keywords no cuentan.
  - `body_calls`: devuelve `{name, line}` de cada llamada del cuerpo en orden de fuente, sin entrar en un `def` ni en una `class` anidados.
  - `definition_extras`: para una clase, relaciones `extends` y `attrs.bases`; para una función o método, `attrs.calls` y una relación `calls` por destino distinto; para todas, `attrs.decorators`.
  - Todo el texto pasa por `py_norm`.
- `src/sldb/code/py_statements.py` (nuevo):
  - `statement_facts`: lee el nivel de módulo y el cuerpo de cada clase que es fact, incluida una `Meta` anidada.
    - `nombre = valor` o `nombre: T = valor` da un fact `assignment`, con `attrs.call`, `attrs.items` o `attrs.value`.
    - Una sentencia que es solo una llamada da un fact `call`. Su `name` y su `qualified_name` son el texto de func (con `Owner.` delante dentro de una clase). Su id es `<módulo>.<func>` y `Ids.take` le pone `~N` si se repite.
  - `class_owners`: lista las clases que son dueñas de esas sentencias.
  - Las huellas de un fact nuevo son el sha del texto normalizado (signature y body) y la forma con el nombre sustituido (shape).
- `src/sldb/code/scan.py`:
  - `scan_file` añade los facts de `statement_facts` después de las definiciones.
  - `_definition_facts` devuelve también el mapa de ids.
  - `_definition_fact` incorpora `definition_extras`: relaciones ordenadas como en `rels` y attrs fusionados.
  - Docstring del módulo actualizado.
  - Las huellas de las definiciones no cambian.
- `tests/selfdoc/test_treesitter_symbols.py`: siete tests nuevos.
  - Seis sobre el fixture `blog`, leído vía `sldb.api.code.code_facts` según la decisión (6).
  - Uno de casos borde: llamada repetida con `~2`, `*rest`/`**more`, asignación encadenada, atributo, sentencia dentro de `if`, decoradores con tupla, `metaclass=`, def anidado.
  - Uno que comprueba que `NORMALIZATION` sigue en 1.
- `tests/fixtures/treesitter/blog_app/`: copia del `tests/fixtures/blog_app` de IR (decisión 5), sin `__pycache__`.
- `CHANGELOG.md`: entrada en 0.1.13. Dice que `NORMALIZATION` no sube y por qué, siguiendo la decisión (3).
- `tests/selfdoc/test_treesitter_agreement.py` — **desvío**: no está en la lista de archivos, pero Validation exige que pase. Sin tocarlo fallaba, porque comparaba todos los facts que no son módulo con el escáner `ast` y los kinds nuevos aparecían como "symbol sets differ". El filtro pasa de `kind != "module"` a `kind in ("class", "function", "method")`. Es una línea y no cambia lo que la prueba quiere comprobar.

`src/sldb/code/readers.py` no hizo falta tocarlo: se reutilizan `py_norm`, `text`, `field_text`, `first_statement` y `py_end_line`.

## Done When

- Los comandos de Validation pasan: los 7 con rc=0 (ver `validation.log`).
- Sobre el fixture salen:
  - Las bases `models.Model`, `viewsets.ModelViewSet` y `serializers.ModelSerializer`.
  - `@action` con `{detail: 'True', methods: "['post']"}`.
  - La cadena `PostViewSet.publish -> post.publish` y `Post.publish -> can_publish`, con `can_publish` como función.
  - Los campos como `assignment` con `models.ForeignKey` / `CharField` y sus kwargs, entre ellos `choices`, `on_delete` y `related_name`.
  - `Meta.db_table = 'posts'`, `Meta.model = Post` y `Meta.fields` (items y value).
  - `router.register` como `call` y `path(...)` en `blogsite.urls.urlpatterns.items`.
- Las anclas existentes no cambian de estado: las huellas de module, class, function y method no se tocan, y `NORMALIZATION` sigue en 1. Lo confirman `test_fingerprints.py`, `test_anchors.py` y el test nuevo.
- CHANGELOG: hecho.
- Commit y aviso a IR: **no hechos**, por el brief y por la decisión (7). Quedan para el coordinador.

## Comandos (todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)

| Comando | rc |
|---|---|
| `pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 |
| `pytest -q tests/selfdoc/test_treesitter_agreement.py` | 0 |
| `pytest -q tests/selfdoc/test_fingerprints.py` | 0 |
| `pytest -q tests/notations/test_component_spec_python.py` | 0 |
| `pytest -q tests/api/test_anchors.py` | 0 |
| `pytest -q tests/test_clean_code_rules.py` | 0 |
| `bash tools/check.sh --fast` | 0 |

No corrí la suite completa ni `sldb stores build --check`: los corre el integrador.

## Archivos tocados

- `src/sldb/code/scan.py` (M)
- `src/sldb/code/py_calls.py` (nuevo)
- `src/sldb/code/py_statements.py` (nuevo)
- `tests/selfdoc/test_treesitter_symbols.py` (M)
- `tests/selfdoc/test_treesitter_agreement.py` (M, desvío explicado arriba)
- `tests/fixtures/treesitter/blog_app/**` (nuevo, 13 archivos)
- `CHANGELOG.md` (M)
- `runs/subagents/20261116-exec-k3/{validation.log,result-summary.md}`

## Dudas y riesgos

- **Choque entre (a) y (b) del Scope.** (a) pide `attrs.items` para una lista o tupla; (b) dice que una lista de literales es un literal simple, que daría `attrs.value`. Una lista o tupla da siempre `items`, y además `value` cuando ningún ítem es llamada. Así `fields = [...]` cumple las dos lecturas.
- **Tupla sin paréntesis.** `DRAFT = "draft", "Draft"` (`expression_list`) se trata como tupla.
- **Sentencias que no dan fact.** No dan fact las asignaciones encadenadas (`a = b = 2`), las que tienen como blanco un atributo o una tupla (`obj.attr = 3`, `a, b = ...`) ni las anotaciones sin valor.
- **Colisión de ids entre archivos.** Los facts nuevos van después de las definiciones de su archivo, así que dentro de un archivo no le quitan el id a una definición. Entre archivos sí puede pasar: un `x = ...` en `pkg/__init__.py` toma el id `pkg.x`, y si existe `pkg/x.py` su módulo pasaría a ser `pkg.x~2` en `scan_tree` y `code_facts`, porque `find_files` lee antes `__init__.py`. La resolución de anclas (`record_anchor`) escanea por archivo y no se ve afectada; las referencias de `reconnect` a módulos no usan el sufijo. Lo dejo anotado: evitarlo pediría un espacio de ids aparte, lo que contradice la decisión (2).
