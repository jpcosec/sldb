# GraphBackend: the seam under every graph analysis

Estado (2026-11-05): contrato del nodo GO03 del plan
`desk/drawer/plans/grafo-operable` (gate G_SEAM). Fija la costura `GraphBackend` sobre
networkx. Cualquier motor futuro —Kùzu, Neo4j, Datalevin— entra detrás de esta costura; las
reglas y los comandos no lo ven. La semántica de los predicados vive en
[`rules-language.md`](rules-language.md); la proyección real llega en GO04 y el evaluador
completo en GO05.

## El protocolo

`src/sldb/store/graph/backend/protocol.py` declara tres operaciones:

```python
load(index, projection) -> None
eval(predicate, subject=None) -> list[finding]
analyze(op, **args) -> resultado
```

- **`load`** guarda en la instancia el índice compuesto y la proyección. El índice es el
  objeto que devuelve `sldb.store.edge_index.compose.compose_edge_index`: nodos y aristas ya
  resueltos. **Compose queda fuera del backend**: él lo produce y se lo entrega a `load`.
  Devuelve `None`.
- **`eval`** evalúa un predicado sobre un sujeto. El sujeto es un payload (`dict`) o un
  `export_id` (`str`). Si es un `export_id`, se lee la proyección cargada; sin proyección o
  sin ese id, `eval` levanta `ValueError("sin proyección para <id>")`. En GO03 la proyección
  real siempre es `None` (la produce GO04), así que los tests pasan el sujeto como payload.
- **`analyze`** responde una pregunta de grafo completo con los argumentos que las
  operaciones ya reciben. Hoy son las diez de `sldb.api.graph.analyze`: `path`, `paths`,
  `cycles`, `order`, `layers`, `components`, `islands`, `isolated`, `central` y `similar`;
  las seis de la CLI (`path`, `cycles`, `order`, `components`, `central`, `similar`) son el
  subconjunto que el contrato del nodo nombra.

El backend **nunca expone su grafo interno**. Se guarda en un atributo privado y las
operaciones lo usan dentro; no hay accesor público ni fuga del `MultiDiGraph` de networkx.

La implementación actual, `NetworkXBackend`, envuelve `sldb.store.graph.analysis` sin
cambiar ninguna respuesta.

## eval en GO03

Acepta el subconjunto de GO02 **sin caminos**: `has`, `nonempty`, `in`, `~`, `model <=`,
comparaciones `= != < <= > >=`, `and`/`or`/`not`, paréntesis y sustitución `{campo}` desde
el payload del sujeto. Reutiliza `where_lookup` para las rutas de campo,
`where_subject.fill_braces` para la sustitución y `WherePredicateError` para lo que no
parsea.

Un predicado con camino —`any(...)`, `all(...)`, `none(...)`, `count(...)`, `rel:<tipo>`,
`^campo`, pasos con `+`— levanta `NotImplementedError` hasta GO05.

Cada resultado es un finding de la forma fijada en `rules-language.md` §4 y §6:

```json
{"node": "Task:a", "holds": "true", "clause": "status = \"open\"", "seen": {"status": "open"}}
```

## Selección por store.yaml

`.sldb/store.yaml` puede declarar:

```yaml
graph_backend: networkx
```

- **Ausente**: se usa `networkx` (también si el store no tiene declaración).
- **`"networkx"`**: aceptado.
- **Cualquier otro valor**: el store falla al cargar la declaración con el mensaje exacto
  `graph_backend <valor> no admitido; admitidos: ["networkx"]`.

La resolución vive en `src/sldb/api/graph/analyze.py` (`backend_for`, que llama a
`declared_graph_backend` en `src/sldb/api/stores/store_declaration.py` y pasa el nombre a
`make_backend` en `src/sldb/store/graph/backend/__init__.py`). Así el paquete `store` no
importa nada de `sldb.api`.

Para tests y para futuros motores, un llamador de Python puede inyectar una instancia:
`graph_path(..., backend=motor)`, `GraphAnalysisCLI(backend=motor)` o
`GraphCLI(backend=motor)`. `store.yaml` sigue siendo el selector de producción.

## Regla de la costura

Toda capacidad de análisis de grafo entra por `analyze`; toda evaluación de predicados entra
por `eval`; toda lectura de un índice entra por `load`. Un motor nuevo implementa las tres
operaciones y nada más cambia: ni las reglas, ni la API, ni la CLI conocen networkx.

## La proyección del payload (GO04)

