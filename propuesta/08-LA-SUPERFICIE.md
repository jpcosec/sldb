# La superficie

Tenías razón en las dos cosas: **ya está pasando**, y los consumidores se reparan
al final.

Eso cambia el diseño. No hay que inferir qué superficie debería existir: hay que
**leer la que los consumidores ya construyeron** y declararla.

---

## Lo que ya está pasando

Cinco proyectos consumen `sldb`. Lo que piden, medido:

| consumidor | símbolos |
|---|---|
| kgdb | 31 |
| deskops | 26 |
| spec2viz | 8 |
| hum-scrapper | 1 |
| ontology | 1 |

**53 símbolos distintos en total.** Y nueve los pide más de uno:

| símbolo | consumidores |
|---|---|
| `StructuredNLDoc` | **4** |
| `resolve_model_ref` | 3 |
| `load_store_index` | 3 |
| `load_models_index` | 3 |
| `store_exists` | 2 |
| `project_root` | 2 |
| `load_documents_index` | 2 |
| `find_local_store` | 2 |
| `extract_model_data` | 2 |

Eso es una superficie emergiendo sola. Nadie la diseñó y aun así hay un núcleo
de nueve símbolos con demanda múltiple.

---

## Los 53, agrupados por unidad

Y acá está el dato que hace que esto funcione: **se agrupan casi perfectamente
por unidad viable**.

| unidad | símbolos | ejemplos |
|---|---|---|
| **grafo** | 13 | `GraphSnapshot`, `KnowledgeNode`, `FacetPayload`, `StructuredQuery`, `QueryResult` |
| **operación** | 12 | `open_store`, `init_store`, `describe_field`, `diagnose_store`, `track_document` |
| **núcleo** | 11 | `StructuredNLDoc`, `extract_model_data`, `RelationDoc`, `SLDBValidationError` |
| **persistencia** | 7 | `load_store_index`, `store_exists`, `project_root`, `find_local_store` |
| **la interfaz** | 6 | `resolve_model_ref`, `get_store_context`, `registered_model`, `parse_data_value`, `ModelCLI`, `DocCLI` |
| sin ubicar | 4 | `Edge`, `init_store`, `BUILTIN_RELATION_TYPES`, `VocabularyTerm` |

La superficie que los consumidores pidieron **refleja las unidades que el
análisis encontró**, sin que nadie coordinara las dos cosas. Es la confirmación
más fuerte de que las unidades son reales: si fueran una invención mía, los
símbolos estarían repartidos al azar.

---

## El estado actual, sin adornos

De los 53 símbolos:

| | |
|---|---|
| ya están en algún `__all__` | **32** |
| no están exportados | **21** |

Y entre los 21 hay tres clases de problema distintas.

### Privados importados desde fuera

```python
# kgdb/src/kgdb/ingest/typed.py:42
from sldb.store.graph.ingest_sldb import _base_provenance, _collect_semantic_tags
```

Dos funciones con guion bajo, importadas por otro proyecto. El guion bajo decía
«esto es interno» y nadie podía hacerlo cumplir.

**No es culpa de kgdb**: necesitaba la capacidad y no había puerta. Es el mismo
patrón que las cinco funciones de lectura de índice.

### La interfaz usada como biblioteca

Hay que separar dos casos, porque los conté juntos y no son lo mismo.

**Legítimo**: `deskops` invoca `sldb.cli.main` desde sus pruebas, para ejercitar
la interfaz de punta a punta. Seis archivos de prueba lo hacen y está bien: es
probar el transporte como transporte.

**Defecto**: código de producción importando funciones de `cli/`.

```
deskops/deskops/operations.py        from sldb.cli.utils import parse_data_value
deskops/deskops/identity.py          from sldb.cli.store_context import get_store_context
deskops/deskops/bootstrap.py         from sldb.cli.commands.model import ModelCLI
deskops/deskops/cli/.../repo.py      from sldb.cli.model_utils import registered_model, resolve_model_ref
deskops/deskops/cli/.../promote.py   from sldb.cli.commands.doc import DocCLI
spec2viz/spec2viz/deskops.py         from sldb.cli.model_utils import resolve_model_ref
```

**Seis funciones de la interfaz usadas por código de producción de dos
proyectos.** `resolve_model_ref` es la más pedida: tres consumidores.

Eso significa que seis operaciones **no existen como operaciones**: existen
envueltas en el transporte. El contrato de capas dice que el transporte «no debe
contener lógica que un programa necesite»; acá la contiene y hay dos programas
que la necesitan.

