# Las dudas, cerradas

Cada documento anterior terminó con una sección «lo que no sé». Esto las cierra
con medición, y donde no se puede medir lo dice.

---

## 1 · ¿`store.io` es superficie o deskops está mal acoplado?

**Es superficie, y falta una operación.**

Lo que deskops hace con los tres `load_*_index`:

```python
# deskops/deskops/operations.py:2801
store_index     = load_store_index(store_path)
models_index    = load_models_index(self.root / entry.models_index)
documents_index = load_documents_index(self.root / models_index.documents_index)
```

Tres lecturas en cadena para recorrer un almacén: índice de almacén → índice de
modelos → índice de documentos. **Nadie debería tener que conocer esa cadena.**

Y el lado de la escritura sí existe como operación: `api/stores/update_store_indexes.py`.
Hay operación para escribir los índices y no para leerlos, así que el consumidor
bajó a `store/io`.

**Veredicto**: no es acoplamiento indebido. Falta una operación de lectura —algo
como «dame los documentos de este almacén»— que oculte la cadena. Las tres
funciones pueden quedar internas una vez que exista.

---

## 2 · ¿El nudo del núcleo se parte?

**Sí, y las seis aristas están localizadas.**

| arista | archivo |
|---|---|
| representación → superficie | `core/node_handler.py#L3` |
| render → runtime | `core/renderer_engine/python_expr.py#L5` |
| render → contrato | `core/renderer.py#L12` |
| contrato → runtime | `models/structured_doc.py#L67` |
| runtime → superficie | `runtime/validation.py#L4` |
| runtime → contrato | `runtime/validation.py#L8` |

### Mi primera respuesta era falsa

Dije que mover `runtime/validation.py` —donde vive `extract_model_data`—
convertiría el nudo en jerarquía. Lo simulé:

```
tras mover runtime/validation.py:
  nudos restantes: [['composicion', 'contrato', 'render', 'representacion', 'superficie']]
```

**El nudo sigue.** Mover el archivo se lleva el problema de sitio sin resolverlo.

### El corte mínimo, calculado

Busqué por fuerza bruta el conjunto más chico de aristas cuyo corte deja un DAG,
sobre las 11 internas:

```
mínimo: cortar 4 aristas, peso total 6
   superficie      → render          peso 3
   representacion  → superficie      peso 1
   render          → runtime         peso 1
   contrato        → runtime         peso 1
```

Con archivo y línea:

| arista | dónde | qué importa |
|---|---|---|
| representación → superficie | `core/node_handler.py#L3` | `SharedNodeHandler` |
| render → runtime | `core/renderer_engine/python_expr.py#L5` | `python_expression_is_allowed` |
| contrato → runtime | `models/structured_doc.py#L67` | `extract_model_data`, diferido |
| superficie → render | `core/segments/instrumented_render.py#L16` | `SLDBRenderer` |

**Veredicto**: el núcleo es divisible cortando **4 aristas de peso total 6**, no
una. Las cuatro son reconocibles:

- dos ya están en `contracts/layers.toml` como R1 y R3
- `node_handler` importa un enrutador de superficie: una pieza de representación
  que conoce al que la va a manejar
- `instrumented_render` es un render instrumentado dentro del eje de superficie:
  está del lado equivocado

Esto corrige `06`, donde declaré el núcleo «indivisible». Es divisible, y el
precio está medido: 4 imports.

---

## 3 · ¿Importa romper a los consumidores?

**Importa para dos de cinco, y se puede graduar.**

| consumidor | último commit | imports profundos |
|---|---|---|
| **deskops** | **2026-10-03** | **101** |
| **kgdb** | 2026-09-20 | 14 |
| spec2viz | 2026-09-09 | 6 |
| hum-scrapper | 2026-06-03 | **0** |
| ontology | 2026-05-19 | **0** |

La correlación es perfecta y vale leerla: **los proyectos activos son los
acoplados; los inactivos usan solo la superficie.**

Dos lecturas posibles:

- los activos crecieron con la biblioteca y fueron tomando lo que necesitaban
- los inactivos se escribieron cuando la superficie era más chica, y por eso se
  quedaron dentro de ella

En ambos casos la conclusión es la misma: **la superficie estable existe y son
los 9 símbolos de demanda múltiple**. Lo que `hum-scrapper` y `ontology` usan
—`StructuredNLDoc` y poco más— no se va a romper con ninguna de las fases.

**Veredicto**: el riesgo está concentrado. deskops y kgdb hay que repararlos;
los otros tres no se enteran. Y como dijiste, eso va al final.

---

## 4 · ¿`adaptadores` son dos unidades o dos implementaciones?

**Dos unidades, sobre un contrato común de un archivo.**

Medido:

| | archivos |
|---|---|
| rama Python (`python_*`) | 8 |
| rama interfaz (`argument`, `command`, `parser`, `click_scanner`…) | 7 |
| compartido | `planned_document`, `projection`, `materialize`, `report` |

Y lo que realmente comparten:

```
materialize          usa: projection, planned_document
python_materialize   usa: planned_document
```

**`planned_document` es el único punto de encuentro.** Su propia docstring lo
dice:

> *Declare the planned-document contract shared by planning, persistence, and
> inspection. It does not write files, register models, or decide which documents
> need saving.*

Las dos ramas no comparten código de extracción: comparten el **contrato de
salida**. Cada una lee su mundo —árbol sintáctico de Python, estructura de
argparse— y produce el mismo tipo de documento planificado.

**Veredicto**: es la respuesta a la pregunta de la recursión. R2 existe en
`adaptadores`:

