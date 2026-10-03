# Los ejes de capacidad

Las capas (`contracts/layers.toml`) responden *¿quién puede importar a quién?*.
Es una pregunta de orden, y sirve para impedir ciclos.

No sirve para la otra pregunta: **¿qué sabe hacer este sistema?** Una capacidad
puede estar repartida entre varias capas, y dos cosas en la misma capa pueden no
tener nada que ver.

Este documento mapea la otra dimensión: los subsistemas que le dan identidad.

**Nota de método**: este documento se corrigió cuatro veces, y cada corrección la
forzó la puerta que lo verifica (`tools/check_axes.py`):

| versión | decía | la puerta encontró |
|---|---|---|
| 1 | 10 ejes, sin motor de embeddings | existe, y es el mejor diseñado (§3) |
| 2 | 12 ejes | faltaba la bitácora |
| 3 | el motor de grafo no importa nada | 5 archivos sí importan (§1) |
| 4 | 14 ejes, 222 archivos | **339 archivos sin eje: el 60% del sistema** |

La versión final tiene **24 ejes y 425 archivos mapeados**. El error de la cuarta
es el más instructivo: excluí `api/` y `store/` del recuento por comodidad, y ahí
vive casi todo el código. Un mapa que ignora el 60% de lo que describe no es un
mapa, y solo una puerta lo nota.

---

## El grafo

```
                      ┌─ superficie ─┐
                      │              │
        markdown ─────┤   BaseAST    │
        python-ast ───┤   Handler    │──→ representación (IR)
        argparse ─────┤              │       MeaningNode
        click ────────┘              │       SurfaceNode
                      └──────────────┘            │
                                                  ▼
                                            contrato (modelos)
                                              StructuredNLDoc
                                                  │
                        ┌─────────────────────────┼──────────────────┐
                        ▼                         ▼                  ▼
                   persistencia               consulta            grafo
                  (store/io, models)      (query_engine,      (store/graph
                        │                      corpus)          + edge_index)
                        │                         │                  │
                        └──────── render ◄────────┴── semántica ─────┘
                              (jinja2, reversible)    (DAG de tipos)
```

---

## Los veinticuatro ejes, medidos

Salida de `python tools/check_axes.py --map`:

### Identidad — 63 archivos

| eje | arch. | externo | qué sabe hacer |
|---|---|---|---|
| **superficie** | 18 | `markdown-it-py` | texto → árbol unificado |
| **representación** | 15 | `pydantic` | `MeaningNode` + `SurfaceNode`: significado y superficie ancladas |
| **render** | 14 | `jinja2` | árbol → texto reversible |
| **contrato** | 11 | `pydantic` | qué es un documento válido |
| **runtime** | 3 | — | qué se permite al renderizar; `extract_model_data` |
| **identidad_y_hash** | 2 | — | las huellas que detectan deriva |

### Motores — 126 archivos

| eje | arch. | externo | qué sabe hacer |
|---|---|---|---|
| **persistencia** | 34 | — | guardar, indexar, fragmentar |
| **grafo** | 33 | `networkx` | recorrer, ciclos, orden, centralidad, similitud estructural |
| **índice_de_aristas** | 25 | — | derivar aristas de documentos |
| **adaptadores** | 22 | `ast`, `argparse`, `click` | derivar documentos de código |
| **recuperación** | 19 | *puerto `Embedder`* | similitud aproximada, caché de vectores |
| **consulta** | 11 | — | buscar y filtrar por campo |
| **bitácora** | 10 | — | una entrada encadenada por hash por escritura |
| **semántica** | 10 | `networkx` | jerarquía de tipos como DAG |
| **enlaces** | 7 | — | relaciones declaradas entre documentos |

### Operación — 158 archivos

| eje | arch. | qué sabe hacer |
|---|---|---|
| **op_almacén** | 46 | abrir, enlazar, refrescar, exportar, diagnosticar |
| **op_documentos** | 45 | seguir, guardar, navegar documentos y tramos |
| **op_modelos** | 45 | resolver, registrar, describir, editar contratos |
| **op_aristas** | 22 | leer, reconstruir, verificar el índice; consultar el grafo |

### Infraestructura — 35 archivos

| eje | arch. | qué sabe hacer |
|---|---|---|
| **errores** | 17 | la jerarquía de excepciones |
| **caché** | 6 | memorizar lo derivado y saber cuándo invalidarlo |
| **federación** | 5 | encontrar almacenes y resolver entre varios |
| **migración** | 3 | leer almacenes de versiones anteriores |
| **codec** | 2 | serializar el estado del almacén |

### El acoplamiento entre ejes

| origen → destino | aristas |
|---|---|
| op_almacén → persistencia | **36** |
| op_documentos → persistencia | **30** |
| op_modelos → persistencia | **27** |
| índice_de_aristas → persistencia | **23** |
| op_aristas → grafo | 19 |
| op_aristas → índice_de_aristas | 18 |
| op_aristas → persistencia | 17 |
| op_modelos → errores | 16 |
| op_modelos → op_almacén | 13 |
| semántica → persistencia | 12 |

