# Anclaje a código

Estado (2026-10-20): implementado (etapas b, c y d: escáner, modelo `CodeAnchorDoc`, `anchors
record` y `anchors check [--record]`); deskops avisado por inbox de cómo declarar anchors desde
atoms, tasks y docs (etapa e). La definición, las vías y
las reglas del dueño están en el documento de autoridad, [anchoring.md](anchoring.md); este
documento las implementa y no las rediscute.

Decisiones del dueño (2026-10-20), [anchoring.md, sección 5](anchoring.md):
1. El anclaje es un modelo propio de sldb, con `ref`, fingerprints por nodo, estado y
   provenance. El `AnchorDoc` de pron no se toca; la sección 7 queda reemplazada.
2. En `lint`, una ruta citada que no existe es la alerta `lost`. El ruido estructural sigue
   siendo error.
3. `anchors check` solo lee; `anchors check --record` es el único que escribe, y registra las
   reconexiones. `anchors update` queda fuera.

## 1. Referencia

`code:<ruta>::<qualified_name>`, por ejemplo `code:src/sldb/store/model_import_root.py::import_root`
o `code:src/sldb/api/stores/store_declaration.py::StoreDeclaration.derived`.

- `<ruta>` es relativa a la raíz del proyecto, con `/`.
- `<qualified_name>` es el que emite el adaptador tree-sitter: la cadena de dueños léxicos
  (`Clase.metodo`, `funcion.anidada`). El módulo entero es `code:<ruta>::` (nombre vacío).
- Se resuelve por nombre, nunca por línea: las líneas se mueven sin que nada cambie.
- Un nombre repetido en el mismo archivo (definición condicional, redefinición) toma el
  sufijo `~2`, `~3` del adaptador, en orden de aparición.

## 2. Lo que guarda un anclaje

```yaml
code:
  ref: code:src/sldb/store/model_import_root.py::import_root
  kind: function            # module | class | function | method
  seen:                     # un fingerprint por nodo, no el hash del archivo
    signature: sha256:…     # decoradores + firma normalizada
    shape: sha256:…         # la firma sin el nombre: lo que un renombre conserva
    docstring: sha256:… | null   # null: no tenía docstring
    body: sha256:…          # el cuerpo sin la docstring
  normalization: 1          # versión de las reglas de la sección 3
  recorded_with: treesitter-symbols/1 (tree-sitter-python 0.x)
  history:                  # lo que pasó con la referencia, nunca se borra
    - {event: reconnected, from: code:…::old_name, to: code:…::import_root}
```

Docstring y cuerpo son nodos distintos (decisión 1): un cambio en la docstring no toca el
fingerprint del cuerpo, y al revés. Guardar los tres fingerprints permite decir cuál cambió.

## 3. Normalización (versión 1)

El fingerprint es `sha256` del texto normalizado del nodo, no del archivo.

| nodo | texto normalizado |
|---|---|
| signature | los decoradores, en orden, más `def nombre(params) -> ret` o `class Nombre(bases)`, con los espacios colapsados (`py_norm` del adaptador) |
| docstring | el valor del literal (no su sintaxis), con `inspect.cleandoc`; `null` si no hay |
| body | los tokens hoja del cuerpo, sin la docstring y sin comentarios, unidos por un espacio |

- **Formato no es mutación.** Reindentar, partir líneas o mover comillas no cambia ningún
  fingerprint. Un comentario tampoco: no es docstring ni código.
- **Una definición anidada no arrastra a su dueña.** En el cuerpo de una clase, cada método se
  reemplaza por su nombre y su fingerprint de firma: el anclaje a la clase cambia si cambian
  sus propios enunciados o la lista y las firmas de sus métodos, no si cambia el cuerpo de un
  método. El método se ancla aparte.
- Cambiar estas reglas sube `normalization`; un anclaje grabado con otra versión se reporta
  `renormalize` (alerta) y se compara recién después de regrabarlo.

## 4. Estados

| estado | condición | clase | qué se hace |
|---|---|---|---|
| `intact` | el nombre existe y los tres fingerprints coinciden | ok | nada |
| `changed(signature\|docstring\|body)` | el nombre existe y difiere al menos uno; se listan cuáles | alerta | mirar; reanclar (`anchors record` y guardar lo visto en el anclaje) |
| `reconnected(X → Y)` | el nombre ya no existe y hay **un único** candidato (sección 5) | alerta | se reporta y se registra en `history`; puede venir con `changed` |
| `lost` | el nombre ya no existe y no hay candidato, o hay más de uno (se listan) | alerta | mirar; reanclar a mano |
| `renormalize` | grabado con otra versión de normalización | alerta | reanclar, como en `changed` |
| `unparseable` | el archivo no parsea (`has_error`) | **error** | arreglar el archivo |
| `invalid` | la referencia no tiene la forma `code:…::…`, o el anclaje no trae `seen` | **error** | arreglar el documento |
| `unavailable` | tree-sitter o su gramática no están instalados (extra `[code]`) | **error** | `pip install 'structuredLanguageDB[code]'` |

