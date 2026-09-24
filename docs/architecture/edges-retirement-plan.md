# Plan de retiro de la capa `runtime/edges/`

Inventario y plan, sin refactor. Decisión del mantenedor (documentada, no discutida): la capa
derivada `runtime/edges/` (un YAML por documento) se retira; se queda la capa de grafo
`src/sldb/store/graph/` (networkx + node-link JSON portable) con KGDB integrado.

Base del inventario: commit `bb1efbb`, rama `chore/edges-retirement-inventory`.
Línea base de tests: `PYTHONPATH=src python -m pytest -q` → **1015 passed** (2026-09-24).

Evidencia citada por el mantenedor: KB real de 1027 documentos markdown (~1MB de texto) →
`runtime/edges/` pesa 16MB; `runtime/graphs/*.nx.json` + `*.kg.json` pesan 350KB para el mismo
grafo. Un documento de 1.3KB genera un edges YAML de 405 líneas (el bloque `semantics` completo
se repite en el nodo del documento, en cada nodo de sección y en `about`).

---

## 0. Hallazgo estructural (lee esto primero)

**La "capa nueva" es hoy lectora de la capa vieja.** Todo `src/sldb/store/graph/` y
`src/sldb/api/graph/` entra al grafo por un solo punto: `load_edge_index` →
`compose_edge_index` → shards de `runtime/edges/`:

- `src/sldb/api/graph/analyze.py:12`, `execute.py:7`, `neighborhood.py:7`, `snapshot.py:7`,
  `traverse.py:12` importan `load_edge_index`.
- `src/sldb/api/edges/edge_reading.py:16-21` → `compose_edge_index` →
  `shard_reading.read_store_contributions` → `load_edges_shard` de `runtime/edges/`.
- `src/sldb/store/graph/convert.py:9-11` (snapshot↔index) y `analysis/*` operan sobre ese
  `EdgeIndex` compuesto de shards; `store/graph/__init__` lo dice: "all on top of the edge index".

Dos consecuencias para el plan:

1. Retirar `runtime/edges/` NO es borrar los 10 archivos de la lista: es re-puntar la fuente de
   verdad de toda la capa graph hacia el grafo portable (snapshot node-link), que hoy solo se
   produce **desde** los shards (`api/graph/snapshot.py:snapshot_save`).
2. La ruta alternativa ya existe y es la base del porte: `stores semantic-export`
   (`store/export.py`) produce el payload `sldb_kgdb_semantic_export` desde los índices fuente
   (store/models/docs/sections/DAG, **sin tocar edges**), y `store/graph/ingest_sldb.py` +
   `ingest_sldb_nodes.py` lo convierten en `GraphSnapshot` (`graph ingest-sldb`). Esa ruta
   cubre hoy un subconjunto del vocabulario viejo: ver GAPS en §2.

---

## 1. Inventario de consumidores

Clasificación: **(A)** se borra con la capa · **(B)** se reescribe contra el grafo
networkx/KGDB · **(C)** no dependía de verdad.

