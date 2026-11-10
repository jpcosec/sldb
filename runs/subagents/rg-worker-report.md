# rg-worker: rule_graph no compone la federación entera de stores enlazados

TaskDoc: `desk/tasks/task-reglas-rule-graph-no-compone-la-federación-entera-de-stores-enlazados-27-s-por-comando-de-deskops.md` (task.code).
Rama `wt/rule-graph-local`, base `63b8d8c7`. Commit de código: `d0e3d440`. Fecha: 2026-11-10.
Scripts, logs y datos crudos: `~/proyectos/SLDB_1/coord2-ccconfig/rg/`.

## Resumen

`rule_graph` compone los stores enlazados solo cuando alguna regla del store puede leer un
documento de un store enlazado. Lo decide un análisis estático sobre el AST de las reglas y el
índice propio del store (opción a). En el desk nuevo de `deskops init`, que es el caso del
informe de perf:
- `rule_graph` baja de 26,3 s a 0,27 s en frío;
- `deskops show task` baja de 29,8 s a 1,4 s, con la misma salida.

Los findings no cambian en ninguno de los 6 desks (10 casos), y los tests de s4 pasan todos.

Una salvedad sobre b4: el desk del propio repo de deskops no registra `RuleDoc`. Ahí
`show task` nunca llama a `rule_graph` y tarda 2,8 s antes y después. Ese tiempo es de un
`edges_from` local de deskops, y se va en leer shards (ver «Lo que queda fuera»).

## s1 / b4. Mediciones

### Montaje (`setup-copies.sh`)

- **b4.**
  - `/dev/shm/sldb-rg-desk` copia `desk/`, `.sldb/` y `.sldb_cache/` de `~/proyectos/SLDB_1/deskops`. Los shards de aristas viven en `.sldb_cache`: sin él, el índice sale vacío.
  - Los stores enlazados se copian en `/dev/shm/sldb-rg-{sldb,spec2viz,pron,scion}`.
  - Los enlaces se reapuntaron en `store.yaml` y en `core/store_index.yaml` de cada copia, incluidos los de vuelta a deskops. La federación queda como la real: 6 stores, unos 29 000 nodos.
- **Código de deskops.** `/dev/shm/sldb-rg-deskops-main` = `git archive origin/main` (`7a875176`). El `main` local del checkout está 114 commits atrás y no tiene CC32.
- **Desk nuevo.** `/dev/shm/sldb-rg-init` se creó con `deskops init`, con el store dueño en la copia de b4, y una tarea `task.code` (`task-rg-probe`). Es el montaje del informe de perf: ahí corren las 7 reglas de activación.
- **Antes.** Mismo código de sldb llamando a `rule_graph(store)`, que compone como siempre (el default no cambió), o `/dev/shm/sldb-rg-base` = `git archive 63b8d8c7`.

### Tabla

| medición | antes | después |
|---|---|---|
| `rule_graph`, desk nuevo (13 docs locales), frío | **26,32 s** (28 887 nodos) | **0,27 s** (481 nodos) |
| `rule_graph`, desk nuevo, caliente | 3,70 s | 0,06 s |
| `deskops show task task-rg-probe --root /dev/shm/sldb-rg-init` (3 corridas) | **29,77 / 29,80 / 30,06 s** | **1,42 / 1,42 / 1,42 s** |
| `rule_graph`, store del repo de deskops (266 docs locales), frío | 26,57 s (28 842 nodos) | 1,59 s (1 772 nodos) |
| `rule_graph`, store del repo de deskops, caliente | 3,34 s | 0,25 s |
| `deskops show task <primera de list tasks> --root /dev/shm/sldb-rg-desk` | 2,74 / 2,75 / 2,74 s | 2,81 / 2,76 / 2,86 s |
| `load_edge_index(False)` / `(True)`, store de deskops (sin `_COMPOSED`) | 0,92 s, 1 772 nodos / 9,51 s, 28 842 nodos | sin cambio (b6) |

La primera tarea de `deskops list tasks` en la copia es
`task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados`.

La salida de los dos `show task` es idéntica antes y después (`diff` vacío).

Crudos:
- `s1-before-probe.txt`, `s1-before-probe-init.txt`, `s1-after-probe-rg.txt`;
- `s1-before-show.txt`, `s1-after-show.txt`.

