---
sldb:
  by: agent
  at: '2026-11-15T17:45:43Z'
  authority: generated
  via: save_document_payload
id: task-migrar-a-sldb-el-generador-de-spec-de-componentes-desde-un-grafo-y-desde-el-ast-de-python-d2-b4
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-migrar-a-sldb-los-modelos-de-spec-por-tipo-de-diagrama-de-spec2viz-con-carga-y-validación-junto-a-sp
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Migrar a sldb el generador de spec de componentes desde un grafo y desde el AST de Python (D2, B4)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: lo genérico va a sldb. spec2viz tiene el módulo graph_import (grafo o snapshot a spec de componentes, función component_spec_from_graph) y el generador python_ast (spec desde el AST de Python).

## Goal

_Describe the concrete result this task must produce._

sldb produce un spec de componentes desde un grafo y desde código Python, reutilizando lo que ya tiene.

## Scope

_State what is in scope and what is out of scope._

SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE. Entra: component_spec_from_graph y sus ayudantes (migrados), component_spec_from_python sobre sldb.code.scan_tree (reutiliza el escáner, no migra el de ast), write_component_spec, el adaptador de snapshot sobre snapshot_load y el subcomando "sldb notations from-graph". Criterio de cobertura: sldb la cubre si tiene una función con la misma entrada y la misma salida observable en los tests portados; entonces se reutiliza, si no se migra. "No duplicar el escaneo AST" significa que ninguna función nueva recorre código Python por su cuenta fuera de sldb.code. Sale: compiladores, renderers, la CLI de spec2viz y cualquier cambio en spec2viz; el modelo de componente lo entrega D3 y esta tarea no lo redefine. Orden: depende de D3 (modelos de spec) y no empieza antes. spec2viz NO se retira y conserva su código; el gate IR13 es la tarea IR13 del desk de IR, que decide el retiro; aquí solo se nombra. Paridad: los tests de spec2viz de la pieza se portan con el mínimo cambio. Cubre B4 del brief.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Comparación previa (hecha al preparar la tarea; repetir y registrar en el informe de cierre, función por función). Origen en spec2viz (repo hermano, existen): módulo spec2viz.graph_import (364 líneas) y spec2viz.generators.python_ast (116 líneas, la usa la CLI de spec2viz para from-graph y python-ast). Criterio reutilizar o migrar: si sldb ya tiene una función con la misma entrada y la misma salida observable en los tests portados, se reutiliza; si no, se migra el código de spec2viz.
2. Reutilizar de sldb: (a) lectura de un snapshot node-link: sldb.api.graph.snapshot_load / sldb.store.graph.graph_io.load_graph (src/sldb/api/graph/snapshot.py) cubre load_node_link: los nodos con id y tipo y las aristas con relation_type salen del GraphSnapshot, así que load_node_link se sustituye por un adaptador de pocas líneas sobre snapshot_load y no se migra. (b) load_store_index: spec2viz ya llama a sldb.api.load_edge_index, así que en sldb se llama directo (src/sldb/api/edges/edge_reading.py) sin loader propio. (c) load_node_link_graph con atributos de nodo (_node_attrs: schema.ast y schema.semantics del grafo de fuente de Python): se reutiliza snapshot_load SOLO si el test portado test_python_source_graph_labels_kinds_and_scope pasa leyendo esos atributos del KnowledgeNode; si el snapshot no los conserva, se migra _node_attrs (y load_node_link_graph) leyendo el JSON crudo. Anotar cuál ocurrió. (d) evaluate_projection_view y save_projection_view (src/sldb/api/notations/projection_view.py y projection_save.py) dan nodos y aristas de una ViewDoc, no filtran por tipo de nodo, modelo ni relación ni producen un spec: se pueden usar como fuente alternativa de (nodes, edges) pero NO sustituyen a component_spec_from_graph.
3. Migrar (no existe en sldb): node_kind, document_ref, sanitize_id, _unique_ids, _label_and_kind, _describe, las constantes (DEFAULT_NODE_TYPES, DEFAULT_EXCLUDED_RELATIONS, CONTAINS_RELATION, _RESERVED_IDS, SLDB_SCHEME, _AST_KINDS) y component_spec_from_graph con la misma firma y el mismo comportamiento. Destino: un módulo nuevo bajo src/sldb/api/notations/ (nombre sugerido component_spec_graph) y otro para la parte Python; cada uno bajo el límite de líneas del repo.
4. Generador desde Python: NO se migra el escáner ast de spec2viz (_scan_module, _module_matches, generate_python_ast_spec). La función nueva component_spec_from_python(src_dir, project_id, title, root_package) usa sldb.code.scan_tree (src/sldb/code/scan.py) y se queda con los hechos de módulo y de clase y con sus relaciones: nodo kind module por módulo, kind class por clase de primer nivel, relación defines de módulo a clase, relación imports por cada import resuelto, y nodos external para los destinos no declarados, igual que spec2viz. write_spec se migra tal cual (yaml.dump con sort_keys=False y allow_unicode=True) como write_component_spec. Eso es "no duplicar el escaneo AST de sldb.code": ninguna función nueva recorre árboles con el módulo ast ni con tree-sitter fuera de sldb.code. Entrada: "árbol de Python" = un directorio con .py (la misma entrada que el generador de AST); "snapshot" = el JSON node-link; "grafo" = el edge index de un store. Son tres entradas, dos funciones.
5. tree-sitter es el extra opcional [code]: si no está, component_spec_from_python devuelve el aviso (formato de findings de sldb: level, code, subject, what, fix) con level alert, code component-spec/code-extra-missing, subject la ruta del árbol, what "no hay tree-sitter" y fix "pip install 'structuredLanguageDB[code]'", y no escribe nada. Otros avisos con el mismo formato: component-spec/syntax-error (archivo no analizable, se omite como hace spec2viz) y component-spec/dangling-edge (arista con extremo fuera de alcance, descartada).
6. API pública: exportar desde sldb.api.notations component_spec_from_graph, component_spec_from_python y write_component_spec. Devuelven el dict de spec de componentes que valida como ComponentDiagram, el modelo de la tarea de modelos de spec (D3, de la que depende esta tarea; no empieza antes de que D3 esté integrada). CLI: subcomando "sldb notations from-graph" con --snapshot RUTA | --store RUTA | --python DIR (exactamente uno), --node-type, --model, --relation, --exclude-relation, --drop-isolated, --module-prefix, --id, --title y --output (stdout si falta), portando lo que hace hoy "spec2viz from-graph" y "python-ast".
7. Tests a portar con el mínimo cambio: los 21 de spec2viz test_graph_import (los de función se importan de sldb.api.notations; test_load_store_index_uses_public_sldb_api se adapta a la llamada directa; los 5 test_cli_from_graph_* y test_cli_from_graph_module_prefix se reescriben contra "sldb notations from-graph"). spec2viz NO tiene tests del generador python_ast: se agrega un test nuevo de sldb que genera el spec sobre un árbol pequeño con component_spec_from_python y lo compara con la salida de generate_python_ast_spec de spec2viz (mismos módulos, clases y relaciones defines) y valida con ComponentDiagram; las diferencias (p. ej. imports simples que ast ignoraba) se registran en el informe.
8. Informe de comparación en el cierre: tabla con cada función de graph_import y python_ast, su equivalente en sldb (o "migrada") y el motivo. spec2viz no se toca: conserva su código; el retiro lo decide la tarea IR13 del desk de IR (gate IR13); aquí solo se nombra.

