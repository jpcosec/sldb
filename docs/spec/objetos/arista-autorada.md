---
clase: objeto
tipo: arista
nombre: arista autorada
estado: borrador
---

# Arista autorada

## Qué es

Una arista que alguien escribe con un tipo: `references`, `implements`, `booked_by` o cualquier
tipo declarado por un `RelationTypeDoc`. Une dos documentos y lleva una condición opcional y
atributos libres. Con la condición y los atributos `sets` y `terminal` una arista es una
transición: hoy existen transiciones sueltas, no una máquina de estados (esa será un documento
declarado con un grafo de estados, de sldb, y todavía no existe).

Hay tres formas de crearla y las tres dan aristas de origen distinto:

- `RelationDoc`: un documento del store con `source_id`, `target_id`, `relation_type`,
  `condition`, `attributes` (`src/sldb/models/relation_doc.py:13`). Origen `relation_doc`.
- Un campo de referencia que el modelo declara en `__references__`. Origen `schema`, tipo
  `references`. Los campos `contains` y `composes` tienen su propia página
  (`arista-contains-y-composes.md`).
- `assert_edge` del MCP: crea un `RelationDoc` (`src/sldb/mcp/changes/typed.py:32`).

## Cómo se nombra

Hoy una arista no tiene dirección propia. Se nombra por el documento `RelationDoc:<name>` que la
declara, o por la terna (origen, tipo, destino) con los ids de nodo `sldb://document/<Model>:<name>`
(`src/sldb/store/edge_index/node_ids.py:21`). `RelationDoc.source_id` y `target_id` se escriben
como `Model:name`, o `store:Model:name` para un store enlazado
(`src/sldb/models/relation_doc.py:46`). Con la gramática propuesta (borrador) los extremos serían
`[store:]st/<Model>/<doc>`, y también `…#<sección>` o `…/<campo>`: el dueño fijó que una arista
puede terminar en una sección o en un valor. Hoy no puede: un extremo que no es un nodo
documento se informa como `endpoint-not-a-node` y la arista se descarta
(`src/sldb/store/edge_index/resolve.py:61`).

## Dónde se guarda

- `RelationDoc`: un Markdown del proyecto, ruta por defecto del modelo (`path` en `AssertEdge`
  la cambia: `src/sldb/mcp/changes/assert_edge.py:24`). La arista del índice es derivada.
- Campo de referencia: el Markdown del documento origen; la declaración `__references__` está en
  el código Python del modelo.
- El índice de aristas es derivado y vive en `.sldb_cache/edges/` (`src/sldb/store/models/model_edges.py:1`);
  nadie lo escribe.

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | `docs create --model RelationDoc`; `fields create`/`fields update`/`docs update` en un campo de referencia; `assert_edge` (MCP). No hay `edges create`. | `src/sldb/cli/parsers/docs1.py:13`, `fields.py:25`; `src/sldb/mcp/write/propose.py:14` | **Sin confirmar:** enlazar dos nodos con un tipo; el tipo decide por qué puerta se guarda. |
| Leer | `edges show [--to] [--relation] [--holds-for]`, `edges referrers`, `graph neighborhood`; MCP `neighbors`, `neighborhood` | `src/sldb/cli/commands/edges.py:30`; `src/sldb/cli/commands/edges_rewrite.py:20`; `src/sldb/mcp/read/graph.py:37` | **Sin confirmar:** listar las aristas de un nodo, filtradas por tipo y por condición. |
| Cambiar | Solo `RelationDoc`: `docs update` o `update_document` (MCP). `edges rewrite` NO sirve: solo mueve aristas `origin: schema`. | `src/sldb/api/edges/rewrite_values.py:30` | **Sin confirmar:** cambiar extremos, condición o atributos de la misma arista. |
| Borrar | `retract_edge` (MCP) borra el `RelationDoc`; `docs delete`; vaciar el campo de referencia (`edges rewrite --remove` solo para campos) | `src/sldb/mcp/changes/retract_edge.py:10`; `src/sldb/mcp/write/propose.py:39`; `src/sldb/cli/parsers/docs1.py:47` | **Sin confirmar:** declarar que la arista se retiró; queda dicha, con quién y por qué, y la consecuencia baja por las relaciones. Si la declara un campo, el valor se quita en el archivo y eso llega como cambio (corregido 2026-11-27 con los fundamentos). |

Transiciones (lectura, sin escritura). `edges_holding` devuelve las aristas que salen de un nodo
cuya condición se cumple sobre un sujeto, con `effects = {sets, terminal}`
(`src/sldb/api/edges/edges_holding.py:14`, `edge_effects.py:13`). `apply_effects` calcula el
payload nuevo y lo valida contra el modelo, pero no lo guarda (`apply_effects.py:12`). La
CLI solo expone la lectura: `edges show --holds-for` (`src/sldb/cli/commands/edges.py:40`).
Sin verificar: ningún comando de CLI ni herramienta MCP aplica una transición; `apply_effects`
solo aparece exportado en `src/sldb/api/__init__.py:41`.