Si el archivo ya no existe, se busca candidato en todo el proyecto; si no hay, es `lost`.

## 5. Reconexión

Adapta la heurística de renombre de selfdoc (`_rename_candidate`/`_symbol_key` en
`cli/selfdoc_inspect.py`, que exige igualdad de hash de archivo, kind, firma y docstring) a
fingerprints por nodo:

1. Candidatos del mismo `kind`, primero en el mismo archivo, después en el resto del proyecto.
2. Coincide si el **cuerpo** es igual (el código no cambió, se movió o renombró), o si
   **docstring y firma** son iguales salvo el nombre.
3. Un único candidato: `reconnected`. Cero o más de uno: `lost`, con los candidatos listados.

`anchors check` solo lee. `anchors check --record` es el único que escribe (decisión del
dueño 3): registra la reconexión en el anclaje, con la nueva `ref` y una entrada en
`history`. Así queda registrada sin que una lectura escriba.

## 6. Comandos

- `sldb anchors record <ref> [--write <ruta> --claim "..."]`: resuelve la referencia y devuelve
  el bloque de la sección 2; con `--write` crea (o regraba, conservando `claim` e `history`)
  un `CodeAnchorDoc` trackeado en el store.
- `sldb anchors check [--store S] [--format text|json] [--record]`: verifica cada anclaje a
  código del store. Exit 0 con solo alertas; distinto de 0 solo con errores (`anchors/invalid`
  3, `anchors/unparseable` 3, `anchors/unavailable` 5 con `--envelope`).
- No hay `anchors update` (decisión del dueño 3). Aceptar un `changed` es reanclar: el autor
  guarda en el anclaje el bloque que da `anchors record`, con la API de documentos.

Una alerta nunca es silenciosa:
- va en la salida de texto, una línea por anclaje;
- con `--envelope`, va en `warnings`;
- en GitHub Actions (`GITHUB_ACTIONS=true`), se imprime como `::warning file=…::`;
- el resumen final da los conteos: `12 intact, 2 changed, 1 reconnected, 0 lost — 3 alertas`.

## 7. Modelo propio, no AnchorDoc (decisión del dueño 1)

El anclaje es un modelo de sldb que guarda la `ref`, lo visto (sección 2), el estado y la
provenance. AnchorDoc es un modelo de **pron** (`pron.models:AnchorDoc`), un alias de léxico
que sldb hereda y resuelve (`store/edge_index/anchor_targets.py`). AnchorDoc no cambia: un
alias resuelve, y lo que quiera verificar remite al modelo de anclaje de sldb.

## 8. Origen del código

Hecho (2026-10-20): el adaptador vive en `src/sldb/code/` (solo Python,
partido a las reglas de tamaño de sldb), con `fingerprints.py` para los nodos de la sección 3
más `shape` (la firma sin el nombre, para reconectar un renombre); el extra es `[code]`
(`tree-sitter>=0.25`, `tree-sitter-python`), y los tests y fixtures están en
`tests/selfdoc/test_treesitter_symbols.py`, `tests/selfdoc/test_treesitter_agreement.py`
(contra `PythonScanner`, el escáner `ast` de sldb) y `tests/fixtures/treesitter/`.

El adaptador viene de `kimun/python/kimun/adapters/treesitter_symbols.py` (MIT, mismo autor),
con sus tests `test_treesitter_symbols.py` y `test_treesitter_agreement.py` y las fixtures que
usan (`kimun/test/fixtures/adapters/pytree`, `pytree_ts`). Por autorización del dueño, es lo
único que se trae de kimun. Va a `sldb.selfdoc`, tree-sitter queda como extra opcional `[code]`
(`tree-sitter>=0.25`, que trae `QueryCursor`), y la prueba de acuerdo se porta contra el
escáner ast de sldb. Las funciones de fingerprint por nodo son nuevas en sldb: el adaptador
emite la firma y la docstring, pero no el texto del cuerpo.

## 9. Las reglas, ejecutables

Las reglas de [anchoring.md](anchoring.md) quedan en el código, no solo escritas:

- **Estados como enum tipado.** `AnchorState` (`intact`, `changed`, `reconnected`, `lost`,
  `renormalize`, `unparseable`, `invalid`, `unavailable`). Cada valor dice su clase,
  `ok`, `alert` o `error`, en un solo lugar. `changed` lleva el conjunto de nodos que
  cambiaron (`signature`, `docstring`, `body`).
- **Un test por regla.**
  - Regla 1: cambiar solo la docstring da `changed({docstring})`, cambiar solo el cuerpo da
    `changed({body})`, cambiar los dos da los dos; reformatear sin cambiar tokens da `intact`.
  - Regla 2: un `changed` sale con exit 0 y su línea aparece en el texto, en `warnings` del
    envelope y en el conteo del resumen.
  - Regla 3: renombrar un símbolo da `reconnected` con origen y destino; borrarlo, o dejar dos
    candidatos, da `lost`. Las dos cosas siempre se reportan.