| Consumidor | Qué lee/escribe de la capa edges | Pasa si desaparece | Clase |
|---|---|---|---|
| `api/documents/payload_save_steps.py` | `rebuild_edges_indexes(sp, root, ...)` dentro de `save_document_indexes`, bajo el store lock — `payload_save_steps.py:21` y `:84` | El write deja de regenerar el índice; el grafo queda stale salvo que el mismo punto regenerue el snapshot. Se reescribe: la llamada al rebuild se sustituye por la regeneración del snapshot de grafo (mismo lock, mismo sitio). | B |
| `api/documents/untrack_document.py` | Ídem: `rebuild_edges_indexes` en `forget_document` — `untrack_document.py:21` y `:65` | Igual que el anterior; un untrack también debe refrescar el snapshot de grafo. | B |
| `api/edges/rebuild_edges.py` | Es la capa misma: `rebuild_edges` (semantic→sections→edges) — `rebuild_edges.py:36-38` | Se borra entero con la capa. Nadie fuera de `cli/commands/edges.py:8` e `init_relations.py` lo llama (ver §1 anexo). | A |
| `api/__init__.py` | Exporta ~20 símbolos de la capa: `check_edges`, `edges_from/to`, `edge_node`, `edge_nodes_of_type`, `load_edge_index`, `init_relations`, `rebuild_edges`, serializers, `EdgeIndex`, `EdgeCheckReport`, `EdgeNodeRecord`, `EdgeRecord`, `EdgeRebuildReport`, `RelationsInitReport` y los helpers de node ids (`doc_node_id`, `tag_node_id`, `kind`, `bare`, ...) — `api/__init__.py:22-28` y `:62-65` + `__all__`. Este módulo es el contrato público de librería ("Consumers (pron, kgdb, deskops...) call these instead of instantiating sldb.cli", `api/__init__.py:3-7`) | Cada símbolo de edges que muere rompe a cualquier consumidor externo que lo use. Se limpia el surface: lo que muere con los shards (lecturas, init, rebuild, reportes) sale del `__all__`; `EdgeNodeRecord`/`EdgeRecord` sobreviven (los usa `store/graph/convert.py:10-11`); los helpers `node_ids` se re-exportan desde `store/graph`. | A (surface muere; piezas vivas se mueven a `store/graph`) |
| `api/semantic/dag_writes.py` | `refresh_store_edges(sp)` tras cada write al DAG — `dag_writes.py:16` y `:58` | El cambio de DAG no se refleja en el grafo. Equivalente nuevo: regenerar/actualizar el snapshot (nodo store, `semantic_parent`/`semantic_equivalent`), que es justo lo que `ingest_sldb_nodes._semantic_tag_node` ya produce. | B |
| `api/stores/index_commit.py` | `rebuild_edges_indexes` en `_rebuild_indexes` (semantic+sections+edges+cascade) — `index_commit.py:13` y `:51` | `commit_index_updates` (usado por `update_store_indexes`) deja el grafo stale. Se reescribe contra snapshot. | B |
| `cli/selfdoc_write.py` | `rebuild_edges_indexes` tras escribir docs autogenerados — `selfdoc_write.py:13` y `:25` | El selfdoc no refresca el grafo. Se reescribe (además, el selfdoc python ya escribe su `.kg.json` vía `kgdb_sync`, `kgdb_sync.py:14-24`). | B |
| `store/derived_rebuild.py` | `rebuild_edges_indexes` como tercer paso de `rebuild_derived_indexes` — `derived_rebuild.py:8` y `:23` | Centro de los writes por modelo (reindex/promote). Se reescribe: la regeneración del snapshot pasa a ser el paso 3. | B |
| `store/export.py` | `rebuild_edges_indexes` en `SemanticExporter._rebuild` — `export.py:13` y `:37` | Solo afecta a `--rebuild` del export; el payload del export no incluye edges. Irónico: el export **es** la fuente nueva. Se quita la llamada. | B |
| `store/ops.py` | `rebuild_edges_indexes` en `_do_track` — `ops.py:14` y `:45` | `track_document` deja el grafo stale. Se reescribe contra snapshot. | B |
| `store/models/__init__.py` | Importa `EdgeContribution` (`:17`) y `DocEdges` (`:18`) — los dos en la lista de retiro — y `ModelEdges` (`:19`, no listado) | `DocEdges` desaparece con el shard por-documento. `EdgeContribution`/`ModelEdges` quedan vivos mientras vivan `compose`/`shard_reading`/`store_contribution`/`model_contribution` (ver anexo): se edita el `__init__` en el PR que retira esos lectores, no antes. | B |
| `cli/commands/ast.py` | Nada: `"edges"` en `:21` es un literal del `SCHEMA` (nombres de aristas del AST). `ast_for_target` construye desde runtime docs (`cli/graph_ops/build_ast.py`), no lee shards | Nada. | C |
| `cli/commands/doc.py` | Indirecto: `rebuild_derived_indexes` en `_save_updated` — `doc.py:19` y `:71` | El efecto es el de `derived_rebuild` (B); doc.py en sí no importa nada de la capa edges. | B (via `derived_rebuild`) |
| `cli/dispatcher.py` | `_load_edges()` importa `EdgesCLI` y registra el handler `edges` — `dispatcher.py:48-50` (llamado en `:12`) | Se borra el registro; el método `_load_edges` también llamaba `_load_graph` (`:51`), que se conserva (se fusiona en `_load_3`). | A |
| `cli/graph_ops/build_ir.py` | Nada: `GraphEdge`/`graph.edges` (`:82-88`) son el edge del IR **por documento**, construido del markdown (`sldb.core.ir`), no de la capa edges | Nada. | C |
| `cli/parsers/public.py` | `add_edges_group` registra el grupo `edges` — `public.py:9` y `:21` | Se quita la llamada; queda `add_graph_group` (`:22`). El parser `cli/parsers/edges.py` (retirado) queda sin referencias. | A |
| `cli/parsers/graph_analysis.py` | Nada de la capa edges: sus únicos imports son argparse y `sldb.store.graph.analysis.KINDS` (`:7`); `--directed`/`--isolated` son flags de análisis | Nada. Su handler (`cli/commands/graph_analysis.py`) sí lee `load_edge_index` vía `api.graph` — dependencia indirecta cubierta en §2 (G3/G5). | C |
| `cli/serve/routes.py` | `dispatch_edge` y la rama `/edges*` — `routes.py:10` y `:64-65` | Las rutas `/edges`, `/edges/node`, `/edges/nodes` (de `edges_routes.py`, retirado) dejan de existir. La alternativa `/graph/*` ya vive en `graph_routes.py`. Se borra la rama y el import. | A |
| `cli/serve/lint_routes.py` | `check_edges(store_path, include_linked=False)` para la sección `edge` del `/lint` — `lint_routes.py:16` y `:61-64` | `/lint` pierde los problemas de edges (errores + "Shard de aristas desactualizado"). Se reescribe contra la validación del grafo nuevo, o se retira esa sección (el concepto "shard stale" muere con la capa). **Está fuera de la lista de retiro y se queda huérfano: hay que tocarlo sí o sí.** | B |