## Aristas que le llegan y que salen

El tipo y los extremos son los del `RelationDoc`. Una arista `RelationDoc` hereda la condición y
el eje de su `RelationTypeDoc` si no trae los suyos, y si el tipo es `undirected` el índice
agrega la inversa con `reverse: true` (`src/sldb/store/edge_index/resolve.py:67`).
Los tipos propios de sldb (`references`, `contains`, `composes`, estructurales) también son
`RelationTypeDoc` que `edges init` registra (`src/sldb/api/edges/init_relations.py:15`). Los
análisis del grafo tratan `references` como derivada, no autorada
(`src/sldb/store/graph/analysis/relations.py:17`).

## Qué lo mantiene correcto

- El tipo debe existir como `RelationTypeDoc`; si no, `unknown relation type`
  (`src/sldb/store/edge_index/validation.py:81`).
- `source_types` y `target_types` del tipo limitan la clase de los extremos
  (`validation.py:83`); `cardinality` se valida al ingerir (`validation.py:105`).
- `condition` debe parsear con el lenguaje de predicados (`validation.py:88`).
- `attributes.terminal` booleano y `attributes.sets` mapa de escalares o listas de escalares:
  `src/sldb/models/transition_attributes.py:16`, usado por el validador de `RelationDoc`.
- `edges check` valida todo el índice; sale 1 solo con errores (`src/sldb/cli/commands/edges.py:46`).
- Cambiar un `RelationDoc` pasa por el mismo hash y guarda contra sobrescritura que cualquier
  documento; `retract_edge` y las actualizaciones van protegidas por `expected_source_hash`
  (`src/sldb/mcp/write/propose.py:31`).

## Abierto

- ¿Un `RelationDoc` y un campo de referencia son la misma cosa con dos puertas, o dos cosas? Hoy
  tienen origen distinto (`relation_doc` / `schema`), solo el primero se cambia con `docs update`.
- Un tipo de relación, ¿decide también por qué puerta se guarda la arista, o lo decide quien
  crea?
- Una transición que se aplica: ¿es un verbo de este objeto (cambiar el sujeto) o pertenece a
  la máquina de estados futura?

## Desde los fundamentos

**Qué es.** Una relación entre dos nodos, con un tipo, que alguien declara. Es un hecho de
adentro, con autor. Puede salir o llegar a una parte marcada, no solo a un documento.

**De qué principio cuelga.** 1, El valor sale de las relaciones. Y 6, Todo lo dicho es dicho por
alguien (que dos cosas se relacionen es algo que se declara).

**Qué contradice los niveles 1 y 2.**
- (a) Borrar: "Borrar ... `retract_edge` borra el `RelationDoc`; `docs delete`; vaciar el campo".
  Adentro no se borra: retirar una arista es declarar que se retiró; la arista queda dicha.
- (h) "Une dos documentos": une dos nodos. Un documento es un nodo más, y también lo es una parte
  marcada.
- (f) "`RelationDoc`: un Markdown del proyecto": lo que alguien declara vive adentro, no en un
  archivo de afuera. El Markdown puede ser una proyección.
- (c/5) "El tipo debe existir como `RelationTypeDoc`; si no, `unknown relation type`": los tipos
  salen de lo que entró, y no se exige un tipo antes de aceptar algo.
- (6) La página no dice quién declaró la arista ni en qué se apoya. Los hechos tienen autor.

**Qué queda igual.** Una arista tiene tipo, condición opcional y atributos. Las transiciones
sueltas. La arista puede terminar en algo metido dentro de un nodo. Las comprobaciones de tipo
de extremos y de condición siguen valiendo como reglas, que son nodos.

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

Es una relación tipada entre nodos. Puede salir o llegar a algo metido dentro de un nodo.

## Fuentes

`src/sldb/models/relation_doc.py`, `relation_type_doc.py`, `transition_attributes.py`,
`builtin_relation_types.py`; `src/sldb/api/edges/` (`edges_holding.py`, `apply_effects.py`,
`edge_effects.py`, `init_relations.py`, `rewrite_values.py`); `src/sldb/mcp/changes/`,
`src/sldb/mcp/write/propose.py`, `src/sldb/mcp/read/graph.py`;
`src/sldb/store/edge_index/` (`doc_kinds.py`, `resolve.py`, `validation.py`, `node_ids.py`);
`src/sldb/cli/commands/edges.py`, `edges_rewrite.py`; ayuda `sldb edges --help`;
`docs/architecture/one-address-grammar-two-spaces.md`.