### Objetivo s1

| objetivo | resultado |
|---|---|
| `rule_graph` < 1 s | **Cumplido en el desk nuevo**: 0,27 s. **No cumplido en los stores grandes**, aunque no componen la federación. En frío, sobre su índice propio: repo de deskops 1,59 s (266 docs, sin `RuleDoc`: ningún comando de deskops llama ahí a `rule_graph`), y con reglas sembradas 6r/deskops 1,60 s, 6r/graph_ui 1,22 s y 6r/sldb 2,05 s (`s3-decision.txt`, última sección). En caliente todos quedan en 0,17-0,28 s. |
| `deskops show task` < 2 s | **Cumplido** donde corren las reglas: 1,42 s. En el desk del repo de deskops es 2,8 s, igual que antes. Ese tiempo no viene de `rule_graph`. |

Lo que queda en esos dos casos es leer el índice **local**. El cProfile de `rule_graph` en el
store de deskops da 3,7 s bajo el profiler, y casi todo es:
- `load_edges_shard` → `yaml_load` (1,9 s, yaml en Python puro);
- `_cached_shard` → `model_copy`/`deepcopy` (1,3 s).

Las dos cosas están en `src/sldb/store/io/` (`shards.py`, `utils.py`), fuera de los archivos de
la tarea. Las propuestas 2 y 3 del informe de perf (no copiar por lectura y usar
`yaml.CSafeLoader`) atacarían ese resto. No las toqué; quedan para que el coordinador decida.

## s2. Diseño elegido: (a) análisis estático, conservador

**Por qué (a) y no (b) ni (c).**
- (a) alcanza: en todos los desks medidos con reglas, todas las reglas resultan locales, y el costo baja al del índice propio.
- (b) obliga a leer los shards de los stores enlazados para encontrar los vecinos (las aristas inversas viven en el otro store). Agrega complejidad sin ganancia en los casos reales.
- (c) no hizo falta (b3).
- (a) es correcta por construcción porque, ante cualquier duda, compone como antes.

**Por qué un documento local lee lo mismo en el índice propio que en el compuesto.** Revisé
`compose.py`, `federation.py`, `resolve.py`, `declared_resolution.py`,
`composition_targets.py` y `doc_anchor_states.py`:
- Al componer, el store local va primero y `nodes.setdefault` conserva sus nodos. El payload, los modelos y los `semantics` de un documento local son los mismos.
- `qualify_id` nunca quita un prefijo de store. Una arista de un store enlazado nunca apunta a un documento local: un id local tiene un solo `:`, y todo lo del enlazado queda `alias:Model:name` o ya traía alias.
- La resolución por ruta (`_owners_by_path`) excluye a los documentos enlazados como dueños.
- Un id suelto de un documento local se resuelve con prefijo vacío, o sea, solo contra documentos locales.

**Dónde puede aparecer el store enlazado.** Solo en estos casos. `rule_reach.needs_linked`
compone si se da cualquiera de ellos:

1. **Familias de modelos.** El modelo de un documento local, o una de sus bases transitivas, no tiene nodo de modelo en el índice propio pero lo registra algún store de la federación. En ese caso `model <= X` podría leer distinto. Una base que no registra nadie (`OperationalArtifactDoc` y `PrimitiveDoc` en todos estos desks) tampoco está en el compuesto, así que no cuenta.
2. **Pasos `rel:`.** Alguna regla tiene un paso `rel:<tipo>`. Tipos de relación, tags y modelos son vocabulario compartido entre stores, así que un paso así puede pasar por ellos y llegar a documentos enlazados. Lo mismo vale para `composes`, que puede resolver desde un enlazado hacia una ruta local.
3. **Campos de los caminos.** Un campo que nombra un paso de camino (directo o `^campo`, recogido del AST de `subject`, `where` y `condition` con `predicate_parser` y `predicate_ast.walk`, b2) cumple una de estas dos condiciones en un documento local:
   - tiene una referencia sin resolver que nombra `alias:Model:name`, que solo el compuesto resuelve;
   - tiene una arista `references` hacia un documento no local.