### Anexo — dependencias adyacentes no listadas (lectores de `runtime/edges/`)

El retiro listado cubre el **camino de escritura** (edge_sync, edge_rebuild, doc_contribution,
doc_edges/edge_contribution, rebuild_edges API, CLI y rutas HTTP). El **camino de lectura** no
está en la lista pero muere con los shards si no se re-punta:

- `api/edges/edge_reading.py` (`load_edge_index/edges_from/edges_to/edge_node/edge_nodes_of_type`)
- `api/edges/check_edges.py`, `edge_check_report.py`, `edge_serialization.py`, `init_relations.py`,
  `relations_init_report.py`, `builtin_relation_writes.py`, `relation_models.py`
- `store/edge_index/` completo: `compose.py`, `shard_reading.py`, `resolve.py`, `validation.py`,
  `federation.py`, `acyclic.py`, `records.py`, `node_ids.py`, `doc_kinds.py`, `doc_structure.py`,
  `model_contribution.py`, `store_contribution.py`, `anchor_targets.py`, `form_targets.py`,
  `ref_form.py`, `ref_symbol.py`, `cache_keys.py`, `shard_signature.py`
- `store/io/shards.py` (`load_edges_shard`/`save_edges_shard`), `store/io/shard_compose.py`
  (`compose_edges_documents`), `store/layout.py` (`edges_*` paths)
- `api/graph/*` (analyze/execute/neighborhood/snapshot/traverse) y `store/graph/convert.py`,
  `node_view.py`, `traversal.py`, `executor.py`, `facet_match.py`: consumen `load_edge_index`.

**`init_relations` (`api/edges/init_relations.py`) llama `rebuild_edges`** (`init_relations.py`):
la parte de registrar RelationTypeDoc/RelationDoc/builtin-relations/predicados sobrevive (son
operaciones de docs), su efecto en el índice depende del GAP G2.

---

## 2. Mapa de equivalencia

Capacidad que hoy da `runtime/edges/` → equivalente **exacto** en la capa networkx/KGDB.
`GAP` = sin equivalente hoy (bloquea el retiro).

