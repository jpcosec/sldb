---
clase: objeto
tipo: nodo
nombre: tipo de relación
estado: borrador
---

# Tipo de relación

## Qué es

Un tipo de relación (`RelationTypeDoc`) declara el verbo de una arista autorada: su nombre
(`implements`, `booked_by`), entre qué clases de nodo conecta, su dirección, su cardinalidad, el
eje de predicado al que responde y una condición que toda arista de ese tipo hereda. Es un
documento del store y, a la vez, un nodo `relation_type` del grafo. Sin un tipo registrado, el
índice informa la arista como error. Los tipos que sldb mismo produce (`has_model`, `links_to`,
`references`, …) se guardan también como estos documentos.

## Cómo se nombra

Hoy hay dos nombres, y no son el mismo:

- Nodo del grafo: `sldb://relation_type/<name>`, con el campo `name` del documento
  (`src/sldb/store/edge_index/node_ids.py:43-45`, `src/sldb/store/edge_index/doc_kinds.py:40`).
- Documento: `RelationTypeDoc:<nombre-del-doc>`. Los de sldb se llaman `reltype-<name>`
  (`src/sldb/models/builtin_relation_types.py:44-46`); el nodo guarda ese nombre en
  `semantics.doc` (`doc_kinds.py:41`). El nombre del documento y el `name` del tipo pueden diferir.
- En una arista se escribe el `name` (`relation_type` de `RelationDoc`;
  `src/sldb/mcp/changes/assert_edge.py:19-21`).

Con la gramática propuesta (borrador): el tipo es un documento y se nombra como tal,
`[store:]st/RelationTypeDoc/<doc>`; el espacio `sldb://relation_type/` desaparece
(`one-address-grammar-two-spaces.md`, decisión 2 y 3).

## Dónde se guarda

Un Markdown de un modelo `RelationTypeDoc`, con front matter (`name`, `direction`,
`cardinality`, `axis`, `source_types`, `target_types`, `condition`) y una sección
`Description` (`src/sldb/models/relation_type_doc.py:12-44`). Los de sldb se escriben en
`sldb/relation_types/` (`src/sldb/api/edges/builtin_relation_writes.py:26`). El nodo del grafo es
derivado: lo calcula el índice de aristas desde el documento (`doc_kinds.py:38-43`). Antes de
poder crear uno hay que registrar los modelos `RelationTypeDoc` y `RelationDoc` con `edges init`
(`src/sldb/api/edges/init_relations.py:15-33`).

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | Como cualquier documento: `docs create --model RelationTypeDoc`. `edges init` crea solo los tipos de sldb. MCP: `CreateDocument` con ese modelo, solo con nivel de escritura 2 | `src/sldb/cli/parsers/docs1.py:13-20`, `src/sldb/cli/commands/doc.py:45-48`, `src/sldb/cli/commands/edges.py:21-23`, `src/sldb/mcp/mutability.py:16,30-32` | **Sin confirmar:** declarar un verbo nuevo; el tipo de relación es un documento como otro, con la misma operación. |
| Leer | MCP `list_relation_types` y `describe_relation_type`. En CLI no hay comando propio: se lee como documento (`docs show`, `docs list`) o se ve su efecto en `edges check` | `src/sldb/mcp/read/models.py:35-46`, `src/sldb/cli/parsers/docs1.py:54`, `src/sldb/cli/commands/edges.py:46` (buscado en `src/sldb/cli/parsers/{edges,graph,tags}.py`) | **Sin confirmar:** devolver sus atributos; listar los tipos como se listan los modelos. |
| Cambiar | Como documento: `docs update`; MCP `UpdateDocument` (nivel 2). El lote del MCP simula el índice con el tipo nuevo antes de aplicar | `src/sldb/cli/commands/doc.py:63-73`, `src/sldb/api/documents/batch_simulation.py:42-43,74-84` | **Sin confirmar:** cambiar el contrato del verbo; las aristas existentes se revisan contra el contrato nuevo. |
| Borrar | Como documento: `docs delete` (borra el archivo) o `docs untrack`; MCP `DeleteDocument` (nivel 2). Las aristas de ese tipo no se tocan: quedan como error "unknown relation type" | `src/sldb/cli/commands/doc.py:90-102`, `src/sldb/mcp/changes/delete_document.py:10-15`, `src/sldb/store/edge_index/validation.py:81` | **Sin confirmar:** retirar el verbo; qué pasa con sus aristas es la pregunta abierta. Sin verificar si el lote del MCP rechaza la baja cuando hay aristas. |

