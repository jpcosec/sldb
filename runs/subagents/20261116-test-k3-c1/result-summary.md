# Tester deskops-t-5f3f1737becc-a2: corrección 1 de C3 Python

Task: `task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre`.

**Veredicto: FALLA, por un solo motivo.** La FALLA del intento 1 (choque de ids) está resuelta: los facts existentes son idénticos a HEAD en los 13 árboles probados, también en todos los choques. El motivo nuevo es un borde que el intento 1 no probó:

- **`urlpatterns += [...]` y `urlpatterns += static(...)` se pierden sin aviso.** Una asignación aumentada no da ningún fact. El fact `urlpatterns` muestra solo la lista inicial y nada indica que la lista se amplió después.
  - Este es el modismo de la documentación de Django (`+= static(...)`) y de DRF (`+= router.urls`).
  - Con el criterio del coordinador (datos erróneos sin aviso en Python común) cuenta como falla.
  - Atenuante: el Scope define la asignación como `nombre = valor`, así que el `+=` queda fuera de la letra del contrato. Si el coordinador prefiere tratarlo como límite, alcanza con documentarlo en el docstring de `py_statements` y en el CHANGELOG. La otra opción es emitirlo como `assignment` con `attrs.op: "+="`, con id tardío y `~N`.

Salida completa en `validation.log`. Scripts y árboles en `/dev/shm/k3t2/`.

## Validation (corrida propia con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)
| Comando | Resultado |
|---|---|
| pytest -q tests/selfdoc/test_treesitter_symbols.py | PASA, 24 passed |
| pytest -q tests/selfdoc/test_treesitter_agreement.py | PASA, 2 passed |
| pytest -q tests/selfdoc/test_fingerprints.py | PASA, 4 passed |
| pytest -q tests/notations/test_component_spec_python.py | PASA, 5 passed |
| pytest -q tests/api/test_anchors.py | PASA, 22 passed |
| pytest -q tests/test_clean_code_rules.py | PASA, 1196 passed |
| bash tools/check.sh --fast | PASA, rc=0 |

`uv` funcionó y no hizo falta el plan B. La suite completa y `sldb stores build --check` quedan delegadas al integrador.

**Regresiones vecinas.** Los tests que importan los módulos tocados (`scan`, `ids`, `py_calls`, `py_module`, `py_statements`, `api.code`) son `test_anchors`, `test_component_spec_python`, `test_treesitter_agreement` y `test_treesitter_symbols`. Son los mismos de Validation y los cuatro pasan.

## (1) Facts existentes frente a HEAD, choque y variantes: PASA
Método:
- `probe.py` corre una vez con el `src` de HEAD (`git archive` en `/dev/shm/k3t-head`, que es idéntico a `HEAD:src`) y otra con el `src` del árbol.
- A los facts nuevos solo se les quitan `extends`, `calls`, `decorators` y `bases`.
- Compara los facts module, class, function y method completos, incluidos id, `contained-in` y huellas, además de los kinds TS y SQL.

Resultado: 13 árboles OK, 0 faltantes, 0 cambiados y 0 ids None.

| Árbol | Facts existentes | Kinds nuevos |
|---|---|---|
| `src/sldb` | 5674 | 1930 |
| blog_app | 26 | 37 |
| pytree, pytree_ts, frontend, sql | 28, 20, 7 y 2 | — |
| `k3t-edge/t` (el caso del intento 1) | 8 | — |

Variantes del choque (`/dev/shm/k3t2/trees/`). En todas, el fact existente conserva su id y el nuevo lleva el `~N`:
- **clash**: `x = 1` en `pkg/__init__.py` frente a `pkg/x.py`. `pkg.x` es el módulo y la asignación es `pkg.x~2`.
- **callsub**: la llamada de módulo `y()` frente al submódulo `pkg/y.py`. La llamada es `pkg.y~2`.
- **attr**:
  - El atributo de clase `foo = 1` frente al método `foo`: el método es `m.A.foo` y el atributo `m.A.foo~2`.
  - `def main` + `main()` + `main = 3`: quedan `m.main`, `m.main~2` (call) y `m.main~3`.
- **nested**: los paquetes anidados `a/__init__.py: b = 1`, `a/b/__init__.py: c = make()`, `a/b/c.py` y `a/b/d.py`. Los módulos `a.b` y `a.b.c` conservan su id; las asignaciones son `a.b~2` y `a.b.c~2`.
- **rootinit**: `z = 2` en el `__init__.py` de la raíz frente a `z.py`. La asignación es `z~2`.