El patrón: **los cuatro ejes de operación cuelgan de persistencia**, con 110
aristas entre ellos. Eso es esperable —una operación opera sobre lo guardado— y
confirma que `persistencia` es el centro del sistema aunque no sea su identidad.

Los ejes de identidad, en cambio, se tocan poco: `superficie → representación`
son 9 aristas, `render → superficie` 5. Fronteras limpias entre las piezas que
definen qué es el sistema.

---

## Lo que el mapa revela

### 1. El motor de grafo es *casi* extraíble

Primero escribí que `store/graph/` no importaba nada fuera de sí mismo. La puerta
`check_axes.py` lo refutó: **cinco archivos sí lo hacen**.

| archivo | importa de |
|---|---|
| `store/graph/convert.py` | `edge_index`, `store/models` |
| `store/graph/node_view.py` | `store/models` |
| `store/graph/traversal.py` | `edge_index` |
| `store/graph/analysis/relations.py` | `models` |

Mi comprobación había usado un `grep` que truncaba las rutas y solo mostraba los
imports internos. El dato correcto: **28 de 33 archivos son autónomos**, y las
cinco aristas se concentran en convertir entre el formato del índice de aristas y
el del motor.

Eso es una frontera de adaptación, no una fusión. Pero hay que cortarla antes de
llamar al eje extraíble, y está declarada como deuda en el contrato.

Aparte de eso:

```
$ python3 -c "import sldb.store.graph"
arrastra: core, models, runtime, store
módulos: 125
```

**125 módulos para un motor que no depende de ninguno.** La causa es que
`sldb/store/__init__.py` se ejecuta al importar cualquier submódulo suyo, y ese
`__init__` importa el almacén entero.

Es el mismo defecto de la Fase 0 —un reexport que contamina— en otra escala. Y es
el argumento más fuerte de este documento: **el eje del grafo ya es un
subsistema, y solo su dirección lo oculta**.

### 2. `edge_index` y `store/graph` son dos cosas, no una

Los conté juntos como «grafo» y es un error del primer mapa:

| | importa de fuera | qué es |
|---|---|---|
| `store/graph` (33) | **nada** | el motor: recorrido, análisis, consulta |
| `store/edge_index` (25) | `api.schema`, `store` | el constructor: deriva aristas de documentos |

El motor no sabe de documentos. El índice sí, y por eso depende del almacén. Son
el *qué* y el *de dónde*: separarlos es lo que permitiría usar el motor con
aristas de otra procedencia.

### 3. Sí hay motor de embeddings, y yo lo había negado

Mi primera versión de este documento decía «no hay motor de embeddings». Era
falso, y lo escribí porque busqué en el eje equivocado: miré `store/graph` y vi
que `similar_to` usa destinos compartidos, no vectores.

Pero existe `api/matching/` + `api/corpus/` — **19 archivos**:

```python
# api/matching/embedder_protocol.py
class Embedder(Protocol):
    def id(self) -> str: ...
    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...
```

```python
# api/matching/matcher.py
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    ...
```

Con caché de vectores en disco, invalidación por identidad del embebedor, y una
política declarable:

```python
# api/corpus/index_projection.py
"""`text_id` names the mapping so a change of representation invalidates the
index the same way a change of embedder does."""
```

Es un **puerto**, no una implementación: la aplicación inyecta el embebedor y sin
uno el sistema degrada a `difflib`. Por eso el eje no aparece en las dependencias
del proyecto — no hay ninguna biblioteca vectorial declarada, y aun así la
capacidad está construida.

Eso explica mi error y lo hace más interesante que un simple descuido: **el eje
mejor diseñado del sistema es invisible desde las dependencias**, porque su
diseño consiste precisamente en no tenerlas.

Y hay dos nociones de similitud, no una:

| | dónde | cómo | qué contesta |
|---|---|---|---|
| **estructural** | `store/graph/analysis/similarity.py` | destinos compartidos | «¿comparten etiquetas?» |
| **aproximada** | `api/matching/matcher.py` | coseno, o `difflib` | «¿hablan de lo mismo?» |

### 4. Los dos ejes mejor aislados son los dos adaptadores

`markdown-it-py` aparece en `core/ast` y en un archivo más.
`networkx` aparece en `store/graph` y en un archivo más.

Ninguna otra dependencia externa está tan confinada. Eso significa que las dos
fronteras más limpias del sistema son justamente las de los dos motores que se
podrían reemplazar: el analizador de superficie y el de grafo.

### 5. La superficie ya es un eje plural, y la autorada no

```
BaseASTHandler (abstracto)
   └── MarkdownASTHandler          ← la única implementación
```

Pero por el otro lado:

```
adaptadores derivados
   ├── python_scanner      (ast.parse)        1.279 documentos
   ├── parser scanner      (argparse)            89 documentos
   └── click_scanner       (click)        escrito, sin uso registrado
```