| # | Capacidad vieja (símbolo) | Equivalente nuevo (símbolo concreto) | Estado |
|---|---|---|---|
| 1 | Leer el grafo tipado de un store: `load_edge_index` → `EdgeIndex` (`edge_reading.py:16-21`, `compose.py:38`) | `load_graph(path)` (`graph_io.py:16`) → `index_from_snapshot` (`store/graph/convert.py:17-20`) devuelve un `EdgeIndex` idéntico en forma. `graph_get`/`graph_list`/`execute_query` (`api/graph/execute.py`) y `collect_neighborhood` (`neighborhood.py`) ya operan sobre `EdgeIndex` | **Parcial**: la forma es la misma, pero el snapshot hoy se genera **desde** los shards (`api/graph/snapshot.py:17`). El paso "snapshot desde índices fuente sin shards" es el porte (§3). |
| 2 | Nodos store/model/document/section/semantic_tag (`doc_structure.py:22-41`, `model_contribution.py`, `store_contribution.py`) | `_store_node`/`_model_node`/`_document_node`/`_section_node`/`_semantic_tag_node` (`ingest_sldb_nodes.py:10-70`), vía `sldb_semantic_export_to_snapshot` (`ingest_sldb.py:19`). Mismos ids `sldb://<kind>/...` y misma `semantics` (export_id, path, hash_c/hash_d, tags) | ✔ equivalente exacto para estos 5 tipos |
| 3 | Edges estructurales + DAG: `has_model`, `has_document`, `has_section`, `tagged_as`, `semantic_parent`, `semantic_equivalent` (`doc_structure.py:44-52`, `store_contribution.py:16-28`) | Los mismos nombres y targets en `ingest_sldb_nodes.py` (`_store_node:11`, `_model_node:30-34`, `_document_node:42-46`, `_section_node:53`, `_semantic_tag_node:17-21`) | ✔ equivalente exacto |
| 4 | Nodos **field** + edges `has_field` y `extends` (`model_contribution.py:24-28`; campos de `model_type.model_fields` con `describe_field`) | Ninguno. El semantic export no lleva campos (`export.py:_proc_entry` deja fuera `model_fields`) y `ingest_sldb_nodes` no genera `sldb://field/...` | **GAP G1** — requiere importar el modelo ("como `edge_rebuild._model_type`", `edge_rebuild.py:48-59`) o extender el export |
| 5 | Nodos relation_type/anchor y edges authoreados `relation_doc`, `applies_to_source/target`, alias de anchor (`doc_kinds.py:36-58`, `anchor_targets.py`) | Ninguno: `ingest_sldb_nodes` no produce `sldb://relation_type/`, `sldb://anchor/` ni edges de RelationDoc | **GAP G2** |
| 6 | Reglas cross-document al componer: authored edge hereda `condition`/`axis` de su tipo, `direction=undirected` → reverse, authored apuntando a nada → `problems` y se descarta, schema/alias colgantes → descartados (`resolve.py:26-44`) | Ninguno: `index_from_snapshot` copia edges crudos (`convert.py:24-25`); el snapshot es el grafo "ya resuelto". | **GAP G3** — o se resuelve al generar el snapshot (el generador aplica las reglas, y el snapshot queda final) |
| 7 | Validación de edges contra relation types: tipo desconocido, endpoints inexistentes, clases de endpoints (`source_types`/`target_types` con herencia por `base_models`), cardinalidad (`validation.py:20-40`); ciclos en `semantic_parent`/`extends` (`acyclic.py:14-16`) | Ciclos: `graph.analysis.cycles` existe y `acyclic.cycle_errors` ya lo reusa (`acyclic.py:12`) — pero corre sobre un `EdgeIndex`. La validación por-edge y la cardinalidad no tienen home en la capa nueva | **GAP G4** |
| 8 | Rebuild incremental en la hash chain: `rebuild_edges_indexes`, cache keys (`cache_keys.py`), dirty sets, `EdgeRebuildReport` | No hay equivalente, deliberadamente: el costo (16MB vs 350KB) es la razón del retiro. El "rebuild" nuevo = regenerar el snapshot completo (barato) | ✔ retiro intencional, no gap |
| 9 | Staleness por-shard (`EdgeIndex.stale` → lint "Shard de aristas desactualizado", `lint_routes.py:64`; `edge_reading.py:17`) | Desaparece el concepto: no hay cache derivada por documento a la que detectar stale | ✔ retiro intencional (el lint se reescribe, §1) |
| 10 | Federación: `federated_stores`/`qualify_id` (`federation.py:8-24`), `include_linked` en toda lectura | Ninguno sobre snapshots: hoy la federación lee los shards de cada store linkeado (`compose.py:46-53`). Alternativa: snapshot por store y merge al leer (port de `_merge_store`, `compose.py:59-63`, sobre `GraphSnapshot`s) | **GAP G5** |
| 11 | `exclude_tags` al leer (`shard_reading.py:30-40`, que deja solo los tag nodes) | Ninguno en snapshot/convert; se puede portar mecánicamente como filtro en `index_from_snapshot` | **GAP G6** (menor, mecánico) |
| 12 | `sldb edges show/check/rebuild/init` y `/edges*` HTTP (retirados) | Sustitutos: `sldb graph get/list/neighborhood/query/snapshot` + `/graph/*` (`graph_routes.py`) + `/lint`. No es equivalencia 1:1: `edges show` devolvía `EdgeRecord`s de un nodo; `graph get` devuelve `GraphNode` con sus edges, y el query language cubre filtros (`language.py`) | ✔ sustitución, con rewrites de ruta en el PR 4 |
| 13 | Semántica por nodo (payload de RelationTypeDoc, hashes en doc nodes, facets) | `KnowledgeNode.semantics`/`source`/`git` (`convert.py:28-35`) — misma conversión de facetas | ✔ equivalente |

