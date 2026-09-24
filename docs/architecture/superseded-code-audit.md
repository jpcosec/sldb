# Auditoría de código superseded en `src/sldb/`

Inventario con evidencia, sin refactor y sin borrar nada. Complementa y extiende
[`edges-retirement-plan.md`](edges-retirement-plan.md): este documento cubre lo que el plan de
edges no tocó (kgdb↔sldb, islas muertas, compat bridges, derivados sections/semantic/cache).

- Base: `1d232ae`, rama `docs/superseded-audit`.
- Línea base de tests: `PYTHONPATH=src python -m pytest -q` → **1015 passed** (2026-09-24).
- Método: censo AST de importadores sobre `src/` + `tests/` (script propio, incluye imports
  relativos), greps dirigidos para cada símbolo sospechoso, diff entre pares duplicados.

Clasificación: **(i)** muerto de verdad, borrable · **(ii)** superseded con consumidores,
requiere migración · **(iii)** parece duplicado pero no lo es.

---

## 1. Inventario resumido

| # | Hallazgo | Evidencia (archivo:línea) | Lo que lo supersedió | Clase | Tamaño estimado del retiro |
|---|---|---|---|---|---|
| 1 | Capa `runtime/edges/` + sus lectores (la capa nueva lee a la vieja) | `store/edge_index/compose.py:21` (`compose_edge_index` → shards vía `shard_reading.read_store_contributions`, `compose.py:13,58`); `api/edges/edge_reading.py:14`; ver también [edges-retirement-plan.md §0](edges-retirement-plan.md) | `store/graph/` + snapshot portable: `store/export.py:18,43` (`sldb_kgdb_semantic_export` sin tocar edges) → `graph/ingest_sldb.py:20` (`sldb_semantic_export_to_snapshot`) → `cli/parsers/graph.py:70` (`graph ingest-sldb`) | i (capa) / ii (writes clase B, §4 del plan) | ≈ 1.613 líneas directas en 30+ módulos (ver §6.1) |
| 2 | `core/ingest/` completo: isla muerta e inimportable | 0 importadores: `grep -rn "core.ingest" src tests --include="*.py"` → vacío; `ingest/engine.py:3-8` importa `wiki_compiler`/`ontology`, no declarados en `pyproject.toml:21-28` ni instalados (import → `ModuleNotFoundError`); último toque `e83db87` | El ingestion real vive en `store/` (sync por shard, `store/semantic.py`, `store/section_sync.py`) y en `selfdoc/` (`selfdoc/python_scanner.py`); `wiki_compiler` era el producto anterior | i | 9 módulos, 328 líneas |
| 3 | `cli/graph/`: árbol sin `__init__.py`, sin importadores | No existe `cli/graph/__init__.py`; `grep -rnE "from sldb\.cli\.graph import|sldb\.cli\.graph\." src tests` → 0; código casi idéntico a `graph_old/` (`diff -r cli/graph cli/graph_old`); ambos nacidos en `73e4553` (refactor de subagente interrumpido) | `cli/graph_ops/` (único tree vivo: 22 importadores en `src`, p. ej. `commands/find.py:3`, `api/search.py:43-49`) + `cli/search_record.py` | i | 6 módulos, 134 líneas |
| 4 | `cli/graph_old/`: idem, con `__init__` roto | `graph_old/__init__.py:3-5` importa `.query`, `.search`, `.ast_target` que no existen → `import sldb.cli.graph_old` lanza `ModuleNotFoundError`; 0 importadores (`grep -rn "graph_old" src tests` → vacío) | ídem #3 | i | 4 módulos, 79 líneas |
| 5 | `cli/commands/doc_helpers.py`: muerto | `grep -rln "doc_helpers" src tests --include="*.py"` → **0 archivos** (ni el propio módulo se nombra) | Sus helpers (`parse_yaml_string`, `validate_and_render`) duplican `core.exceptions` + `runtime.validation` que los callers reales importan directo | i | 1 módulo, 100 líneas |
| 6 | `cli/commands/legacy.py` + `cli/parsers/legacy.py`: compat activa del "pre-redesign DSL" | `dispatcher.py:58-75` (docstring "pre-redesign spelling", alias `ls|get|glob|raw-find|recover|compose` registrados); `parsers/core.py:8,28`; `parsers/hidden.py:3-8` | El redesign: `QueryCLI`/`LinkCLI` a los que `legacy.py:5-18` re-despacha; el surface per se quedó para no romper el DSL viejo | ii (sus consumidores son el destino del alias, no código nuevo) | 2 módulos, 79 líneas |
| 7 | `cli/commands/model_update.py`: superseded, solo tests | Sin importadores en `src` (`grep -rn "model_update" src --include="*.py"` excl. self → vacío); único uso es `tests/test_cli_v2.py:1664` (monkeypatch sobre un módulo que la ruta real no importa: `models update` va por `commands/models.py:37-39` → `ModelCLI`, no por `model_update.update_model`) | `api/model_registry/reindex_model` + `commands/model.py` (`ModelCLI`) | i (src) — el monkeypatch del test es inerte | 1 módulo, 67 líneas |
| 8 | `cli/commands/predicates_format.py`: muerto | `grep -rn "predicates_format" src tests` → 0 | Formateo implementado inline en el CLI vivo (`cli/commands/predicates.py` no lo referencia) | i | 1 módulo, 42 líneas |
| 9 | Compat bridges sin consumidores: `cli/commands/model_source.py`, `cli/federated_utils.py` | Docstrings "Compatibility bridge" (`model_source.py:1-3`, `federated_utils.py:1-3`); 0 importadores (`grep -rn "commands.model_source\|federated_utils" src tests` → solo docstrings de "moved here" en `api/model_drafts/source_location.py:3` y `api/model_registry/federated_lookup.py:3`) | `api/model_drafts/source_location.py:resolve_definition`; `api/model_registry/federated_lookup.py` | i (todos los consumidores ya migraron) | 2 módulos, 21 líneas |
| 10 | `kgdb/contracts/persistence.py`: muerto en kgdb, **sin** duplicado en sldb | sldb no tiene `PersistenceEntry`/`TransactionManifest` (`grep -rn "PersistenceEntry" src` → vacío); en kgdb solo lo exporta `contracts/__init__.py:10,13`; nadie lo importa (kgdb src, pron, deskops) | El contrato de persistencia de grafo murió con la fusión: no existe "before/after" durable del grafo en sldb | i (kgdb-side, se retira con el shim) | 55 líneas |
| 11 | 4 importaciones sldb→kgdb (el ciclo) | `core/ingest/scanner.py:5-6`, `core/ingest/python_scanner.py:4`, `core/ingest/typescript_scanner.py:3-4` — las 4 dentro del árbol muerto #2 | Nada: kgdb hoy solo debería importar sldb (shims) | i (mueren con #2) | 4 líneas de import |
| 12 | `api/__init__.py`: 47 de 76 símbolos del surface sin importadores internos | Censo: sin `from sldb.api import X` en src/tests para `load_edge_index`, `edge_node(s_of_type)`, `edges_from/to`, `check_edges`, `journal`, `verify_journal`, node-id helpers (`doc_node_id`…), `delete_document`, `deep_set/delete`, `ensure_list`, serializers de edges, reportes pydantic, etc. | Contrato público declarado (`api/__init__.py:3-7`: "Consumers (pron, kgdb, deskops...)"), así que NO es muerto — pero el 100% de los símbolos de edges que exporta muere con #1 (listados ya en el plan, `api/__init__.py:22-28,62-65`) | iii (contrato) / ii (los símbolos de edges) | poda de `__all__` al retirar #1 |
| 13 | `runtime/sections/`, `runtime/semantic/`: **no** hay formato duplicado | `store/io/sections_index.py:8-12` ("no longer written to (PLAN 15 capa 5), still the key"); `semantic_index.py:26-30` (compone shards, legado solo si no hay shards) y `:40-46` (save shardea y unlinkea el legacy); `store/migration.py:69` (`migrate_store_layout`, convertidor vivo, llamado desde `api/stores/open_store.py:36-38`) | En edges el shard-per-doc es lo *viejo*; en sections/semantic el shard-per-doc es lo *nuevo* (PLAN 15 capa 5). Lo único "viejo" es el fallback de lectura para stores no migrados (`sections_index.py:33-37`, `semantic_index.py:26-30`), que `migration.py` elimina en la próxima apertura | iii — no duplicado; el fallback es transitorio y se va solo con la migración | 0 (no retirar) |
| 14 | `runtime/cache/`: dos archivos JSON, **no** dos formatos del mismo dato | `runtime_cache_disk.py:12-14` (`extracted.json`: payloads extraídos, clave por leaf + hash_b) vs `built_cache.py:7-8` (`built.json`: resultados derivados por modelo, clave por hash_b) | Son dos caches distintos (misma filosofía de clave, distinto contenido), cada una en un único formato, ambas derivadas y borrables (`runtime_cache_disk.py:5-7`) | iii | 0 (no retirar) |
| 15 | Analisis de grafo reimplementado a mano fuera de `store/graph/analysis` | No queda: `analysis/` (7 módulos nx) es la única casa (`cli/commands/graph_analysis.py:25`); `edge_index/acyclic.py:11` ya reusa `graph.analysis.cycles`; `graph/executor.py:18` y `neighborhood.py` hacen BFS propio sobre `EdgeIndex` — es la capa de query, no análisis | networkx (`pyproject.toml:28`) | iii | 0 |
| 16 | Parsers/serializadores duplicados entre `core/` y `store/` | No hay: `query_engine/where_parse.py:1-5` es la única gramática `--where` (usada por `cli/commands/find.py:6`, `query_engine/{structural_queries,filter,semantic}.py`, `api/search.py:31`); `core/renderer_engine/yaml.py` es renderizado, `store/io/utils.py` es serialización de índices — no coinciden | — | iii | 0 |