**Tres adaptadores derivados, una sola superficie autorada.** El eje de
superficie está ejercitado en la rama que deriva de código y no en la que un
humano escribe. Markdown no tiene hermanos.

---

## Qué le da identidad, entonces

De los diez ejes, no todos son identidad. Distingo tres grupos:

### Lo que define al sistema

| eje | por qué |
|---|---|
| **representación/ir** | `MeaningNode` + `SurfaceNode` es *la* idea: significado y superficie como dos proyecciones ancladas del mismo objeto |
| **contrato/modelos** | que un documento sea un tipo validado, no texto con convenciones |
| **superficie/ast** | que cualquier cosa con estructura determinista entre por la misma puerta |
| **render** | que se pueda volver al texto exacto — sin esto la representación es un volcado, no un lugar donde trabajar |

Esos cuatro son 56 archivos. Si se quitara cualquiera, lo que queda no es el
mismo sistema.

### Lo que lo hace útil

| eje | por qué |
|---|---|
| **persistencia** | sin almacén, cada operación reparte desde cero |
| **consulta** | direccionar un campo es lo que convierte documentos en datos |
| **grafo** | las relaciones entre documentos como objeto de primera clase |
| **adaptadores** | la prueba de que la superficie es plural |
| **recuperación** | encontrar por significado, no solo por dirección |
| **bitácora** | que una escritura deje rastro verificable |

Son 166 archivos. Valioso, reemplazable en principio.

### Lo que son accesorios

`enlaces` (7) y `semántica` (4) son chicos y dependen de persistencia. Podrían
plegarse en otros ejes sin que se pierda una capacidad.

---

## La frontera que este mapa sugiere

Si los ejes son reales, el sistema admite una división que hoy no tiene:

```
sldb-core       identidad: superficie, representación, render,        63 archivos
                contrato, runtime, identidad_y_hash
                + errores                                            80 archivos
                depende de: pydantic, markdown-it, jinja2

sldb-store      persistencia, consulta, bitácora, enlaces,           130 archivos
                semántica, caché, codec, migración, federación
                + índice_de_aristas
                depende de sldb-core

sldb-graph      el motor                                              33 archivos
                depende de networkx; 28 de 33 archivos ya autónomos

sldb-retrieval  recuperación por similitud                            19 archivos
                puerto Embedder; sin dependencia vectorial propia

sldb-adapters   python-ast, argparse, click                           22 archivos
                depende de sldb-core

sldb-api        los cuatro ejes de operación                         158 archivos
                depende de todo lo anterior
```

Seis piezas en vez de una, y los tamaños dicen algo: **la operación (158) es
mayor que la identidad (80)**. Eso es normal en una biblioteca madura, pero
conviene saberlo antes de decidir qué se publica por separado.

Dos de las seis están casi listas: `sldb-graph` tiene 28 de 33 archivos
autónomos, y `sldb-retrieval` solo depende de cuatro módulos externos a su eje.

Eso no es una propuesta de reescritura: es la constatación de que la
descomposición ya ocurrió en el código y no está declarada en ninguna parte. Es
el mismo patrón que S5: la frontera existe, nadie la escribió, y por eso nadie
puede decidir si algo la cruza.

---

### 6. Dos lenguajes de consulta para la misma intención

Dije que no lo había verificado; lo verifiqué:

| | operadores |
|---|---|
| `store/query_engine/where_parse.py` | `=` `!=` `<=` `>=` |
| `store/graph/language/field_condition.py` | `eq` `ne` `lt` `gt` `contains` `starts_with` `is_null` `is_not_null` |

**Dos vocabularios para filtrar por campo.** El del almacén usa símbolos y el del
grafo nombres, y el segundo tiene cuatro operadores que el primero no.

No es duplicación de código: son dos lenguajes que un usuario tiene que aprender
por separado para hacer lo mismo en dos ejes. Un cambio en uno no llega al otro, y
nada lo detecta — exactamente el antipatrón del camino doble.

---

## Lo que no sé

Declararlo importa, porque un mapa que no dice dónde termina invita a confiar de
más:

- **No sé por qué `click_scanner` existe sin uso.** 
  Verificado: ninguna referencia en `src/` ni en `tests/`, y ningún documento del
  almacén viene de él. Está escrito completo y nunca se ejercitó.
- **`store/journal/` lo encontré al final** y está en la tabla. Es un eje de
  bitácora: *«one hash-chained entry per write through `sldb.api`»*, con
  `verify_chain` que recorre las entradas comprobando el enlace de cada una con
  la anterior. Depende solo de `store.io` y `store.layout`. No sé si algo la
  verifica automáticamente.
- **El eje de recuperación lo encontré por error.** Lo había declarado ausente;
  existe y es el mejor diseñado. Eso sugiere que puede haber más capacidades que
  no vi, y que mi recorrido por dependencias externas fue mal criterio: el eje
  invisible era justamente el que no declara dependencias.
