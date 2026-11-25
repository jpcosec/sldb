---
sldb:
  by: agent
  at: '2026-11-25T21:34:26Z'
  authority: generated
  via: save_document_payload
id: task-sldb-responde-que-documentos-aplican-a-un-archivo-o-a-un-simbolo-sea-porque-lo-anclan-directo-o-porq
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references:
- contracts/layers.toml
- src/sldb/api/__init__.py
- src/sldb/api/anchors/__init__.py
- src/sldb/api/anchors/resolve_pointers.py
- src/sldb/api/anchors/tag_reach.py
- src/sldb/mcp/read/tools.py
- src/sldb/mcp/registry.py
- src/sldb/models/code_anchor_doc.py
- tests/mcp/test_read_tools.py
- tests/test_where_pointers_resolve.py
- f68074750918eb74b262ff15f27f1fc9be1e2e9e
depends_on: []
pills: []
files:
- contracts/layers.toml
- src/sldb/api/__init__.py
- src/sldb/api/anchors/__init__.py
- src/sldb/api/anchors/resolve_pointers.py
- src/sldb/api/anchors/tag_reach.py
- src/sldb/mcp/read/tools.py
- src/sldb/mcp/registry.py
- src/sldb/models/code_anchor_doc.py
- tests/mcp/test_read_tools.py
- tests/test_where_pointers_resolve.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-responde-que-documentos-aplican-a-un-archivo-o-simbolo
---

# sldb responde qué documentos aplican a un archivo o a un símbolo, sea porque lo anclan directo o porque apuntan a una categoría que lo cubre

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25): el dónde de una decisión, una pill o una tarea es un puntero a un documento del store, a una categoría (un tag del árbol semántico, como layer:interface) o a un ancla de código; y quien resuelve es sldb, que es el mecanismo. Hoy sldb sabe si el código de un ancla cambió (sldb.api.anchors) y sabe bajar por el árbol de tags (sldb semantic show), pero no hay una operación que junte las dos cosas ni la pregunta inversa.

## Goal

_Describe the concrete result this task must produce._

Dos operaciones de lectura: dado un puntero, qué documentos y qué código cubre; y dado un archivo o un símbolo, qué documentos apuntan a él, directo o a través de una categoría.

## Scope

_State what is in scope and what is out of scope._

Dentro: sldb.api (anclas, árbol semántico, grafo) y la herramienta MCP que lo exponga. Fuera: definir categorías (son contenido de quien las siembra), el campo donde deskops guarda los punteros, cualquier interfaz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer docs/architecture/code-anchoring.md, anchoring.md, tags.md y selectors.md. Se compone con lo que existe (check_anchors, el árbol semántico, graph_path); no se escribe un segundo índice. La operación entra a la taxonomía de comandos (docs/architecture/one-command-taxonomy-served-by-fastmcp.md) con un solo nombre.

Aclaraciones de la revisión: Una sola operación en sldb.api y una herramienta MCP con el mismo nombre canónico (proponer anchors_resolve en docs/architecture/command-taxonomy.md si ya existe; si no, dejarlo en result-summary), con dos direcciones según el argumento: target=archivo o símbolo -> documentos que lo cubren; document=<Modelo:id> -> archivos y símbolos que cubre. Símbolo en la forma que ya usa sldb para anclas de código (docs/architecture/code-anchoring.md, p. ej. ruta::Símbolo). Cobertura = anclas directas + documentos que llegan por tag, con descendientes transitivos (todo el subárbol del DAG, más equivalencias). Salida: lista de {doc (Modelo:id), via: 'direct' | 'tag:<tag>'} (o {path, symbol, via} en la otra dirección), ordenada por doc. Un puntero a un tag inexistente no es error: va en un campo unresolved con el tag y el documento que lo nombra. tests/test_where_pointers_resolve.py se crea con un store temporal de fixtures. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_where_pointers_resolve.py

## Done When

_Name the observable condition that makes the task complete._

En un store de prueba con un documento anclado a una función, otro que apunta a un tag padre y un tercero sin relación: preguntar por el archivo de la función devuelve los dos primeros y dice por cuál vía llega cada uno; resolver el tag padre devuelve los documentos de sus tags hijos y el código al que están anclados. Un puntero a un tag que no existe se informa como tal. Nada se escribe.
