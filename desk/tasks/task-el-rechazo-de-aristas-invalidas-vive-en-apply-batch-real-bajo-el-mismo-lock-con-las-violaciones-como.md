---
sldb:
  by: agent
  at: '2026-11-26T03:56:52Z'
  authority: generated
  via: create_document
id: task-el-rechazo-de-aristas-invalidas-vive-en-apply-batch-real-bajo-el-mismo-lock-con-las-violaciones-como
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El rechazo de aristas inválidas vive en apply_batch real, bajo el mismo lock, con las violaciones como datos y no como texto

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido del desk de sldb tras leer la entrega de propose-changes (560e5a1e0; sala/2026-11-25-planificacion/sldb.md, sección propose-changes). Esa entrega no duplica la máquina de estados ni C2, pero tiene cuatro defectos: (1) el rechazo no ocurre en una escritura real por sldb.api, porque apply_batch solo calcula violaciones con dry_run=True y quien rechaza es la capa MCP (edge_rejection), así que un plugin que escribe como librería escribe la relación inválida igual; (2) la comprobación y la escritura no van bajo el mismo lock, porque MCP hace el dry_run, lo suelta y después aplica; (3) las violaciones se clasifican leyendo el texto del mensaje con expresiones regulares; (4) edge_rejection traga cualquier excepción y deja seguir la escritura. Va antes de la máquina de estados y de C2 de deskops, que cuelgan del mismo punto (la prevalidación de apply_batch y batch_edge_violations).

## Goal

_Describe the concrete result this task must produce._

Una escritura real por sldb.api.apply_batch que viola tipos, cardinalidad o condición de un RelationTypeDoc se rechaza entera antes de escribir, dentro de la misma transacción y lock que la escritura, y cada violación sale como dato estructurado.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/documents/apply_batch.py (_run), src/sldb/api/documents/batch_edges.py (batch_edge_violations) y lo que produce las violaciones de edges check, y src/sldb/mcp/write/apply.py (edge_rejection pasa a delegar). Fuera: la máquina de estados, C2 (tomar una transición) y el cambio de ids; el literal sldb://document/ se deja como está (va al inventario del cambio de ids).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) En apply_batch, la escritura real (_run) llama a batch_edge_violations dentro de la misma transacción y lock con que escribe, antes de escribir; si hay violaciones, no escribe nada y devuelve o lanza un rechazo con la lista. 2) batch_edge_violations devuelve cada violación como dato: código (types, cardinality o condition), relación, origen, destino y mensaje, tomados de la estructura que arma edges check y no de su texto; se borra la clasificación por expresiones regulares. 3) edge_rejection de MCP deja de hacer su propio dry_run y usa el rechazo de apply_batch; no traga excepciones: un error al validar es un error, no un permiso para escribir. 4) Tests: una relación inválida por cada uno de los tres códigos se rechaza llamando a sldb.api.apply_batch directo (sin MCP) y el store queda igual; una relación válida se escribe; cambiar el texto de un mensaje de edges check no cambia el código de la violación; un error dentro de la validación hace fallar la escritura. 5) Commit con prefijo feat:, sin trailer Task-Id. Correr los tests nuevos y los de apply_batch, batch_edges y mcp/write existentes; la suite completa la corre el host.

## Validation

_List the checks required before this task can close._

- pytest -q tests de apply_batch, batch_edges y mcp/write

## Done When

_Name the observable condition that makes the task complete._

sldb.api.apply_batch con una arista que viola tipos, cardinalidad o condición rechaza el lote entero sin escribir, también sin pasar por MCP; cada violación trae su código como campo; edge_rejection ya no traga excepciones; los tests nuevos pasan.
