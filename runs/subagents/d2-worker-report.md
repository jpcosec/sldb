# Informe del worker D2

Tarea: migrar a sldb el generador de spec de componentes desde un grafo y desde el AST de Python (D2, B4).
Commit de código: `c3316caa` en main, sin push. Este informe va en un commit aparte.
spec2viz no se tocó (`git status` limpio). Su retiro lo decide el gate IR13, la tarea IR13 del desk de IR.

## Comparación función por función

Origen: `spec2viz/spec2viz/graph_import.py` y `spec2viz/spec2viz/generators/python_ast.py`.
Destino: `src/sldb/api/notations/component_spec_*.py`.

### graph_import

| spec2viz | sldb | Decisión y motivo |
|---|---|---|
| `GraphNodes`, `GraphEdges`, `GraphAttrs`, `_AST_KINDS`, `SLDB_SCHEME`, `DEFAULT_NODE_TYPES`, `DEFAULT_EXCLUDED_RELATIONS`, `CONTAINS_RELATION`, `_RESERVED_IDS` | `component_spec_constants.py` | Migradas tal cual. sldb no las tenía. |
| `_normalize_type`, `node_kind`, `_id_tail`, `document_ref`, `sanitize_id`, `_label_and_kind` | `component_spec_ids.py` | Migradas tal cual. sldb no tiene nada equivalente. |
| `_unique_ids` | `component_spec_ids.py` (`_unique_ids` + `_free_id`) | Migrada. El bucle del sufijo pasa a `_free_id` por la regla de 10 líneas, con la misma salida. |
| `_node_identity`, `_node_attrs` | `component_spec_loaders.py` (`_node_attrs` + `_label_and_fallback`) | Migradas. Ver la decisión de abajo. La rama de label/kind se separó por la regla de 10 líneas. |
| `load_node_link_graph` | `component_spec_loaders.py` (+ `_read_node`, `_links`) | Migrada, leyendo el JSON crudo. Ver la decisión de abajo. |
| `load_node_link` | `component_spec_loaders.py` | Migrada como envoltorio de `load_node_link_graph`, igual que en spec2viz. No es un adaptador de `snapshot_load` (ver abajo). |
| `load_store_index` | sin loader propio: `sldb.api.load_edge_index` + `index_graph` | Reutilizada. La CLI llama a `load_edge_index(store)` directo. `index_graph(index)` solo convierte el índice a `(nodes, edges)`, son las dos líneas de la función original sin la carga. |
| `_describe` | `component_spec_describe.py` | Migrada. Las dos ramas relations/exclude_relations quedan en un condicional de una línea, con el mismo texto. |
| `component_spec_from_graph` | `component_spec_graph.py` (+ `_live_edges`, `_connected`, `_spec_data`, `_spec_node`; `_keeps` e `_in_scope` en `component_spec_filters.py`; `_spec` en `component_spec_describe.py`) | Migrada con la misma firma y el mismo comportamiento. Los cinco pasos numerados se separaron en ayudantes por las reglas de tamaño. Los 13 tests de compilación pasan sin cambios. |
| `evaluate_projection_view` / `save_projection_view` (sldb) | — | No sustituyen a `component_spec_from_graph`: no filtran por tipo, modelo ni relación y no producen un spec. No se usaron. |

### python_ast

| spec2viz | sldb | Decisión y motivo |
|---|---|---|
| `_scan_module`, `generate_python_ast_spec`, `_module_matches` | `component_spec_from_python` + `_modules`, `_wanted`, `_module_elements`, `_class_elements`, `_imports`, `_resolve` (`component_spec_python.py`) | No se migran, como manda el TaskDoc. Los hechos salen de `sldb.code.scan_tree`: el hecho `module`, los hechos `class` de primer nivel (`qualified_name` sin punto) y `attrs.imports`. El filtro por paquete repite la regla de `_module_matches` sobre `fact["path"]`. |
| `_sanitize_id` (el de python_ast: `.` y `-` a `_`) | `component_spec_python_build.py` | Migrada tal cual. Mantiene los ids `module_*` y `class_*` de spec2viz para la paridad. |
| `_build_spec`, `_register_missing_nodes` | `component_spec_python_build.py` | Migradas tal cual. El nodo `external` toma la etiqueta `target.split("_")[-1]`, igual que spec2viz. |
| `write_spec` | `write_component_spec` (`component_spec_python_build.py`) | Migrada: `yaml.dump` con `sort_keys=False` y `allow_unicode=True`. Además acepta `str` como ruta. |

## Decisión sobre `_node_attrs` y `load_node_link_graph`: migradas

Se probó `snapshot_load` (`sldb.store.graph.graph_io.load_graph`) con los fixtures de los tests portados:

