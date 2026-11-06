# Aristas como máquina de estados: condiciones y efectos de transición

Estado (2026-11-06): contrato e implementación del nodo GO09 del plan
`desk/drawer/plans/grafo-operable`. Un `RelationDoc` declara una arista autorada; cuando la
arista es una transición, su efecto sobre el sujeto viaja con ella en `attributes`, y sldb lo
resuelve y lo aplica sin persistir. Las condiciones se escriben en el lenguaje de
[`rules-language.md`](rules-language.md). Fuera de este nodo: findings por arista y el orden
pinneado → reglas (GO08), el retiro de `sets_status`/`terminal` del YAML de deskops
(G_CONSUMER) y los shims (GO10).

## 1. La convención de `RelationDoc.attributes`

`attributes` es libre (multiplicidad, rol...), salvo dos claves con significado fijo:

| Clave | Valor | Significado |
|---|---|---|
| `sets` | mapa campo → valor | Lo que la transición escribe en el sujeto, p. ej. `{status: closed}`. Cada valor es un escalar YAML (`null` incluido) o una lista de escalares. |
| `terminal` | booleano | Marca de transición terminal; sldb solo la transporta. |

Defaults: `attributes`, `sets` o `terminal` ausentes o `null` equivalen a `sets = {}` y
`terminal = false`. Las demás claves de `attributes` se conservan en el documento (y en
`metadata.attributes` de la arista del índice) y no entran a los efectos.

La convención es un validador pydantic de `RelationDoc`
(`sldb.models.transition_attributes.check_transition_attributes`): escribir un `RelationDoc`
que la viola, por cualquier vía de escritura (`create_document`, `save_document_payload`,
`sldb docs create|update`), levanta el `ValidationError` del modelo en el campo `attributes`
con el motivo. Se rechaza:

- `attributes` que no es un mapa;
- `sets` presente que no es un mapa;
- `terminal` presente que no es booleano;
- un valor de `sets` que es un mapa;
- un valor de `sets` que es una lista con una lista dentro.

## 2. `{campo}` en los valores de `sets`

Los valores string de `sets` (y cada string de una lista de `sets`) admiten `{campo}` con la
sintaxis y la fuente de `where_subject` (`fill_braces`): el campo de primer nivel del payload
del sujeto. La sustitución deja un string: el escalar se escribe en su forma YAML
(`true`/`false`, números como YAML los escribe, p. ej. `3`, `1.5`, `1.0e+20`) y un string tal
cual, sin comillas ni escape; nunca el `repr` de Python. Ejemplo: `sets: {closed: "{done}"}`
con `done = True` da `closed = "true"`.

Un `{campo}` ausente, `null` o no escalar en el sujeto hace que la arista **no se cumpla**,
igual que en una condición. `sets: {x: null}` (null literal, sin llaves) sí es asignable y
escribe `null`.

## 3. `edges_holding` y `EdgeRecord.effects`

`sldb.api.edges_holding(store, export_id, subject, relation=None, ...)` devuelve las aristas
que salen de `export_id` cuya condición (la propia, o la de su tipo de relación) se cumple
sobre `subject`, evaluada con `payload_holds`. Cada `EdgeRecord` devuelto lleva:

```python
edge.effects == {"sets": {...resueltos...}, "terminal": bool}
```

Una arista sin `attributes` da `{"sets": {}, "terminal": False}`. La resolución vive en
`sldb.api.effects_of(attributes, subject)` (`None` cuando un `{campo}` no resuelve).

`EdgeRecord.effects` es opcional (default `None`) y solo lo llena `edges_holding`. Mientras
es `None` no aparece en `model_dump`, `model_dump_json` ni en ninguna salida: `edges_from`,
`edges_to`, `sldb edges show` y los shards del índice no cambian. GO08 agregará `findings` a
cada `EdgeRecord` sin tocar `effects`.

## 4. `apply_effects`

```python
sldb.api.apply_effects(subject: dict, effects: dict, model: type[StructuredNLDoc]) -> dict
```

Función pura: devuelve una copia del sujeto donde cada clave de `effects["sets"]` reemplaza
entera la clave de primer nivel del mismo nombre, o la agrega (sin fusión anidada). Valida el
payload completo resultante contra `model` y levanta su `ValidationError` si no valida; un
valor de `sets` que es un mapa o una lista anidada levanta `ValueError`. Nunca persiste.

`model` es la clase del modelo del sujeto. Quien solo tiene su `Model:name` la obtiene con el
resolutor de modelos del store (`sldb.api.load_registered_model(store, name, pythonpath).model_type`,
el mismo que usa la escritura de documentos); `apply_effects` no resuelve nombres.

## 5. Ejemplo

```yaml
# RelationDoc e-submit
source_id: State:open
target_id: State:review
relation_type: moves_to
condition: status = "open"
attributes:
  sets: {status: review, closed: "{done}"}
  terminal: false
```

```python
[edge] = api.edges_holding(store, "State:open", {"title": "i", "status": "open", "done": True}, "moves_to")
edge.effects  # {"sets": {"status": "review", "closed": "true"}, "terminal": False}
api.apply_effects(subject, edge.effects, Item)  # {..., "status": "review", "closed": "true"}
```

Pruebas: `tests/api/test_edge_effects.py`.
