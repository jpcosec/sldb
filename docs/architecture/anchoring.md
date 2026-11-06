# Anclaje

Documento de autoridad de sldb sobre qué es anclar, sus vías, sus reglas y la distinción entre
error y alerta. Las reglas de las secciones 3 y 4 son decisiones del dueño y no se rediscuten;
el diseño técnico que las implementa está en [code-anchoring.md](code-anchoring.md).

## 1. Definición

**Anclar es fundamentar una afirmación en su fuente**: «esto lo digo porque está dicho allá».
Un anclaje une lo que se afirma con el lugar exacto que lo respalda, y **guarda lo que vio**
de esa fuente. Por eso detecta mutaciones: cuando la fuente cambia, lo guardado y lo actual
dejan de coincidir, y el anclaje lo sabe.

Un anclaje que solo resuelve (encuentra a qué apunta) sin guardar lo que vio no verifica nada:
puede decir dónde está su fuente, pero no si sigue diciendo lo mismo.

Esta es la definición de sldb. El `AnchorDoc` de pron la usa con otro sentido, el de **alias**:
una palabra del léxico y lo que nombra (`pron.models:AnchorDoc`). Un alias resuelve; no
fundamenta ni guarda lo que vio.

## 2. Las vías

1. **AnchorDoc**: un documento cuyo `ref` apunta a algo del store (un modelo, un campo, un
   documento, una relación; sldb lo resuelve en `src/sldb/store/edge_index/anchor_targets.py`).
   Hoy resuelve, pero no verifica: no guarda lo que vio.
2. **Código, con tree-sitter**: un anclaje a un símbolo de código, `code:<ruta>::<qualified_name>`,
   resuelto por nombre y no por línea, que guarda un fingerprint de cada nodo que vio
   (`CodeAnchorDoc`, `sldb anchors record|check`); su diseño está en
   [code-anchoring.md](code-anchoring.md).
3. **Documento, con hash de contrato** (GO07): un campo que el modelo declara en
   `__doc_anchors__`, o un elemento `doc:` del `from:` de la provenance, guarda
   `doc:Model:name@sha256:<hash>` con el hash de contrato que vio del destino (sección 6).

## 3. Reglas del anclaje (decisión del dueño, 2026-10-19)

1. **Docstring y cuerpo son nodos distintos.** El anclaje guarda un fingerprint de cada uno por
   separado: el texto normalizado del nodo, no el hash del archivo. Los dos cuentan como
   mutación, pero el anclaje distingue cuál cambió: la docstring, el cuerpo o ambos (y la
   firma, si conviene).
2. **`changed` no es un error, es una alerta** (sección 4). La fuente se movió respecto de lo
   anclado; el estado es válido, pero hay que mirarlo.
3. **Una referencia rota se intenta reconectar.** Si el símbolo ya no está en su
   `qualified_name`, se busca dónde quedó, con la heurística de renombre de selfdoc adaptada
   a los fingerprints por nodo. Si se encuentra, se reporta «reconnected: de X a Y» y queda
   registrado; si no, se reporta «lost». Los dos casos son alertas explícitas, nunca
   silenciosas.

## 4. Error y alerta, en todo sldb (decisión del dueño, 2026-10-19)

- Un **error** es algo roto o que viola un contrato: no parsea, el store está corrupto, un
  documento es inválido, falta un archivo requerido, un modelo no importa.
- Una **alerta** es que la fuente se movió respecto de lo registrado: un anclaje cambió, un
  hash quedó atrás, un documento generado está viejo. El estado es válido, pero hay que
  mirarlo.

Reglas de salida:
- Una alerta no hace fallar el comando: si solo hay alertas, el exit code es 0.
- Una alerta **jamás es silenciosa**. Aparece en la salida de texto; con `--envelope`, en
  `warnings`; en el CI, como annotation; y en el resumen final, con su conteo.
- Un error sí hace fallar el comando.

La regla vale para todo sldb, no solo para los anclajes. Hoy varios comandos tratan un
movimiento de fuente como error (por ejemplo, `stores check` da FAIL por un hash atrasado).
La auditoría de cada caso y su reclasificación propuesta están en
[code-anchoring.md, sección 10](code-anchoring.md).

## 5. Decisiones del dueño sobre la implementación (2026-10-20)

1. **sldb tiene su propio modelo de anclaje.** Lleva la `ref`, un fingerprint por nodo
   (firma, docstring y cuerpo), el estado y la provenance. El `AnchorDoc` de pron sigue
   siendo un alias de léxico y **no se toca**: si algo quiere verificar, va al modelo de sldb.
2. **En `lint`, una ruta citada que ya no existe es la alerta `lost`**: exit 0 y siempre
   visible. El ruido estructural (headings que el modelo no declara) **sigue siendo error**,
   en `lint` y en `stores check`.
3. **`anchors check` solo lee.** `anchors check --record` es el único que escribe, y lo que
   registra son las reconexiones.

Regla general: el envelope lleva las alertas en `warnings` (antes era `[]` fijo) y
`--format json` no las omite. Una alerta nunca es silenciosa. La reclasificación de la
auditoría ([code-anchoring.md, sección 10](code-anchoring.md)) queda aprobada.

