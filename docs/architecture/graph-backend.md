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