El caso extremo es `ModelCLI().add(args)`: `deskops` construye un objeto de
línea de comandos y le pasa argumentos simulados para registrar un modelo.

### Capacidades sin nombre público

`extract_model_data` (37 usos en deskops), `project_root`, `store_exists`,
`track_document`, `parse_data_value`, `render_model_markdown`. Existen, se usan,
y ningún `__all__` las menciona.

---

## El diseño

Una superficie por unidad, que es lo que los datos piden:

```python
sldb                      # el núcleo: lo que define al sistema
    StructuredNLDoc, extract_model_data, SLDBError…

sldb.store                # persistencia: abrir, leer, localizar
    open_store, store_exists, project_root, find_local_store,
    load_store_index, load_models_index, load_documents_index

sldb.graph                # el motor
    GraphSnapshot, KnowledgeNode, StructuredQuery, QueryResult…

sldb.ops                  # las operaciones compuestas
    init_store, track_document, untrack_document, describe_field,
    diagnose_store, update_store_indexes, resolve_model_ref

sldb.adapters             # derivar de código
sldb.retrieval            # similitud aproximada
```

Seis puertas, una por unidad. Todo lo demás es interno y se puede mover.

### Las tres reglas

**1. Un consumidor importa solo de estos seis.** Un import de
`sldb.store.io.utils` o `sldb.cli.commands.model` es un defecto, y la puerta lo
puede detectar porque los consumidores están en el mismo árbol.

**2. Lo que un consumidor ya usa, entra.** No se diseña desde cero: los 53
símbolos son el punto de partida. Si `kgdb` necesita `_base_provenance`, esa
capacidad existe y le falta nombre — no se le quita, se le pone nombre.

**3. Lo que se saca, se registra.** Quitar un símbolo de la superficie es un
cambio incompatible y va al historial de cambios. Agregar, no.

---

## El orden, corregido con lo que dijiste

Tu criterio —romper ahora, reparar al final— simplifica el plan. Antes tenía el
contrato de superficie bloqueando todo por miedo a romper consumidores. Ya no.

| | qué | por qué en este orden |
|---|---|---|
| **1** | declarar los 53 en seis puertas | es inventario, no diseño: ya están identificados |
| **2** | nombrar lo que hoy es privado | `_base_provenance`, `_collect_semantic_tags` y los 19 restantes |
| **3** | subir a operaciones las 6 funciones de `cli` | `resolve_model_ref`, `get_store_context`, `registered_model`, `parse_data_value`, y lo que hacen `ModelCLI.add` y `DocCLI` |
| **4** | la puerta de superficie | congela el conjunto; un cambio sin registrar falla |
| **5** | `tests/<unidad>/` | la auditoría que falta en las cinco |
| **6** | los 32 alfileres | separación física |
| **7** | **reparar los consumidores** | al final, como dijiste |

Los pasos 1–3 no rompen nada: solo **agregan** nombres públicos. Romper empieza
en el 6, y para entonces la superficie ya existe y los consumidores se adaptan a
ella en un solo paso.

---

## Lo que esto resuelve del diagnóstico

| hallazgo original | con la superficie declarada |
|---|---|
| «336 definiciones públicas sin frontera» | 53 son superficie, el resto interno |
| «nada marca qué es estable» | seis puertas, y lo de fuera se puede mover |
| S4 sin mecanismo | la puerta de superficie es el mecanismo |
| `enlaces` «capacidad sin superficie» | `compose_document` entra o se declara interna |

Y resuelve el problema que no había visto: **el sistema no tiene demasiada
superficie, tiene la superficie en el lugar equivocado**. 53 símbolos repartidos
entre seis ejes, veintiuno sin nombre público, dos con guion bajo delante.

---

## Lo que queda por decidir

Tres cosas que son decisión tuya, no hallazgo:

**`store.io` y `store.layout`: ¿superficie o acoplamiento?** Las siete funciones
de lectura de índice las usan tres consumidores. Mi lectura es que son superficie
legítima —son las preguntas básicas que se le hacen a un almacén— pero exponerlas
congela el formato de los índices.

**`sldb.ops` <!-- gone --> o `sldb.api`.** El paquete se llama `api` y la unidad «operación» es
una fachada. Mantener el nombre es menos trabajo; `ops` dice mejor qué es.

**Qué hacer con los 13 símbolos de `grafo`.** Si el motor se extrae como paquete
aparte, su superficie es la del paquete y no una puerta de `sldb`. Eso depende de
si se publica separado, que es la decisión del punto 9 de la lista anterior.