## (2) record_anchor, check_anchors y code_facts: PASA
- **record_anchor:** `scan_file` sin `idgen` da los mismos ids de facts existentes que HEAD, archivo por archivo, en todos los árboles. `record_anchor` sobre cada fact existente da el mismo resultado que en HEAD, incluidos los errores. `symbol_of` sigue usando el `scan_file` de un solo archivo.
- **check_anchors:** se apoya en `record_anchor`/`scan_file` y en `scan_tree` (`reconnect`). Por eso queda cubierto por la igualdad anterior y por `tests/api/test_anchors.py`, que pasa.
- **code_facts:** da el mismo conjunto de ids que `scan_tree` en los 13 árboles, igual que en HEAD.

## (3) Spec, selfdoc y store: PASA
Corrí dos copias completas del árbol en `/dev/shm/k3t2/store-{old,new}`. Esta vez incluyen `runs/`. La única diferencia entre ellas es `src/`: la de HEAD en una y la del cambio en la otra.

- **`sldb stores update`:**
  - `.sldb` y `.sldb_cache` quedan idénticos (`diff -rq` vacío).
  - Las dos copias dan rc=1 con la misma lista de "Skipped broken models". Viene de la copia, no del cambio.
  - Tardaron unos 2120 s cada una, con load ~250 en la máquina.
- **`sldb selfdoc check`:** rc=0 en las dos, con logs idénticos.
- **`component_spec_from_python(..., root_package="sldb")`:** idéntico byte a byte con el escáner de HEAD y con el nuevo, sobre el mismo `src`, en los dos árboles. Los specs de una copia y la otra difieren solo porque cada `src` tiene módulos distintos.
- **Lock de tests:** no usé `/dev/shm/sldb1-tests.lock`. Lo tenía tomado la suite completa de otro agente, y estas son copias aparte que no tocan el store del repo.

## Done When
- **Validation:** PASA.
- **Fixture blog_app:** PASA. Salen las bases, `@action` con sus kwargs, la cadena handler -> `post.publish` -> `can_publish`, los campos como `assignment` con su llamada, `Meta.db_table`, `Meta.model` y `Meta.fields`, `path()` y `router.register`. Lo cubren los tests y lo verificó el tester del intento 1; el fixture no cambió.
- **Anclas existentes:** PASA. Ver (2), y `NORMALIZATION` no cambia.
- **CHANGELOG:** PASA. Describe la segunda pasada y `pkg.x~2`. La puerta de `check.sh --fast` pasa.
- **Commit y aviso a IR:** no corresponden a esta corrida; los hace el coordinador.

## Archivos fuera del contrato
- `ids.py`, `api/code/code_facts.py` y `test_treesitter_agreement.py` (filtro por kind) están fuera de la lista `files`. El coordinador dice que todo el diff es de esta tarea, así que los acepto.
- `readers.py` está en la lista pero no cambia.
- No hay nada tocado fuera de esto ni de los cambios ajenos.

## Bordes nuevos y su clase (`trees/common` y `trees/dj`)
| Caso | Qué pasa | Clase |
|---|---|---|
| `urlpatterns += [path(...)]`, `+= static(...)` | No da ningún fact; las rutas se pierden sin aviso | **FALLA**: común en Django y sin documentar |
| `urlpatterns = [path(...)] + router.urls` | Solo `attrs.value` con el texto, sin `items`. El texto arrastra el comentario `# admin` | Límite documentado (Scope b: "lo demás da value con su texto"). El comentario dentro del texto es cosmético |
| `created = updated = models.DateTimeField(...)` | No da ningún fact | Límite poco común pero sin documentar: conviene una línea en el docstring |
| `p, q = f()` y `y: int` sin valor | No da ningún fact | Fuera del Scope (`nombre = valor`). Conviene documentarlo |
| Asignación bajo `if` | No da ningún fact | Límite documentado |
| `r"posts"` en args | Sale `r"posts"`, mientras los demás strings salen `'post'` | Observación: `py_norm` no normaliza los prefijos de string |
| `super().t()` y `A().foo()` | Salen las dos llamadas, la de afuera y la de adentro (`super().t` y `super`) | Correcto según el Scope |