## 6. Anclas a documentos (GO07)

Un ancla a un documento es el **valor de un campo**: `doc:Model:name`, o pinneada,
`doc:Model:name@sha256:<hash>`, donde `<hash>` son 64 caracteres hexadecimales: el hash de
contrato del destino que el ancla vio ([rules-language.md §5](rules-language.md)). Se
persiste en el propio documento, en el texto del campo; nada aparte.

**Dónde.** En los campos que el modelo declara en el atributo de clase `__doc_anchors__`
(lista de nombres de campos `str` o `list[str]`, opcionales o no) y en cada elemento de
`from:` de la provenance que empieza por `doc:`. Un elemento de `from:` que no empieza por
`doc:` (`code:...`, otros) no es un ancla de documento y no se toca.

```python
class Review(StructuredNLDoc):
    __doc_anchors__ = ["subject"]
    subject: str = Field(default="", description="The reviewed document.")
    verdict: str = Field(default="", description="accepted or rejected.")
```

**Validación (principio del dueño).** La forma de un valor es una invariante de un documento:
la validan los validadores pydantic (`sldb.models.doc_anchor_value`; el modelo base para los
campos `__doc_anchors__`, `Provenance` para `from:`). Un campo `__doc_anchors__` solo admite
vacío/null o la forma de arriba; cualquier otro texto, un `@sha256:` vacío o un hash que no son
64 hex es `ValidationError` al escribir. La definición del modelo se valida al cargarla
(`resolve_model_ref`, como `__indexed__`) con `SLDBModelError`: un nombre de `__doc_anchors__`
que no es un campo o no es `str`/`list[str]`, o cualquier campo cuyo nombre termina en el
sufijo reservado `__anchor_state`. Lo que depende de otro documento (que exista, su hash, el
estado) no es validación: es el pinneado y `anchors check`.

**Pinneado.** `save_document_payload` completa un valor sin `@sha256` con el hash de contrato
actual del destino, en los campos `__doc_anchors__` y en el `from:` del bloque `sldb`. Si el
destino no está trackeado, el valor se guarda sin hash. Un valor ya pinneado no se repinnea: el
hash es lo que el ancla vio. `create_document` no pinnea: la siguiente escritura lo hace.

**Hash del destino.** `contract_hash(clase del destino, field_hashes del destino)`, con los
`field_hashes` que el índice guarda (GO04) y la clase resuelta como para
`contract_signature` (`model_type_of`). Si la clase del destino no se puede cargar, rige la
regla de `__contract__` ausente: entran todas las claves de `field_hashes`, al pinnear y al
comparar. Un `__contract__` declarado vacío no da hash: el ancla queda `changed` (o se guarda
sin hash).

**Estados** (el vocabulario de `AnchorState`): `intact` (el hash visto es el actual),
`changed` (distinto), `lost` (el destino no está trackeado, o el ancla no tiene hash, aunque el
destino se haya creado después: la siguiente escritura del contenedor la pinnea). `changed` y
`lost` son **alertas**, nunca error. **No hay `reconnected`** para documentos: un destino
renombrado o borrado queda `lost` hasta que alguien reescriba el ancla.

**Aristas.** Cada valor no vacío de un campo `__doc_anchors__` genera una arista `references`
con el nombre del campo hacia `Model:name` (sin el sufijo), con `declared` = el valor escrito;
así `^subject` existe en el grafo. Un destino inexistente no genera arista (queda como
referencia no resuelta, como cualquier `__references__`). `from:` no genera aristas.

**`anchor_state` en el lenguaje.** Al componer el índice (`compose_edge_index`), sobre copias
de los nodos, la facet `payload` de cada documento gana `<campo>__anchor_state` por cada campo
`__doc_anchors__` presente en su payload: escalar para `str`, lista alineada por índice para
`list[str]` (un elemento vacío vale `null`). Un campo `null` o ausente no tiene la clave. La
entrada se calcula al leer y **nunca se escribe al shard**: editar el destino no invalida al
contenedor y `EDGE_INDEX_VERSION` sigue en 5. El lenguaje la expone como `anchor_state` al
atravesar el campo (GO05), también en sentido inverso:

```
any(^subject: anchor_state = "intact" and verdict = "accepted")
```

se cumple sobre una Task si alguna Review la tiene como `subject`, pinneada e intacta, con
veredicto `accepted`.

**`anchors check`.** `sldb.api.check_doc_anchors(store, pythonpath=None) -> list[Finding]`:
un `Finding` de nivel `alert` por ancla no intacta de los documentos del store; códigos
`anchors/doc_changed` y `anchors/doc_lost` (campos `__doc_anchors__`),
`anchors/provenance_changed` y `anchors/provenance_lost` (elementos de `from:`); `subject` es
el `Model:name` del contenedor, `what` nombra el campo (o `from`), el destino y el estado, y
`document` es la ruta del contenedor relativa a la raíz. `sldb anchors check` los agrega a sus
alertas (`doc_anchors` en la salida JSON); el exit code no cambia por ellos. El cableado en
`stores check` es de GO08.