Estado (2026-11-06): contrato del nodo GO04. `load` lee el índice de aristas; desde la
versión 5 (`EDGE_INDEX_VERSION`) cada nodo de documento lleva, persistidos en su shard,
cuatro campos de primer nivel de `EdgeNodeRecord` (no van en `facets`, que sigue siendo solo
de lectura). Los demás nodos (secciones, modelos, campos, tags...) los dejan vacíos y el
shard no los escribe.

- `payload`: mapa plano campo → valor con los campos de nivel superior del payload extraído
  cuyo valor es escalar (str, int, float, bool) o lista de escalares (incluida la vacía). Si
  el modelo declara `__indexed__`, exactamente esos nombres; un nombre ausente en el payload
  de un documento se omite.
- `field_hashes`: el mapa completo de `DocumentEntry.field_hashes` (todos los campos, no solo
  los proyectados).
- `source_hash`: el `hash_c` de la `DocumentEntry`.
- `contract_signature`: sha256 del JSON canónico (claves ordenadas, UTF-8, sin espacios) de
  `{fields, references, containment, compositions}`: todos los nombres de campo del modelo
  tras la herencia y los nombres de `__references__`, `__containment__` y `__compositions__`,
  ordenados; un atributo ausente aporta la lista vacía. Solo nombres.

### Omisiones

- Un campo cuyo valor es un diccionario (un bloque `dict`, un submodelo) o una lista con algún
  elemento no escalar (una tabla) no se proyecta: se lee con `--where` o con el documento.
- Un campo nulo no se proyecta: la extracción lo descarta (`exclude_none`), así que en la
  proyección está ausente, igual que un campo que el documento no tiene.
- Los valores son los del payload en modo JSON: una fecha o un enum llegan como cadena.
- Un modelo que no se puede cargar al reconstruir deja `payload` vacío y `contract_signature`
  en `""`; abrir el store no falla.
- Las relaciones, los tipos de relación y las anclas no son nodos de documento: no llevan
  proyección.
- `__indexed__` se valida al cargar el modelo (`resolve_model_ref`): un nombre que no es campo
  del modelo tras la herencia, o cuyo tipo declarado no es escalar ni lista de escalares, es
  `SLDBModelError` con el modelo y el campo. Cuentan como escalares los tipos cuya forma JSON
  es escalar (enums, fechas, UUID, `Literal` de escalares).
- `__indexed__` no entra en `contract_signature` (el contrato fija sus cuatro claves): cambiarlo
  en un modelo con documentos ya indexados reproyecta un documento cuando se reconstruye su
  shard (su texto cambia o la reconstrucción es completa), no antes.

### Staleness

`EdgeIndex.stale` nombra un documento cuando su shard falta, se construyó desde otro hash o
bajo otra `EDGE_INDEX_VERSION` (un shard de versión 4 queda stale al abrir y entra al dirty
set; la siguiente escritura o `stores build` lo reconstruye), cuando el texto del archivo ya
no da el `source_hash` del shard (edición fuera de sldb) o cuando la firma del modelo cargado
difiere de la guardada (por ejemplo, un campo nuevo en `__references__`). Las dos últimas se
comprueban en cada lectura del índice (`compose_edge_index` con `model_type_of`, que pasan
`load_edge_index` y `rebuild_edges`), no se guardan con el índice compuesto: ninguna mueve un
shard. El hash de cada archivo se recuerda mientras su mtime y su tamaño no cambien.

### Consulta

`StructuredQuery` filtra sobre la proyección con
`FacetFilter(facet="payload", conditions=[FieldCondition(field=..., op=..., value=...)])`. Se
evalúa sobre lo que dice el shard: nunca se re-extrae un documento. Solo los nodos de documento
tienen la facet; los demás no casan con un filtro `payload`. Sobre un campo ausente (nulo) solo
deciden `is_null` e `is_not_null`; sobre una lista, `contains` es pertenencia, `eq` / `ne`
comparan la lista entera, `gt` / `lt` / `starts_with` dan false, `is_null` false e
`is_not_null` true. `eq` / `ne` usan la igualdad de Python sin coerción (`1 == 1.0`,
`True == 1`); una comparación que Python no puede ordenar da false. Un filtro sobre un campo
que ningún modelo proyecta (diccionario, lista no escalar, fuera de `__indexed__`, o inexistente)
es `SLDBGraphArgumentError` con el nombre del campo; un campo proyectable ausente en todos los
payloads da el conjunto vacío. La lista de campos proyectables por modelo vive en el shard del
modelo (`ModelEdges.projected_fields`) y el índice compuesto la expone en
`EdgeIndex.payload_fields`. Las facets existentes (`identity`, `semantics`, `source`...) no
cambian, y `GraphNode` no gana claves.