```
adaptadores
  ├── python-ast     8 archivos    absorbe cambios del AST de Python
  ├── interfaz       7 archivos    absorbe cambios de argparse/click
  └── planned_document            el contrato que ninguna posee
```

Si mañana se agrega un adaptador de otro lenguaje, se repara **dentro de
`adaptadores`**: implementa el contrato y nada más cambia. Eso es absorber su
propia variedad, que es la definición.

---

## 5 · ¿`persistencia` absorbe su variedad?

**No. Y encontré por qué.**

Busqué el versionado del formato de almacenamiento:

```
$ grep -rn "layout_version\|schema_version\|format_version" src/sldb/store
(nada)
```

**No existe.** La migración detecta versiones antiguas **por la existencia de
archivos**:

```python
# store/migration_legacy_layout.py:37
if store_index_path(store_path).exists() or not legacy_store_index_path(store_path).exists():
    return False
```

Es decir: «si existe el archivo nuevo, o no existe el viejo, no hay nada que
migrar».

### Por qué eso significa que no absorbe su variedad

Un cambio de formato hoy exige:

1. agregar una función `legacy_*_path` para la ruta antigua
2. agregar un paso de migración que la detecte por existencia
3. que cada lector sepa tolerar ambas formas

El paso 3 es el que escapa de la unidad. Los diagnosticadores ya lo habían
encontrado sin saber qué era:

> *tolerancia a almacenes escritos antes de `field_hashes`: «absent is unknown,
> never no-fields»* — vive en dos comentarios de código

Esa es una regla de compatibilidad de formato que vive en comentarios, no en el
formato. Con un número de versión sería una condición explícita.

**Veredicto**: `persistencia` es una unidad —produce más de lo que consume— pero
le falta el mecanismo para absorber cambios de formato. Un `layout_version` en el
índice de almacén es el diseño mínimo, y no está en ninguna fase del plan.

**Esto agrega una fase.**

---

## 6 · ¿La superficie autorada única es por diseño?

**No se puede resolver midiendo. Es decisión, y acá está el dato para tomarla.**

`BaseASTHandler` tiene una implementación concreta —Markdown— tras 317 commits.
Pero el adaptador de Python no la usa: tiene su propia rama con 8 archivos y
`ast.parse()`.

Es decir: **la abstracción de superficie no es el camino por el que entraron las
otras tres superficies.** Entraron por `selfdoc`, en paralelo.

Eso reencuadra la pregunta. No es «¿falta una segunda superficie autorada?». Es:

> ¿`BaseASTHandler` es la abstracción correcta, si las tres superficies que se
> agregaron después no la usaron?

Dos respuestas coherentes:

- **Markdown es la única superficie reversible**, y `BaseASTHandler` existe para
  eso. Las derivadas no son reversibles —no se reconstruye un `.py` desde un
  `PythonSymbolDoc`— así que nunca iban a usarla. Se declara y se cierra.
- **La abstracción quedó corta** y debería cubrir ambas.

La primera me parece más probable por la asimetría de reversibilidad, pero es una
lectura, no un hallazgo.

---

## 7 · ¿Por qué `click_scanner` existe sin uso?

**Porque está muerto, y eso oculta un defecto.**

```python
# src/sldb/selfdoc/click_scanner.py:8
import click
```

Sin `try`. Y:

```
$ grep -c click pyproject.toml
0
```

**`click` no es una dependencia del proyecto.** Está en el entorno local por
dependencias ajenas —typer, langgraph-cli, userpath— y por eso nadie lo notó.

No falla porque nadie lo carga:

```
$ python3 -c "import sldb.selfdoc; ..."
selfdoc importa sin click: True
```

En un entorno limpio, importar ese módulo da `ModuleNotFoundError`.

**Veredicto**: es un fallo latente que existe **porque** el código está muerto.
La prueba de que no se ejercita es que el defecto sobrevivió 317 commits.

Dos salidas honestas: declarar `click` como dependencia opcional y ejercitar el
adaptador, o retirarlo. Dejarlo es lo único que no sirve: parece una capacidad y
es un error de importación esperando.

### Y es la única

Revisé si el defecto estaba en otros sitios, comparando todos los imports de
`src/` contra las dependencias declaradas:

| módulo | veredicto |
|---|---|
| `click` | **no declarada** — el defecto |
| `pydantic_core` | legítima: `pydantic` la requiere (`pydantic-core==2.46.4`) |
| `a`, `the`, `its`, `option`, `definitions` | falsos positivos de mi búsqueda: prosa en docstrings |

Una sola dependencia ausente en 586 archivos, y está en el único módulo que nadie
carga. La correlación no es casual: **las dependencias de código vivo se declaran
porque fallan si no**.

---

## Lo que esto cambia en el plan

| | |
|---|---|
| el núcleo pasa de «indivisible» a «divisible si `extract_model_data` sale» | duda 2 |
| R2 existe, y es `adaptadores` | duda 4 |
| **falta una fase: versionado del formato de almacenamiento** | duda 5 |
| falta una operación de lectura de índices | duda 1 |
| el riesgo de ruptura es de 2 consumidores, no 5 | duda 3 |
| `click` falta en las dependencias y el defecto está vivo | duda 7 |

---

## Lo único que queda abierto, y no es una duda

**La decisión del congelamiento.** El README declara el proyecto congelado el
2026-09-07 y hubo 223 commits después. Las dos opciones están en
`contracts/identity.toml`:

1. congelado como producto, activo como autoaplicación
2. activo, y se declara qué es ahora

No es una duda que se cierre midiendo: es tuya.

Y la de la superficie autorada (duda 6), que también es decisión.