## Aristas que le llegan y que salen

- `applies_to_source` y `applies_to_target`: tipo → modelo, una por cada nombre de `source_types`
  y `target_types` (`doc_kinds.py:42`; tipos en `builtin_relation_types.py:25-26`). La crea el
  índice, no un autor.
- `names`: ancla → tipo de relación, cuando el ancla apunta a `relation:<name>`
  (`src/sldb/store/edge_index/anchor_targets.py:31`).
- Las aristas **de** ese tipo (autoradas con un `RelationDoc`) no tocan el nodo tipo: lo
  referencian por nombre en su campo `relation_type`.
- `RelationTypeDoc` es un documento, así que además tiene `has_document` desde su modelo y
  puede llevar `tagged_as`.

## Qué lo mantiene correcto

- `edges check` valida cada arista contra su tipo: tipo desconocido, clases de extremo
  permitidas, cardinalidad y condición que parsea
  (`src/sldb/store/edge_index/validation.py:36-47,76-102,105-113`).
- Los tipos que sldb produce se comparan con la definición de sldb, que gana sobre la del store
  (`validation.py:62-66`).
- El modelo `RelationTypeDoc` valida el documento; `direction` y `cardinality` son enumerados
  (`relation_type_doc.py:48-57`).
- El campo `axis` dice que el tipo se registra como predicado; el código solo registra los de
  sldb (`src/sldb/api/edges/builtin_relation_writes.py:73-81`). Para los autorados, sin verificar.
- Escribirlo exige el nivel 2 del MCP, porque cambia qué es válido
  (`src/sldb/mcp/mutability.py:12-16`).

## Abierto

- Al borrar un tipo con aristas: ¿se borran las aristas, se rechaza mientras existan, o quedan
  como error (hoy)?
- Cambiar el `name` de un tipo cambia su nodo y deja huérfanas las aristas que lo usaban. ¿Es un
  cambio con reescritura de aristas, o un borrar y crear?
- ¿Un tipo de sldb (`has_model`, `references`, …) puede borrarse o cambiarse, o es de solo
  lectura? Hoy sldb impone su definición sobre la del store para las aristas derivadas.
- Si una arista puede terminar en una sección o un valor, ¿`source_types` y `target_types` se
  expresan por modelo del documento, o hay que poder nombrar secciones y valores?

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

Es el tipo de una relación. En kimun las relaciones se tipan (herencia, transclusión, hook y otras); `RelationTypeDoc` es la forma de sldb de declarar un tipo.

## Fuentes

- `desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`, `desk/drawer/plans/spec-de-producto-de-sldb/README.md`
- `docs/architecture/one-address-grammar-two-spaces.md`, `docs/architecture/edges.md`
- `src/sldb/models/{relation_type_doc,builtin_relation_types}.py`
- `src/sldb/store/edge_index/{node_ids,doc_kinds,validation,anchor_targets}.py`
- `src/sldb/api/edges/{init_relations,builtin_relation_writes}.py`, `src/sldb/api/documents/batch_simulation.py`
- `src/sldb/cli/commands/{edges,doc}.py`, `src/sldb/cli/parsers/{edges,docs1}.py`
- `src/sldb/mcp/{mutability,read/models}.py`, `src/sldb/mcp/changes/`