---

## 2. El ciclo kgdb↔sldb

Estado real de los imports entre los dos repos, hoy:

1. **La dirección correcta (kgdb → sldb) ya está instalada.** Los tres shims son re-exports:
   `kgdb/contracts/node.py:7`, `io.py:5`, `base.py:5` importan desde `sldb.store.graph`
   (`KnowledgeNode` vive en `sldb/store/graph/node.py:12`, re-exportado en
   `store/graph/__init__.py:12`).
2. **El ciclo (sldb → kgdb) existe en 4 sitios y todos están dentro de un árbol muerto.**
   `core/ingest/scanner.py:5-6`, `python_scanner.py:4`, `typescript_scanner.py:3-4` importan
   desde el shim un tipo que vive en el propio sldb. Como `core/ingest/` no tiene ningún
   importador (hallazgo #2), el ciclo es 100% latente: borrar `core/ingest/` lo mata entero.
   Ningún otro módulo vivo de sldb importa `kgdb`.
3. **Un test depende del paquete kgdb real (parity), no del shim.** `tests/api/test_api_graph.py:78-81`
   importa `kgdb.ingest.typed`, `kgdb.query`, `kgdb.graph.utils` con `importorskip` — es el test
   de paridad intencional de la transición ("same ids"), y esa parte de kgdb (no-shim) sigue
   existiendo en el repo kgdb (`kgdb/src/kgdb/ingest/typed.py`). No es obsolescencia, es verificación.
4. **`kgdb/contracts/persistence.py` es el único contrato kgdb sin contraparte en sldb** — y no
   hay duplicación porque sldb no tiene equivalente: el concepto ("un update de grafo con hash de
   integridad") no sobrevivió a la fusión en ninguna de las dos formas. Dentro de kgdb es código
   muerto: solo lo referencia su propio `contracts/__init__.py:10,13`, nadie en kgdb/src, pron o
   deskops lo importa.

Qué habría que enderezar (sin hacerlo ahora):
- Borrar `core/ingest/` → elimina los 4 imports de vuelta (§2.2).
- Decidir el destino de `persistence.py` al retirar el shim kgdb: migrarlo a sldb (si el journal
  de escrituras `store/journal/` quiere el contrato) o retirarlo con el shim. Hoy no hay duplicado.
- El test de parity (#2.3) debería re-apuntarse a la ruta interna (`store/graph/ingest_sldb.py`)
  cuando kgdb deje de instalarse.

Volumen: shims kgdb = 55 líneas útiles (110 con `__init__` y `persistence`); ciclo sldb→kgdb = 4 imports en 328 líneas de código que de todas formas es muerto.

---

## 3. Derivados duplicados: sections / semantic / cache

Aplicado el criterio del plan de edges ("lo mismo guardado en dos formas"):

- **sections**: no hay dos formatos. El único formato vivo es el shard por documento
  `runtime/sections/<model>/<doc>.yaml`. El YAML por modelo `runtime/sections/<model>.yaml` ya
  **no se escribe** (`store/io/sections_index.py:8-12`); su lectura es un fallback para stores
  no migrados (`sections_index.py:33-37`) y `save` shardea (`sections_index.py:40-46`).
- **semantic**: idem. `SemanticIndexIO.load` compone shards y cae al archivo único solo si no hay
  shards (`store/io/semantic_index.py:26-30`); `save` shardea y **unlinkea** el legacy
  (`semantic_index.py:40-46`).
- **cache**: `extracted.json` (payloads) y `built.json` (resultados derivados) son dos caches con
  la misma técnica (clave hash de cadena, tier memoria + disco, derivadas y borrables), pero con
  contenido distinto; ninguna duplica a la otra. No hay un formato "viejo" y uno "nuevo".
- **Conclusión**: a diferencia de edges —donde el formato viejo (shards) sigue siendo producido y
  leído por la capa nueva—, aquí el shard es ya la fuente y solo sobrevive el código de
  **conversión** (`store/migration.py:69` `migrate_store_layout`, invocado en
  `api/stores/open_store.py:36-38`) y los **fallbacks de lectura**. Eso no es código superseded:
  es la guarda que hace que un store viejo se migre solo. Retirarlo exigiría garantizar que no
  queda ningún store pre-capa-5 en circulación (pron/deskops/kb_agent), o esperar al retiro de
  esos consumidores.

---

## 4. Cómo se verificó "nadie lo usa"

- Censo AST propio sobre `src/` + `tests/` (maneja imports absolutos y relativos) para cada
  módulo de sldb; los hallazgos #2-#10 se confirmaron con `grep` dirigido adicional porque el
  censo no ve `from sldb.store import <submodulo>` (patrón de `edge_sync.py:11`, `documents_hash.py:19`).
- Regla aplicada: un símbolo usado solo por tests sigue siendo candidato a muerto si el test lo
  referencia sin que la ruta real lo toque (caso `model_update`, #7: el monkeypatch de
  `tests/test_cli_v2.py:1664` cae sobre un módulo que `commands/models.py:37-39` jamás importa).
- El caso inverso: los 47 símbolos de `api/__init__.py` sin importadores internos (#12) **no** se
  marcan muertos porque el propio módulo declara ser contrato público para pron/kgdb/deskops
  (`api/__init__.py:3-7`), y hay consumidores externos que no viven en este repo.

---

## 5. Detalle de los hallazgos nuevos (no cubiertos por el plan de edges)

### 5.1 `cli/graph/` y `cli/graph_old/` — dos copias huérfanas de un refactor interrumpido

Ambos árboles nacen en el mismo commit (`73e4553`, "Massive subagent refactor interrupted by
quota limit"); `e83db87` limpió el resto pero dejó los dos. Ninguno tiene importadores.
`graph_old/__init__.py:3-5` importa módulos inexistentes (`from .query import …` →
`ModuleNotFoundError`). Sus piezas son casi idénticas entre sí (`diff -r` muestra solo
reordenamientos) y su contenido real sobrevive en `cli/graph_ops/` + `cli/search_record.py`
(22 importadores en src, p. ej. `api/search.py:43-49`). Son clase (i) pura: copias muertas que
nadie carga.

### 5.2 `core/ingest/` — la isla pre-ecosistema

328 líneas en 9 módulos que implementan "ingest de raw sources → draft nodes" con
`wikiignore`, manifest CSV (`ingest/manifest.py:16-30`) y un renderer propio
(`ingest/renderer.py`). Depende de `wiki_compiler` y `ontology` (paquetes que no están en
`pyproject.toml:21-28` ni instalados). Cero importadores en src y tests. Es el único sitio del
repo que importa `kgdb` (hallazgo #11). No está roto porque algo lo necesite: simplemente nunca
se cableó al producto sldb actual (el ingestion real lo hacen `store/section_sync.py`,
`store/semantic.py` y `selfdoc/python_scanner.py`).

### 5.3 Compat bridges sin consumidores

`cli/commands/model_source.py:1-3` y `cli/federated_utils.py:1-3` se autodenominan
"Compatibility bridge" y re-exportan desde `api/`. Todos sus destinatarios ya importan desde el
destino final (`api/model_drafts/source_location.py:3`, `api/model_registry/federated_lookup.py:3`
dicen "moved here from … which re-exports these names", pero ya nadie pasa por el re-export).
El motivo del bridge dejó de existir.

### 5.4 El surface público de edges en `api/__init__.py`

El plan ya lista los ~20 símbolos de edges; este censo cuantifica el tamaño del problema del
surface: de los 76 nombres en `__all__`, 47 no tienen ningún importador interno. Se conservan
por contrato, pero cuando #1 muera, la poda del `__all__` (plan §1, fila `api/__init__.py`) debe
avisar a pron/kgdb/deskops — no es un borrado silencioso.

---

## 6. Ranking final: qué retirar primero (impacto / riesgo)

| Orden | Qué | Tamaño | Justificación (una línea) |
|---|---|---|---|
| 1 | `core/ingest/` | 328 lín. | Cero riesgo (nadie lo importa, ni siquiera se importa a sí mismo bien): mata el ciclo kgdb↔sldb completo de un solo golpe |
| 2 | `cli/graph/` + `cli/graph_old/` | 213 lín. | Copias muertas del refactor interrumpido; borrado mecánico sin consumidores; elimina la única `__init__` rota del repo |
| 3 | Capa `runtime/edges/` (plan PR 1→5) | ≈ 1.613 lín. | El mayor volumen y el único con riesgo real (writes clase B + surface público): por eso ya tiene plan propio; aquí se confirma que no hay otra capa con el mismo patrón |
| 4 | `doc_helpers.py`, `predicates_format.py`, `model_source.py`, `federated_utils.py`, `model_update.py` | 230 lín. | Módulos sueltos sin importadores (o test-only); limpieza de bajo riesgo que reduce superficie de confusión |
| 5 | Compat bridges vivos (`legacy.py` x2) | 79 lín. | No urgente: es surface deliberado con alias activos; se retira solo si el mantenedor decide abandonar el DSL `ls/get/glob` |

Los 5 hallazgos más grandes suman ≈ **2.553 líneas** de las 22.390 de `src/sldb/` (≈ 11%):
1.613 (capa edges) + 328 (core/ingest) + 134 (cli/graph) + 100 (doc_helpers) + 79 (cli/graph_old).

---

## 7. Lo que sorprendió

1. **Los 4 imports sldb→kgdb están todos en un árbol que ni siquiera importa.** El "ciclo" que
   parecía un problema de arquitectura viva es en realidad el síntoma de una isla muerta: matar
   la isla mata el ciclo, no hay que "enderezar" nada en el código vivo.
2. **Dos refactors simultáneos dejaron dos copias casi idénticas (`graph/` y `graph_old/`) y una
   tercera que ganó (`graph_ops/`).** El commit interrumpido por cuota de subagente dejó un
   `__init__.py` roto en el repo sin que nadie lo notara — porque nadie lo importa.
3. **Donde el plan de edges ve "shards viejos", sections/semantic tienen exactamente el patrón
   invertido**: el shard-per-documento es lo nuevo y el archivo único es el legado. La lección
   del plan ("re-puntar la fuente, no borrar archivos") no aplica allá porque la migración ya
   está resuelta en vivo por `migration.py` — no hay segunda implementación conviviendo, solo un
   fallback de lectura para stores pre-capa-5.
4. **El contrato "persistencia de grafo" de kgdb no tiene heredero**: `PersistenceEntry`/
   `TransactionManifest` son el único contrato kgdb que no se movió ni se duplicó — simplemente
   quedó sin concepto equivalente en sldb y sin importadores en ningún repo del ecosistema.