**Resumen:** los GAPS que bloquean el retiro son **G1, G2, G3, G4, G5** (G6 es mecánico).
G4/G5 son parciales (existen piezas: `analysis.cycles` para lo acyclico, `federation.py` para el
qualify — pero no tienen home sobre el snapshot).

---

## 3. Comando de porte

Especificación (no implementación). Encaja con el estilo existente: grupo noun-first con
subcomandos con guion bajo `stores` (`semantic-map`, `semantic-export`, `ingest-sldb` en
`graph`). Es una operación de ciclo de vida del store → vive en `stores`.

### `sldb stores migrate-legacy-edges`

```
sldb stores migrate-legacy-edges [--store PATH] [--pythonpath DIR]
                                 [--graph-dir REL] [--kgdb-command CMD]
                                 [--dry-run]
```

| Flag | Default | Qué hace |
|---|---|---|
| `--store PATH` | descubrir (como el resto) | Store a migrar (misma semántica que `open_store`, `open_store.py:24-32`) |
| `--pythonpath DIR` | — | Raíz de import de los modelos del store; **requerido únicamente si G1 está implementado** (nodos field). Sin G1 no importa ningún modelo. |
| `--graph-dir REL` | `runtime/graphs` | Directorio (relativo al root del proyecto) donde se escriben `<name>.nx.json` y `<name>.kg.json` |
| `--kgdb-command CMD` | `kgdb` | Ejecutable para el snapshot `.kg.json` (mismo contrato que `cli/parsers/selfdoc.py:36-37`) |
| `--dry-run` | off | Imprime el plan (qué leería, qué escribiría, qué borraría) sin tocar nada |

**Qué lee** (solo índices fuente, nunca `runtime/edges/`): store index, models indexes,
documents indexes, sections indexes, semantic index y semantic DAG — exactamente lo que ya lee
`SemanticExporter._build_payload` (`export.py:46-60`). Si G1/G2 están implementados, además
importa los modelos por `--pythonpath` (patrón de `edge_rebuild._model_type`,
`edge_rebuild.py:48-59`).

**Qué escribe** (atómico por archivo, como `kgdb_sync.write_kgdb_snapshot`,
`kgdb_sync.py:14-24`):
1. `runtime/graphs/<store>.nx.json` — node-link JSON vía `graph_io.save_graph` (formato de
   `graph_io.py:28-32`: `{directed, multigraph, graph, nodes, links}`).
2. `runtime/graphs/<store>.kg.json` — snapshot KGDB vía `write_kgdb_snapshot` +
   `kgdb --command ingest` (el mismo mecanismo del selfdoc python).