- **Ninguna alerta muda.** Un test genérico recorre las alertas que emite un comando y falla si
  alguna no aparece en su salida de texto o en sus `warnings`. Se aplica a `anchors check` y a
  cada comando que se reclasifique según la sección 10.

## 10. Error y alerta en todo sldb (auditoría del 2026-10-19)

Nota (2026-10-20): la tabla de abajo fue la auditoría; el criterio vigente ya no es una tabla
fija sino la política por autoridad de [provenance.md, sección 5](provenance.md), que la
implementa con los defaults ahí descritos (la ruta citada ausente en `lint` es la alerta
`lost`, decisión del dueño).

La regla del dueño vale para todo sldb. Un **error** es algo roto o que viola un contrato (no
parsea, store corrupto, documento inválido, archivo requerido ausente, modelo que no
importa). Una **alerta** es que la fuente se movió respecto de lo registrado: el estado es
válido, pero hay que mirarlo. Una alerta no hace fallar el comando y nunca es silenciosa.

Hoy sldb trata como error la mayoría de los movimientos de fuente:

| comando | hallazgo | hoy | propuesta |
|---|---|---|---|
| stores check | hash raíz o roster atrasado (`root_ok`, `roster_ok`, `roster_only`) | FAIL, exit 1 | alerta |
| stores check | contrato movido, `contract_mutation`, relectura por un sldb nuevo | FAIL | alerta |
| stores check | `data_mutation` (el documento cambió desde el índice) | FAIL | alerta, mostrada siempre con su detalle |
| stores check | `missing` (archivo trackeado ausente) | FAIL | **error** |
| stores check | modelo que no importa (hoy es una nota y PASS) | PASS | **error** (pasa de menos a más) |
| stores check | enlace roto (hoy es una nota) | PASS | **error** |
| stores check | `legacy_contract`, ruido estructural, `rewrite_loss`, modelos sombreados, política de `.gitignore` | nota | alerta; el ruido estructural es **error** (decisión del dueño 2: las escrituras ya lo rechazan) |
| stores build --check | la copia no pasa la integridad, hay archivos sin declarar, o declarados sin archivo | FAIL | **error** |
| stores build --check | la copia trackea algo que el store local no tiene (local atrasado) | FAIL | alerta |
| selfdoc check / python-check | campos generados viejos, documentos sin generar o sin trackear, hashes viejos, símbolos o comandos quitados, pista de renombre | exit 1 | alerta |
| selfdoc python-check | grafo de fuente viejo | exit 1 | alerta; ausente, ilegible o con otra forma: **error** (hoy van juntos) |
| selfdoc python-check | metadata mal formada, ids repetidos, colisiones | exit 1 | **error** |
| edges check | shard construido desde otro `hash_c` | exit 1 | alerta |
| edges check | aristas inválidas, ciclos, tipos desconocidos | exit 1 | **error** |
| lint | ruta citada que ya no existe | exit 1 | alerta `lost` (decisión del dueño 2) |
| journal verify, models check, stores update con modelos o archivos ausentes | cadena rota, no registrado, no importa, falta | exit 1 | **error** |
| serve `/lint` | raíz o roster atrasados y `data_mutation` como `error`; `missing` como `warning` | — | invertir |

Hoy una alerta quedaría muda en ocho lugares. Hay que arreglarlos al reclasificar:
1. `stores check` imprime el detalle solo cuando el store es inválido (`store_check_report.py`).
2. `--format json`/`yaml` y `--quiet` omiten todas las notas, y el JSON no tiene campos para
   ellas (`store_check.py`).
3. `build --check` descarta la salida del `stores check` de la copia y conserva solo el exit.
4. La nota de `legacy_contract` solo sale cuando el roster está bien.
5. `/health` no da hallazgos cuando el store es válido, y tampoco da los de raíz o roster
   cuando no lo es.
6. `/lint` no da problemas para contratos movidos.
7. El envelope de éxito tiene `warnings: []` fijo (`cli/envelope.py`).
8. Un modelo que no importa oculta la deriva de su contrato.

Propuesta de implementación: un tipo `Alert` común (código `ns/name`, sujeto, qué se movió,
qué hacer) que cada comando devuelve junto con sus errores. Un emisor único lo saca por las
cuatro vías: texto, `warnings` del envelope, `::warning` en GitHub Actions y el conteo del
resumen. El exit code pasa a depender solo de los errores.

Dos inconsistencias encontradas de paso:
- El docstring de `selfdoc/report.py` dice que las variantes de Python devuelven 0 con
  `ok` falso, pero devuelven 1.
- En `check_store` (API y `GET /stores/check`), `ok` y `valid` no coinciden ante movimientos
  benignos.