4. **Anclas.** Un ancla de documento local (`<campo>__anchor_state`) nombra `doc:alias:Model:name`. Su estado sería `lost` en el índice propio e `intact` en el compuesto.
5. **Reglas que no parsean.** Una regla que no parsea compone. Un store sin enlaces nunca compone.

**Sujetos.** Un sujeto que no es local (`rules check --subject alias:...`, `rules explain`,
`transition_findings`) se evalúa sobre el compuesto. Lo hace `rule_subjects.subject_in`, que
compone antes de resolver un id `alias:Model:name`, porque solo el compuesto lo nombra, y
después usa `rule_graph.reading`.

**Firmas (b6).**
- `load_edge_index` no cambia.
- `rule_graph(store, linked=True)` agrega un parámetro opcional cuyo default compone como hoy. Así `run_view` (filas que pueden ser de stores enlazados) y `tag_tree` no cambian, y `api/views` no se tocó.
- Los evaluadores de `sldb.api.rules` llaman `rule_graph(store, None)`: `rules_check`, `rules_explain`, `rules_on_check`, `on_transition`, `on_write` y `store_findings` de la familia de tags.
- `RuleGraph.linked` dice qué índice se cargó.

**Efectos sobre la caché de reglas (`on_check`).**
- Las estampas de una regla «wide» digieren `graph.index_documents` y las de una no wide incluyen a los vecinos. Con el índice propio no hay vecinos enlazados, así que la primera corrida tras el cambio recalcula una vez. Los findings son los mismos, porque la caché nunca es autoridad.
- El dirty set ya no recibe ids `alias:...`. Antes los recibía, pero nunca coincidían con documentos locales.

**Corrección hecha durante s3.** En el desk de sldb, los recibos `ReviewDoc` tienen `subject`
con forma de ancla (`doc:TaskCodeDoc:x`) sin resolver. La primera versión contaba el prefijo
`doc:` como alias y componía por un falso positivo. `qualified` ahora quita `doc:` antes de
contar. Lo cubre un test.

Archivos:
- `src/sldb/api/rules/rule_reach.py` (nuevo);
- `rule_graph.py`, `rule_subjects.py`, `rules_check.py`, `rules_explain.py`, `rules_on_check.py`, `rules_on_transition.py`, `rules_on_write.py` y `builtin_tag_rules.py`;
- `tests/api/test_rules_linked_reach.py` (nuevo);
- `CHANGELOG.md`.

No toqué `src/sldb/store/edge_index/`.

## s3 / b5. Findings de los 6 desks

Copias: `/dev/shm/sldb-rg-6/{deskops,sldb,spec2viz,scion,pron,graph_ui}`, con `desk/`,
`.sldb/` y `.sldb_cache/`. graph_ui se reapuntó a `../deskops`.

Script: `findings.py`. Para cada desk corre:
- `api.rules_check(store)` sin sujeto;
- `api.rules_explain` de cada regla `on_transition` sobre cada documento de su dominio.

Antes = base `63b8d8c7`, después = esta rama. Se compara el JSON entero (`run-findings.sh`).

**Ninguno de los 6 desks registra `RuleDoc` ni declara `tag_namespaces`.** Ahí `rules check`
da `[]` antes y después de forma trivial. Para que la comparación ejercite algo:
- En `/dev/shm/sldb-rg-6r/<desk>` (copias de las copias) `seed-rules.py` registra `RuleDoc` y siembra, por cada modelo de tarea del desk, una regla `on_transition` con la condición de activación de deskops (`any(^subject: …preflight) and any(^subject: …bundle) and all(depends_on: status = "closed")`) y una `on_check` `all(depends_on: status = "closed")`.
- Desks con tareas: deskops (`TaskRefactorDoc`), sldb (`TaskCodeDoc` y `TaskDocsDoc`, con `depends_on` y recibos reales) y graph_ui (`TaskDoc`). spec2viz, scion y pron no tienen tareas.
- Se suma el desk nuevo de `deskops init`, con sus 7 reglas de activación reales.