**Qué borra** (solo tras verificar que el `.nx.json` fue escrito):
- `runtime/edges/` (todo el árbol de shards por modelo/documento)
- `runtime/edges.yaml` (el shard del store; `layout.py:91-93`)
- Nada más: los índices fuente, el DAG y el journal se conservan.

**Verificación antes de borrar**: el snapshot producido debe pasar `graph_is_current`
(`kgdb_sync.py:18-28`): mismos ids de nodos y mismo `source`/`ast` hash. Si algo falla, no se
borra nada y el comando termina en 1.

**Idempotente**: sí. Si `runtime/edges*` no existe → imprime "store already migrated" y sale 0
sin escribir. Si existe pero el grafo nuevo ya está → regenera (es barato) o sale 0 según
`graph_is_current`. Re-ejecutable sin efectos laterales.

**Qué imprime** (estilo de las impresiones existentes, `cli/commands/edges.py:24-25`):
```
Edges migrated: 847 nodes, 5213 edges -> runtime/graphs/pron.nx.json (12KB)
Deleted runtime/edges/ (1027 shards) and runtime/edges.yaml
```
Y con `--dry-run`:
```
Would write runtime/graphs/pron.nx.json (847 nodes, 5213 edges)
Would delete runtime/edges/ (1027 shards) and runtime/edges.yaml
```

---

## 4. Mensaje de error de migración

Condición: `open_store` abre un store que **aún** tiene `runtime/edges/` (o `runtime/edges.yaml`)
y **no** tiene el grafo nuevo (`runtime/graphs/*.nx.json`). Punto de enganche natural:
`open_store` ya ejecuta `migrate_store_layout(store_path, root)` (`open_store.py:36-38`); el
check nuevo va al lado, y el error usa `SLDBStoreError` (tono de `store_discovery.py:20`: oración
de diagnóstico + comando exacto entre comillas simples).

Texto literal:

```
SLDBStoreError: The store at <store_path> still uses the retired edge layer
(runtime/edges/). The graph is now read from the portable snapshots under
runtime/graphs/ (*.nx.json). Migrate this store once, then retry:

    sldb stores migrate-legacy-edges --store <store_path>

The command converts the store's indexed graph to the new format and deletes
runtime/edges/; it is idempotent and safe to re-run.
```

Detalles de redacción que siguen el tono del repo (`store_discovery.py:20-24`): caso
`<store_path>` interpolado, verbo imperativo al final ("Run 'sldb ...'"), comillas simples
alrededor del comando. El comando citado es literalmente el de §3. El error se activa solo en la
fase final del retiro (PR 5, §5): durante la transición los stores tienen ambas cosas
(snapshot nuevo + `runtime/edges/` viejo) y **no** deben fallar.

---

## 5. Orden de ejecución (PRs, main nunca roto)

