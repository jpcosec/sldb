---
clase: objeto
tipo: arista
nombre: aristas contains y composes
estado: borrador
---

# Aristas `contains` y `composes`

## Qué es

Dos aristas que un modelo declara en su código y que el índice deriva de los valores de cada
documento. Nadie las escribe como arista: se escribe un valor en un campo y la arista aparece.

- `contains`: un campo del modelo, declarado en `__containment__`, guarda un documento hijo. El
  metadato lleva el nombre del campo y los modelos que la declaración permite
  (`src/sldb/models/builtin_relation_types.py:29`).
- `composes`: un campo compuesto del origen, declarado en `__compositions__`, arma su texto con
  el contenido de otro documento. La arista lleva el campo compuesto, el campo que guarda las
  referencias y la referencia tal como se escribió (`builtin_relation_types.py:30`).

`contains` ordena (padre e hijo) y `composes` genera (el texto del padre sale de los hijos).
Si cambia un hijo, `composes` dice qué padre queda desactualizado
(`src/sldb/store/edge_index/composition_edges.py:1`).

## Cómo se nombra

Hoy no tienen nombre propio: son la terna (origen, tipo, destino) con ids
`sldb://document/<Model>:<name>`. El destino de `contains` se escribe en el campo como id
`Model:name`, nombre o ruta; el de `composes` se escribe como ruta de proyecto
(`desk/tasks/task-a.md`) y el índice la resuelve al componerse
(`composition_edges.py:55`, `composition_targets.py:21`). Con la gramática propuesta (borrador) el
destino sería `[store:]st/<Model>/<doc>`, y el campo, un valor dentro del origen
(`st/<Model>/<doc>/<campo>`), que es donde vive la arista.

## Dónde se guarda

- La declaración: el código Python del modelo (`__containment__`, `__compositions__`), o
  `models create --containment/--compositions` y `models metadata edit` con los mismos
  indicadores (`src/sldb/cli/parsers/models2.py:71`, `:73`, `:85`, `:87`).
- Los valores: el Markdown del documento origen, en el campo declarado.
- La arista: derivada, `origin: schema`, en `.sldb_cache/edges/`. Un valor que no nombra
  documento se informa en `edges unresolved` y no queda arista
  (`src/sldb/cli/commands/edges.py:57`). Una referencia de `composes` que ningún documento
  posee se descarta (`composition_targets.py:28`).

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | Escribir un valor en el campo declarado: `docs create`, `docs update`, `fields create`/`append`. Declarar el campo: `models create --containment/--compositions` | `src/sldb/store/edge_index/declared_references.py:38`; `composition_edges.py:28`; `src/sldb/cli/parsers/fields.py:25` | **Sin confirmar:** poner un hijo (o una pieza) en el campo; la arista nace del valor. |
| Leer | `edges show`, `edges referrers`, `graph neighborhood`; `edges unresolved` para valores sin destino. Ninguno es propio de estos tipos | `src/sldb/cli/commands/edges.py:30`, `:57`; `src/sldb/cli/commands/edges_rewrite.py:20` | **Sin confirmar:** listar hijos o piezas de un documento y quién lo contiene. |
| Cambiar | `contains`: `edges rewrite --to` cambia el valor en todos los campos que lo nombran. `composes`: no existe (la arista no lleva `declared`); se cambia el campo con `fields update` | `src/sldb/api/edges/rewrite_values.py:30` | **Sin confirmar:** mover un hijo a otro padre, o cambiar el orden de las piezas. |
| Borrar | `contains`: `edges rewrite --remove` o `fields remove`. `composes`: `fields remove` en el campo de referencias | `src/sldb/api/edges/rewrite_values.py:30`; `src/sldb/cli/parsers/fields.py:25` | **Sin confirmar:** quitar el valor; la arista desaparece con él. |

Composición del texto (no es un verbo de la arista). `docs compose` solo expande `![[doc]]` y
`![[doc#Sección]]` (`src/sldb/links/composer.py:15`); no resuelve `__compositions__`. Esa
composición vive en el modelo: `render_payload` y `compose_field`
(`src/sldb/models/structured_doc.py:28`, `:34`) y sale por `serve` (`GET /document/segments`,
`src/sldb/cli/serve/segments_routes.py:5`). El registro de ejes lo dejaba como "sin verificar": con el código a la
vista, `docs compose` no toca `__compositions__`.

## Aristas que le llegan y que salen

- `contains` y `references` salen de los mismos campos: un campo declarado en las dos formas
  cuenta solo como `contains` (`declared_references.py:59`). Un campo `__references__`
  sin `__containment__` da `references`.
- `contains` sale del documento padre al hijo; `composes` del padre al documento que aporta
  una pieza. Un tipo `contains` autorado por un `RelationDoc` también existe (el código
  de `selfdoc` lo usa) y convive con éste (`src/sldb/store/edge_index/validation.py:62`).
- Los análisis del grafo las cuentan como derivadas, no autoradas
  (`src/sldb/store/graph/analysis/relations.py:17`).

## Qué lo mantiene correcto

- `allowed_models` de `__containment__` restringe qué modelos resuelve un valor
  (`declared_references.py:66`, `declared_resolution.py:71`).
- Cardinalidad: `contains` es `one_to_many` (un hijo, un padre) y se valida con `edges check`
  (`builtin_relation_types.py:29`; `validation.py:105`).
- `edges unresolved` lista los valores declarados que no nombran documento
  (`src/sldb/store/edge_index/unresolved_reference.py:23`).
- El hash del contrato del modelo incluye estas declaraciones, así que cambiarlas cambia el
  hash del contrato (`src/sldb/store/model_contract.py:104`). Sin verificar el hallazgo exacto
  que `stores check` informa.
- Sin verificar: que un ciclo de `contains` se rechace. `acyclic.py` solo vigila
  `semantic_parent` y `extends` (`src/sldb/store/edge_index/acyclic.py:12`).

## Abierto

- ¿`contains` y `composes` son aristas "de verdad" o proyecciones de un valor? Si son
  proyecciones, ¿"borrar la arista" significa borrar el valor?
- Los destinos de `composes` son rutas y los de `contains` ids: ¿se unifican en una dirección?
- ¿Cuántos hijos permite `contains` por padre cuando el campo es un escalar?

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

`contains` es que un nodo tenga cosas adentro; `composes` es la relación tipada de transclusión.

## Fuentes

`src/sldb/store/edge_index/declared_references.py`, `composition_edges.py`,
`declared_resolution.py`, `unresolved_reference.py`, `acyclic.py`, `validation.py`;
`src/sldb/models/builtin_relation_types.py`, `structured_doc.py`;
`src/sldb/api/edges/rewrite_values.py`; `src/sldb/links/composer.py`;
`src/sldb/cli/commands/edges.py`, `edges_rewrite.py`, `src/sldb/cli/parsers/models2.py`,
`fields.py`; `docs/architecture/references.md`, `segments-and-transclusion.md`.