- Atributos: se conservan. `KnowledgeNode.ast` y `KnowledgeNode.semantics` traen `module`, `name`, `node_kind` y `kind` intactos.
- Aristas: se pierden. `_snapshot_from_node_link` arma cada nodo desde `schema` y no lee `links`. En el fixture de `test_load_node_link_reads_id_from_top_level_or_schema_identity` y en `PY_GRAPH` de `test_python_source_graph_labels_kinds_and_scope`, las aristas solo están en `links`, así que `snapshot_load` devuelve todos los nodos con `edges=[]`.

Los archivos que escribe el propio sldb con `save_graph` sí funcionarían, porque duplican las aristas en `schema.edges`. Pero con la regla de cobertura (misma salida observable en los tests portados), `snapshot_load` no cubre el caso: los dos tests fallarían por las aristas. Por eso `_node_identity`, `_node_attrs`, `load_node_link_graph` y `load_node_link` se migran leyendo el JSON crudo, como en spec2viz.

El punto 2(a) del TaskDoc, que daba `load_node_link` como cubierto por `snapshot_load`, partía de que "las aristas salen del GraphSnapshot". Eso no se cumple para un node-link con `links` y sin `schema.edges`.

## Archivos

Nuevos:
- `src/sldb/api/notations/component_spec_constants.py`
- `src/sldb/api/notations/component_spec_ids.py`
- `src/sldb/api/notations/component_spec_loaders.py`
- `src/sldb/api/notations/component_spec_filters.py`
- `src/sldb/api/notations/component_spec_describe.py`
- `src/sldb/api/notations/component_spec_graph.py`
- `src/sldb/api/notations/component_spec_findings.py`
- `src/sldb/api/notations/component_spec_python.py`
- `src/sldb/api/notations/component_spec_python_build.py`
- `src/sldb/cli/commands/notations_from_graph.py`
- `tests/notations/test_component_spec_graph.py`: 16 tests portados (de función y de carga).
- `tests/notations/test_notations_from_graph_cli.py`: los 5 tests de CLI portados + 1 nuevo, el de `dangling-edge` por stderr.
- `tests/notations/test_component_spec_python.py`: 4 tests nuevos, entre ellos la comparación con spec2viz.

Modificados:
- `src/sldb/api/notations/__init__.py`: exporta `component_spec_from_graph`, `component_spec_from_python` y `write_component_spec`. También exporta `load_node_link`, `load_node_link_graph`, `index_graph`, `node_kind`, `document_ref`, `sanitize_id` y las tres constantes públicas, porque los tests portados las importan de `sldb.api.notations`.
- `src/sldb/cli/parsers/notations.py` y `src/sldb/cli/commands/notations.py`: subcomando `sldb notations from-graph` con `--snapshot | --store | --python` (exactamente uno; argparse sale con 2), `--node-type`, `--model`, `--relation`, `--exclude-relation`, `--drop-isolated`, `--module-prefix`, `--id`, `--title` y `--output`. Sin `--output`, el YAML va a stdout.
- `contracts/layers.toml`: la puerta `ejes` falló por acoplamiento nuevo medido. La unidad `nucleo` pasa de `needed_by` 54 a 56 y `notacion` de `needs` 4 a 6, porque el eje `vistas` ahora usa `codigo` (`sldb.code.scan_tree`) y `errores` (`sldb.core.finding`). Se actualizaron las cuentas, con su comentario "medido 2026-11-15 (D2)". En HEAD, antes del cambio, la puerta pasaba.

## Avisos (formato Finding de sldb: level, code, subject, what, fix)

- `component-spec/code-extra-missing`: level alert. El subject es la ruta del árbol, what "no hay tree-sitter" y fix `pip install 'structuredLanguageDB[code]'`. `component_spec_from_python` devuelve `(None, [aviso])` y no escribe nada. La CLI sale con 1.
- `component-spec/syntax-error`: alert por archivo con `has_error`. Queda el nodo módulo, sin clases ni imports, como spec2viz cuando `ast.parse` falla.
- `component-spec/dangling-edge`: alert por arista con un extremo que no es nodo del grafo; `component_spec_from_graph` la descarta. Lo emite la CLI con `dangling_edges(nodes, edges)`, porque `component_spec_from_graph` conserva su firma y devuelve solo el dict. Interpretación: "fuera de alcance" quiere decir fuera del grafo. Las aristas que caen por los filtros que pide el usuario (tipo, modelo, `--module-prefix`) no avisan.
- La CLI manda los avisos a stderr con `Finding.line()` y el fix, para que stdout quede en YAML. También pasan por `alert_sink.report(text=False)` y así llegan al envelope.

API: `component_spec_from_python(src_dir, project_id="project", title="Python AST Architecture", root_package=None)` devuelve `(spec | None, findings)`. `component_spec_from_graph` devuelve el dict, como en spec2viz.

## Tests

Todos de a un archivo, con `flock /dev/shm/sldb1-tests.lock python -m pytest -q -p no:cacheprovider <archivo>` y `TMPDIR=/dev/shm PYTHONPATH=src`:

| Archivo | rc | Resultado |
|---|---|---|
| tests/notations/test_component_spec_graph.py | 0 | 16 passed |
| tests/notations/test_notations_from_graph_cli.py | 0 | 6 passed |
| tests/notations/test_component_spec_python.py (venv, sin `[code]`) | 0 | 1 passed, 3 skipped |
| tests/notations/test_component_spec_python.py (con tree-sitter, `PYTHONPATH=src:/dev/shm/d2-ts`) | 0 | 4 passed |
| tests/test_clean_code_rules.py | 0 | 1113 passed |
| tests/notations/test_notation_view_and_routes.py | 0 | 9 passed |
| tests/test_cli_every_command_has_a_handler.py | 0 | 1 passed |
| tests/test_address_surface.py | 0 | 8 passed |
| tests/test_standalone.py | 0 | 29 passed |

`bash tools/check.sh --fast`: PASS en núcleo aislado, capas (0 violaciones), identidad, ejes (después de actualizar las cuentas) y superficie. Se omiten afirmaciones, pruebas y selfdoc por `--fast`.

`deskops graph missing`: rc 0 y 6 faltantes, todos ajenos a D2 (task-diseño-jerarquía... y task-reglas-rule-graph...). Ninguno es nuevo.

El venv no tiene tree-sitter. Para correr la comparación, tree-sitter 0.26.1 y tree-sitter-python 0.25.0 se instalaron aparte en `/dev/shm/d2-ts` (`uv pip install --target`), sin tocar el venv compartido ni `uv.lock`. Los 21 tests portados son 16 + 5. El test de comparación (`test_matches_spec2viz_on_modules_classes_and_defines`) coincide con `generate_python_ast_spec` en módulos, clases y relaciones `defines`. Cada spec generado valida con `ComponentDiagram.model_validate` + `validate_spec`.

## Grep de escaneo propio

```
$ grep -nE "import ast|tree_sitter" src/sldb/api/notations/component_spec_*.py src/sldb/cli/commands/notations_from_graph.py
(sin resultados, rc=1)
```

## Diferencias con spec2viz

1. Imports del generador Python. spec2viz solo ve `ImportFrom` con `module` y recorre todo el árbol, incluidos los imports dentro de funciones. sldb usa `scan_tree`, que da los imports de primer nivel:
   - entran los `import x` simples; `import a, b` da dos destinos;
   - los relativos se resuelven contra el paquete del módulo: `from .sub.b import X` en `pkg.a` da `module_pkg_sub_b`, donde spec2viz daba `module_sub_b`, y `from . import c` da `module_pkg`, que spec2viz omitía;
   - los imports anidados en funciones o en `if` no entran;
   - sin duplicados, en orden alfabético.
2. Las clases de primer nivel salen en orden de fuente y los módulos en orden de ruta, igual que spec2viz. `scan_tree` ignora `__pycache__`.
3. `--python` en la CLI: `--module-prefix` hace de `root_package` (uno solo). `--node-type`, `--model`, `--relation`, `--exclude-relation` y `--drop-isolated` no aplican: dan error en vez de ignorarse en silencio. Por defecto, id = nombre del padre del directorio y título `<id> AST Architecture`, como `spec2viz diagram generate`.
4. Los tests de CLI usan `--snapshot` en vez del argumento posicional `GRAPH_JSON` y `--output` en vez de `--out`. Los pasos `diagram render --renderer mermaid` y `diagram lint` de `test_cli_from_graph_writes_valid_spec` no se portaron, porque los renderers están fuera de alcance. En su lugar se comprueba sobre el spec el anidamiento que mostraba el mermaid (atom-x contiene atom-y, con sus etiquetas), y `diagram validate` pasa a ser `load_spec` + `validate_spec`.
5. `test_load_store_index_uses_public_sldb_api` se adaptó a la llamada directa: `index_graph(sldb.api.load_edge_index(...))`. `test_cli_from_graph_store_goes_through_loader` parchea `load_edge_index` en el módulo del comando.
6. `--store` lee el edge index con `sldb.api.load_edge_index`. Ya no hace falta el import perezoso ni el error "needs the sldb package".

## Pendientes (del coordinador)

- No se corrió la suite completa de a un archivo, ni `sldb stores build --check`, ni `tools/check.sh` completo, ni selfdoc sync/python-sync, como pidió el encargo. Es probable que los módulos y el subcomando nuevos pidan regenerar selfdoc o la referencia de la CLI.
- El test de comparación con spec2viz se salta en el venv porque falta el extra `[code]`. Hay que decidir si el venv/CI lo instala para que corra siempre.
- Hay que confirmar el criterio de `dangling-edge` (solo extremos fuera del grafo) y la salida con rc 1 cuando falta el extra.
- Hay que confirmar la actualización de las cuentas de unidad en `contracts/layers.toml`.
- Sin push ni closeout. `uv.lock` no se tocó.