| PR | Contenido | Gate (main verde en cada paso) |
|---|---|---|
| **0** (este) | El presente plan en `docs/architecture/edges-retirement-plan.md` | 1015 passed |
| **1** | Comando `stores migrate-legacy-edges` (sin borrado efectivo todavía: escribe snapshot + `--dry-run`; el borrado de `runtime/edges` se activa con flag interno `--purge` en PR 4, o se omite) | Suite verde; sobre una KB real: el `.nx.json` generado sin leer shards tiene los mismos nodos/relaciones que `graph snapshot save` actual para las capacidades 1-3 y 13 (`ingest_sldb_nodes`) |
| **2** | Cerrar **G1+G2** en el generador de snapshot (nodos field/relation_type/anchor, edges `has_field`/`extends`/authored/alias, con `--pythonpath`) y **G3** (reglas de `resolve.py` aplicadas al generar, no al componer) | Comparación idéntica de nodos+edges entre el snapshot nuevo y `compose_edge_index` en la KB real y en los fixtures de `tests/api/test_api_edges.py`; suite verde |
| **3** | Cerrar **G4+G5+G6** (validación de edges + ciclos sobre el snapshot; federación por merge de snapshots; `exclude_tags` en `index_from_snapshot`); reescribir `api/edges/edge_reading.py` y `check_edges.py` para leer snapshot con `load_graph`+`index_from_snapshot` en vez de shards | `sldb graph path/cycles/order/components/central/similar`, `/graph/*`, `/lint` y `api.graph.*` pasan contra un store migrado **sin** `runtime/edges/`; `tests/store/test_graph_*.py` y `tests/api/test_api_edges.py` reescritos sobre fixtures de snapshot |
| **4** | Reapuntar los writes (clase B): `payload_save_steps`, `untrack_document`, `index_commit`, `dag_writes`, `selfdoc_write`, `derived_rebuild`, `export`, `ops`, `doc` → regenerar snapshot en vez de `rebuild_edges_indexes`/`refresh_store_edges`; `models/__init__` deja de importar `DocEdges`/`EdgeContribution` | Cada write regenera el snapshot y `graph_is_current` es verdadero después; los tests de invariantes por-write (hash chain) pasan sin `runtime/edges/` |
| **5** | Borrar la capa: los 10 archivos de la lista + lectores huérfanos (`compose`, `shard_reading`, `edge_reading` residual, `validation` residual, `init_relations` residual, `io/shards` edges fns, `layout.edges_*`), grupo `edges` del parser/dispatcher/help (`dispatcher.py:48-50`, `public.py:9,21`, `help_texts`), rama `/edges*` de serve (`routes.py:64-65`), exports muertos de `api/__init__.py`, `cli/commands/edges.py`, tests viejos. Activar el error de migración (§4) en `open_store` | `grep -r "runtime/edges\|edge_rebuild\|rebuild_edges_indexes\|edges_routes\|from sldb.api import .*edges" src tests` → vacío; suite verde con la nueva cuenta de tests; un store legacy (solo `runtime/edges/`) falla con el mensaje de §4 citando el comando exacto |

Regla transversal: **nunca borrar el lector antes de re-puntar el escritor** (PR 3 antes que 4-5), y
**el error de migración se activa al final**, cuando un store con `runtime/edges/` y sin snapshot
solo puede ser anterior al retiro.

---

## GAPS (bloqueantes del retiro)

1. **G1** — nodos `sldb://field/...` + edges `has_field` y `extends`: sin productor en la ruta
   semantic-export → snapshot (requiere importar el modelo, `--pythonpath`).
2. **G2** — contribution tipada: nodos `relation_type`/`anchor` y edges `relation_doc` /
   `applies_to_*` / alias: sin productor.
3. **G3** — reglas cross-document de `resolve.py` (condition/axis heredados, reverse de
   undirected, dangling authored → problema): el snapshot guarda edges crudos, sin resolución.
4. **G4** — validación de edges contra relation types (tipo desconocido, endpoints, clases con
   herencia, cardinalidad): el `/lint` y `sldb edges check` se quedan sin equivalente. Solo lo
   acyclico tiene pieza (`analysis.cycles`).
5. **G5** — federación de lectura (`include_linked`, ids calificados `store:Model:name`) sobre
   snapshots.
6. **G6** (menor) — `exclude_tags` como filtro en `index_from_snapshot`.

No son gaps (retiro intencional): rebuild incremental por-shard (8), staleness (9).

---

## Consumidores que sorprendieron

1. **La capa nueva lee a la capa vieja.** `store/graph/` (analysis networkx, convert, executor,
   api.graph entero) obtiene su `EdgeIndex` de `compose_edge_index` sobre los shards de
   `runtime/edges/`. "La capa nueva" no tiene hoy fuente propia de verdad: el retiro es un
   re-punteo del input de toda la capa graph, no borrar 10 archivos (§0).
2. **`cli/serve/lint_routes.py`** — fuera de la lista de retiro, pero consume `check_edges` en
   `/lint` (`lint_routes.py:62`) y queda huérfano: hay que reescribirlo sí o sí.
3. **`api/__init__.py` es contrato público** ("Consumers (pron, kgdb, deskops...)"),
   `api/__init__.py:3-7`. Retirar la capa toca la API de librería (≈20 símbolos de edges), no
   solo el CLI.
4. **`ast.py:21` y `build_ir.py:82-88`** mencionan "edges" y son falsos positivos (literales del
   SCHEMA del AST y edges del IR por-documento, respectivamente): clasificados C.