| caso | `rules check` (n) | explain (n) | decisión después | antes = después |
|---|---|---|---|---|
| 6/deskops | 0 | 0 | sin reglas | **iguales** |
| 6/sldb | 0 | 0 | sin reglas | **iguales** |
| 6/spec2viz | 0 | 0 | sin reglas | **iguales** |
| 6/scion | 0 | 0 | sin reglas | **iguales** |
| 6/pron | 0 | 0 | sin reglas | **iguales** |
| 6/graph_ui | 0 | 0 | sin reglas | **iguales** |
| 6r/deskops | 0 | 1 (false) | local | **iguales** |
| 6r/sldb | 0 | 3 (false) | local | **iguales** |
| 6r/graph_ui | 0 | 2 (false) | local | **iguales** |
| init | 0 | 1 (false) | local | **iguales** |

`rules check` sale en 0 en los casos sembrados porque las reglas `on_check` sobre `depends_on`
se cumplen: los `depends_on` sin resolver no se alcanzan, igual antes que después.

Crudos:
- `findings/*.{before,after}.json`;
- `findings-run.log`, `findings-run-after3.log` (código final);
- `s3-decision.txt` (por qué cada store decide local).

El caso que **sí cruza** lo fija el test nuevo:
- `test_a_rule_whose_path_crosses_into_a_linked_store_still_sees_the_linked_document`: `X:x1` tiene `depends_on: other:X:o1`, con `o1` abierto en el store enlazado. `rule_graph(store, None).linked` es True, y `rules check` y `rules explain` dan el finding con el testigo `other:X:o1`.
- Los otros tres tests cubren:
  - reglas locales: índice propio, mismos findings, y el default sigue componiendo;
  - un sujeto `other:X:o1` en `rules explain` y en `rules check --subject`;
  - la forma de ancla.

## s4. Tests (de a uno, `run-tests.sh`)

Logs en `rg/tests/`.

| test | resultado | pared |
|---|---|---|
| `tests/api/test_rules_linked_reach.py` (nuevo) | 4 passed | 1,2 s |
| `tests/api/test_rules_evaluation.py` | 12 passed | 7,3 s |
| `tests/api/test_transaction.py` | 13 passed | 1,8 s |
| `tests/api/test_transaction_rules_dirty.py` | 4 passed | 2,5 s |
| `tests/test_rules_language_spec.py` | 52 passed | 0,9 s |
| `tests/test_clean_code_rules.py` | 950 passed | 1,7 s |
| `tests/api/test_rules.py` (extra, GO06) | 13 passed | 7,0 s |
| deskops `tests/test_activation_rules.py` | **10 passed** | **43,7 s** (< 90 s) |
| deskops `tests/test_lifecycle_end_to_end.py` | **5 passed** | **73,4 s** (< 90 s) |

La primera corrida del test nuevo falló en el caso del sujeto enlazado: `resolve_subject` no
resolvía `other:X:o1` sobre el índice propio. Eso trajo `subject_in`, y después pasó.

**Prueba del consumidor.**
- deskops `origin/main` (`7a875176`) en `/dev/shm/sldb-rg-deskops-main`, con `cwd` ahí y `PYTHONPATH=/mnt/ssd/proyectos/SLDB_1/sldb-wt-rg/src:/dev/shm/sldb-rg-deskops-main`.
- Cada log registra `sldb importado de /mnt/ssd/proyectos/SLDB_1/sldb-wt-rg/src/sldb/__init__.py`.
- No medí esos dos tests de deskops contra la base: el informe de perf ya documenta los timeouts.

## s5. deskops

No escribí en deskops. El código de deskops se leyó de copias en `/dev/shm`. El checkout real
solo se leyó (`git archive`, `cp` de `desk/`, `.sldb/` y `.sldb_cache/`).

## Lo que queda fuera

- **Leer el índice local** (shards yaml en Python puro y `deepcopy` en `_cached_shard`, en `src/sldb/store/io/`). Es lo que deja `rule_graph` en 1,6 s en el store de 266 documentos de deskops y `show task` en 2,8 s en ese desk sin reglas. Está fuera de los archivos de la tarea.
- **`live_stale`**. Ya no rehashea la federación en las evaluaciones de reglas locales (solo el store propio). En `run_view` y `tag_tree` sigue igual.
- **`docs/architecture/rules.md`** no menciona que la evaluación usa el índice propio cuando puede. Está fuera de los archivos de la tarea.
- **Opción (b)** queda como mejora futura para stores cuyas reglas sí cruzan: hoy componen la federación entera, como antes.