## Validation

_List the checks required before this task can close._

- Tests de origen en spec2viz: test_graph_import (21 tests: de función, de carga y de la CLI from-graph). El generador python_ast no tiene archivo de tests en spec2viz.
- Destino previsto: un archivo de tests del generador de spec de componentes desde grafo, junto a los de proyección de vistas de sldb, uno para el generador desde Python (con el test nuevo de comparación con spec2viz, que se salta si falta el extra [code]) y uno del subcomando from-graph.
- Cada spec generado valida con ComponentDiagram (modelo de D3).
- Informe de comparación (función por función: reutilizada o migrada y por qué) escrito en el cierre.
- TMPDIR=/dev/shm pytest -q de cada archivo tocado, uno a la vez; antes de entregar, todos los tests/*.py de a uno.
- tools/check.sh
- sldb stores build --check
- deskops graph missing sin faltantes nuevos.

## Done When

_Name the observable condition that makes the task complete._

1. component_spec_from_graph, component_spec_from_python y write_component_spec exportados desde sldb.api.notations, y "sldb notations from-graph" genera el spec desde snapshot, store o árbol de Python.
2. Los 21 tests portados de test_graph_import pasan y el test nuevo del generador desde Python coincide con spec2viz en módulos, clases y relaciones defines; todo spec generado valida con ComponentDiagram.
3. Ninguna función nueva escanea código Python fuera de sldb.code (se comprueba con grep de "import ast" y "tree_sitter" en los módulos nuevos).
4. Informe de comparación escrito en el cierre, con la decisión sobre _node_attrs y load_node_link_graph (reutilizado de snapshot_load o migrado).
5. Los avisos salen con el formato de findings de sldb (level, code, subject, what, fix).
6. spec2viz sin cambios (retiro = gate IR13, tarea IR13 del desk de IR); la tarea D3 integrada antes de empezar.
7. Suite de a un archivo, tools/check.sh y sldb stores build --check en verde; deskops graph missing sin faltantes nuevos.
