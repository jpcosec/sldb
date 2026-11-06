# Changelog

Version note (2026-09-13, updated 2026-10-18): `pyproject.toml` declares `0.1.12`; it was `0.1.0` while PyPI already had `0.1.1`. Existing entries below are historical development records, not a verified registry release inventory. The product-generation label “v1” is separate from package versioning. No new package version or release is created by this documentation reconciliation.

## 0.1.13 — not released yet (no tag, not on PyPI)

- Grafo de proyecto declarado por datos y servido (GD21, plan generalizar-desde-deskops; `docs/architecture/project-graph.md`):
  - `ProjectGraphConfig` y sus partes (`DocumentSurface`, `FileRule`, `FileExclusions`, `DeclaredFileTargets`, `ReferenceField`, `MentionPattern`, `SectionMentions`, `LineMentions`, `MissingTargetKind`) son dato puro: `ProjectGraphConfig.from_mapping(mapping)` carga y `to_mapping()` vuelca con ida y vuelta exacta. Cargar rechaza con `ValueError` que nombra la ruta de la clave una clave desconocida (`project_graph.surfaces[0].closed_document: unknown key`) o un valor que no es escalar, lista ni mapa.
  - `StoreDeclaration.project_graph` (nuevo, opcional): la configuración en `store.yaml`, validada con `from_mapping` al cargar la declaración; una declaración sin la clave se lee y escribe igual que antes.
  - `DocumentSurface.closed` (nuevo, opcional): predicado del lenguaje de reglas evaluado con `where_matches` sobre el payload del documento (la proyección del índice si está trackeado, sin re-extraer; su frontmatter si no); cuando se cumple, el documento es historia (`record: true` en sus aristas). Una superficie sin `closed` nunca está cerrada; un predicado que no parsea se rechaza al construir la superficie.
  - Deprecado: `ProjectGraphConfig(closed_document=callable)` sigue como argumento solo de Python (`DeprecationWarning` al construir); no se carga (`from_mapping` y `store.yaml` lo rechazan como clave desconocida) ni se vuelca (`to_mapping` levanta error que lo nombra). Donde la superficie declara `closed`, gana `closed`. Se retira cuando deskops migre (CC33).
  - `ProjectGraph.edges_to(node_id)`: las aristas que llegan a un nodo, con el mismo registro que `edges_from` (rol, origen, `provenance_path` y `provenance_locator` ruta:línea para las menciones), desde un único mapa inverso construido una vez desde la extracción completa.
  - `sldb.api.project_graph(store)` → `ProjectGraph` con la configuración declarada en `store.yaml` (también `sldb.api.ProjectGraph` y `sldb.api.ProjectGraphConfig`). Memo por proceso con clave la ruta resuelta del store: se recalcula solo si cambia la firma de shards, el índice compuesto leído (la invalidación de cachés existente, `forget_caches`, lo tira), `(ruta, mtime_ns, size)` de cada archivo leído o incluido (documentos de las superficies, documentos declarantes, archivos de las reglas tras las exclusiones, `store.yaml`) o el mtime de cada directorio recorrido; comprobarlo solo hace `stat`, nunca `os.walk` ni `rglob`.
  - CLI `sldb graph project nodes [--kind K] | edges --from ID | --to ID | missing` (`--store`, `--format`, con envelope); `--from` y `--to` son excluyentes y uno es obligatorio (error de uso, exit 2).
  - `sldb serve`: `GET /project-graph/nodes?kind=`, `GET /project-graph/edges?from=|to=` y `GET /project-graph/missing` responden el mismo JSON que el comando con `--format json`; 400 `{"ok": false, "error": ...}` con `from`/`to` ausentes o ambos, o sin `project_graph` declarado. `GET /edges?from=|to=` acepta `include_linked=false` (por defecto `true`, la salida actual no cambia).
- Retiro de los lenguajes viejos de consulta (GO10, plan grafo-operable; `docs/architecture/rules-language.md` §7 y §9):
  - Cambio de contrato de `sldb graph query` (y de `StructuredQuery`): el JSON ya no acepta `conditions`; cada filtro es `{"facet": ..., "where": "<predicado>"}` con un predicado del lenguaje sobre los campos de la facet (sin caminos: un cuantificador o `count` es `SLDBGraphArgumentError`; `where` vacío = sin condición). `FacetFilter` usa `extra="forbid"`: un filtro con `conditions` es `ValidationError` que lo nombra. Una condición vieja se reescribe con la columna nueva de la tabla de §7 (`eq` → `f = v`, `contains` → `"x" in f`, `starts_with` → `f ~ "^x"`, `is_null` → `not has(f)`...; varias condiciones se unen con `and`). `sldb graph query` ya no emite el warning `deprecated/field-condition`. Los cinco ejemplos de `contracts/queries/sldb` usan `where` y devuelven los mismos ids.
  - Se borran `FieldCondition`, `sldb.store.query_engine.where_parse` (`where_parse`, `compile_where`) y las funciones sin uso de `sldb.store.graph.facet_match` (`matches_filters`, `facet_matches`, `condition_matches`, `ordered_*`); sin alias ni módulo puente.
  - `WherePredicateError` se traslada a `sldb.core.exceptions` (sigue siendo `ValueError` y `SLDBError`, mismo mensaje) y se reexporta desde `sldb.store.exceptions`, `sldb.store.graph.language` y `sldb.api`; la importación pública es `from sldb.api import WherePredicateError` (la ruta `sldb.store.query_engine.where_parse` deja de existir).
  - `sldb.notations.where_check.set_where_parser` pasa a llamarse `connect_where_check`.
- Scaffold de store desde carpetas y semillas declaradas (GD26, plan generalizar-desde-deskops; `docs/architecture/store-declaration.md`):
  - `StoreDeclaration` gana `folders` (rutas relativas a la raíz del proyecto) y `seeds` (lista de `sldb.api.Seed`: `{path, mode: if_missing | managed, text | file | document, track}`); `file` admite una plantilla relativa al directorio de plantillas (por defecto `.sldb/`) o `pkg:modulo/ruta` resuelto con `importlib.resources`; `document` es `{model, name, payload}` renderizado con el modelo y, con `track` (por defecto true), trackeado con ese modelo y nombre. `Seed` usa `extra="forbid"` y sus invariantes son validadores pydantic; una declaración sin esas claves se lee y se escribe igual que antes.
  - `sldb.api.scaffold_store(store, *, declaration=None, apply=False, template_root=None)` → `ScaffoldReport` (`created`, `rewritten`, `present`, `conflicts`, `applied`): idempotente, `if_missing` nunca sobrescribe, `managed` compara bytes y restaura; sin `apply` no escribe y las listas dicen lo que pasaría. Las escrituras van dentro de `sldb.api.transaction`. `declaration=` usa una declaración en proceso en lugar de `store.yaml` sin escribirla.
  - `sldb.api.build_store(store, *, apply=True, generate=None)`: el build de `sldb stores build` como función de la API; aplica la declaración y después el scaffold, en un solo reporte cuya única clave nueva es `scaffold`. Los generadores los pasa la CLI (`run_generators`).
  - CLI `sldb stores scaffold [--apply] [--format]` (exit 1 ante un conflicto) y `sldb stores build` con la sección `scaffold` en su salida JSON/YAML; las demás claves, el resumen y el exit no cambian.
- Reglas evaluadas en su momento (GO08, plan grafo-operable; `docs/architecture/rules.md` §9-§11):
  - `on_write`: `save_document_payload` evalúa, tras pinnear las anclas y antes de escribir, las RuleDoc `on_write` que aplican al documento sobre el payload nuevo. Un error levanta `SLDBRuleViolationError` (nuevo, `sldb.core.exceptions`; una línea `<code>: <what>` por error, por export id de la regla) y no se escribe nada; en el envelope es `rules/violation`, exit 1. Los alerts salen por la nueva `sldb.core.finding_route`, que la CLI conecta a `alert_sink` (`warnings`). Un store sin `RuleDoc` registrado escribe como antes.
  - `on_transition`: `edges_holding` y la nueva `sldb.api.edges_blocked` aceptan `document=` (el documento que transiciona); sus reglas `on_transition` se evalúan sobre el sujeto. `EdgeRecord.findings` (nuevo, opcional; fuera de todo dump mientras es `None`): alerts en las aristas de `edges_holding`; con un error ninguna arista se cumple y `edges_blocked` las devuelve con todos los findings. `sldb edges show --holds-for DOC` pasa `DOC`.
  - `on_check`: `sldb stores check` (y `check_store`, `GET /stores/check`) suma los findings de las reglas `on_check` (`sldb.api.rules_on_check`) y los alerts de `check_doc_anchors`; exit 1 solo ante un error.
  - Caché derivada en `.sldb_cache/rules/` (un JSON por regla, nombrado por su `content_hash`, y `dirty.json`), bajo el bloqueo de store: una segunda evaluación sin cambios no recalcula nada; cambiar una regla recalcula su familia; borrar la caché da los mismos findings. Las clausuras `+` son las semi-naive de GO05 (terminan con ciclos).
  - El `what` de un finding decidido por un cuantificador termina en ` (witness: <Model:name> <seen>)`; también en `sldb rules check`.
  - `sldb edges check` falla ante una condición de arista que no parsea.
- Anclas a documentos con hash de contrato (GO07, plan grafo-operable; `docs/architecture/anchoring.md` §6):
  - `StructuredNLDoc.__doc_anchors__` (nuevo atributo de clase): campos `str` o `list[str]` cuyos valores son vacíos o `doc:Model:name[@sha256:<64 hex>]`; la forma la valida un validador pydantic del modelo base (`sldb.models.doc_anchor_value`) y un valor malformado es `ValidationError` al escribir. `Provenance.from_` valida igual cada elemento que empieza por `doc:`; los demás (`code:...`) no cambian.
  - Al cargar un modelo (`resolve_model_ref`), `__doc_anchors__` que nombra algo que no es un campo `str`/`list[str]`, o un campo con el sufijo reservado `__anchor_state`, es `SLDBModelError` (`sldb.store.model_contract.doc_anchor_fields`).
  - `save_document_payload` pinnea: un ancla sin `@sha256` (en un campo `__doc_anchors__` o en `from:`) se guarda con el hash de contrato actual del destino (`contract_hash`, GO02 §5); un destino no trackeado deja el valor sin hash.
  - Cada ancla de un campo `__doc_anchors__` es una arista `references` con el nombre del campo hacia `Model:name` (sin el sufijo); `from:` no genera aristas.
  - `compose_edge_index` agrega en memoria `<campo>__anchor_state` (`intact` | `changed` | `lost`; lista alineada para `list[str]`) a la facet `payload`; no se escribe al shard y `EDGE_INDEX_VERSION` sigue en 5. El alias `anchor_state` del lenguaje también se lee al atravesar `^F` (desde el elemento alcanzado, que tiene el campo `F`).
  - `sldb.api.check_doc_anchors(store, pythonpath=None)` (también en `sldb.api.anchors`): alertas `anchors/doc_changed`, `anchors/doc_lost`, `anchors/provenance_changed`, `anchors/provenance_lost`; `sldb anchors check` las agrega (`doc_anchors` en la salida JSON, en `warnings` con `--envelope`), exit 0 si solo hay alertas. No hay `reconnected` para documentos.
- Transiciones como datos de la arista (GO09, plan grafo-operable; `docs/architecture/edges.md`):
  - Convención de `RelationDoc.attributes` para una transición: `sets` (mapa campo → escalar YAML o lista de escalares; `null` asignable) y `terminal` (booleano que sldb solo transporta); ausentes o `null` valen `sets = {}` y `terminal = false`; otras claves se conservan y no entran a los efectos. Es un validador pydantic de `RelationDoc` (`sldb.models.transition_attributes`): escribir un `RelationDoc` con `attributes` no mapa, `sets` no mapa, `terminal` no booleano o un valor de `sets` mapa o lista anidada se rechaza con `ValidationError`.
  - `EdgeRecord.effects` (nuevo, opcional): solo lo llena `edges_holding`, como `{sets, terminal}` con `{campo}` sustituido desde el sujeto (sintaxis de `where_subject`, escalar en su forma YAML: `true`/`false`, números, strings tal cual). Un `{campo}` ausente, `null` o no escalar hace que la arista no se cumpla. Con `effects = None` la clave no aparece en ningún dump: la salida de `edges_from`, `edges_to`, `sldb edges show` y los shards no cambia; `sldb edges show --holds-for` sí la muestra.
  - `sldb.api.effects_of(attributes, subject)` (la resolución) y `sldb.api.apply_effects(subject, effects, model)`: función pura que reemplaza o agrega las claves de primer nivel de `sets` en una copia del sujeto y valida el payload completo contra la clase `model` (levanta su `ValidationError`); nunca persiste.
- Selectores de documento (GD23, plan generalizar-desde-deskops; `docs/architecture/selectors.md`):
  - `sldb.api.select_documents(store, selector, expect="many"|"one")` → lista ordenada de `{export_id, model, name, path}` (los del store dado por `path`, después los enlazados por alias y `path`). El selector es un mapa (o `sldb.api.Selector`, pydantic) con claves combinadas por conjunción: `ref` (lo que acepta `doc_status`: `name`, `Model/name`, `Model:name`, ruta trackeada, con `alias:` para un store enlazado directo, que se alcanza aunque `include_linked` sea false), `prefix` (con `expect="one"`, exacto primero y si no prefijo único: la regla `resolve_selector` de deskops), `path_glob` (patrón shell sobre la ruta relativa a la raíz, `**` recursivo), `model` (el modelo y los que lo extienden, por `base_models` de los índices), `where` (lenguaje de reglas sobre la facet `payload` del índice de aristas, sin extraer ningún documento) e `include_linked` (solo los stores enlazados directamente; no transitivo). Una clave vacía o desconocida es `ValidationError`; un `where` que no parsea, `WherePredicateError`.
  - `expect="one"` sin resultados levanta `SLDBDocumentTargetError` (`Unknown document: <selector>`); con varios, `AmbiguousSelectionError(SLDBDocumentTargetError)` (nueva, en `sldb.core.exceptions` y `sldb.api`) con `candidates` (export ids en el orden de salida) y los candidatos en el mensaje.
  - El núcleo vive en el store (`sldb.store.query_engine.document_selection`, filtros en `document_selection_filters`), porque el store no importa `sldb.api`; `glob_structural` y `find_structural` eligen los documentos de su alcance por él (modelo exacto o familia) sin cambiar su salida: el `where` de `sldb query find` sigue evaluándose sobre el payload de cada documento, como antes.
  - CLI `sldb docs select [--ref] [--prefix] [--path-glob] [--model] [--where] [--one] [--include-linked] [--format]` (solo flags; `--one` sale 1 con el mensaje del error; con `--envelope`, `docs/missing` y `docs/ambiguous`) y `GET /docs/select` con los mismos nombres como query params (404 desconocido, 409 ambiguo con `candidates`, 400 clave vacía o `where` inválido); ambos responden `{selector, expect, documents}`.
- Transacción multi-documento y `/save` atómico (GD24, plan generalizar-desde-deskops; `docs/architecture/transactions.md`):
  - `sldb.api.transaction(store, pythonpath=None)` → `Transaction`, anidable (una transacción interna sobre el mismo store se une a la externa; solo la más externa revierte). Escribe en el momento y, ante excepción, restaura bytes, entradas y shards de cada archivo tocado (generaliza `store/io/rollback.py`, que ahora expone `snapshot` y `restore_all`), después invalida las cachés existentes. Operaciones: `create`, `update` (guardas `expected_source_hash` y `expected`), `delete`, `move`, `track`, `untrack`, `write_file` (guarda `expected_sha256`) y `record`.
  - `sldb.api.move_document(store, ref, new_path)`: mueve el archivo y re-trackea con el mismo nombre; las aristas entrantes siguen resolviendo.
  - `sldb.api.apply_batch(store, changes)` → `BatchReport`: prevalida todos los cambios (forma, modelo, round-trip, guardas, destinos) y los aplica en una transacción en orden create/track → update → move → untrack/delete.
  - Excepciones nuevas: `ConflictError(SLDBStoreError)` (`ref`, `expected`, `actual`; en `sldb.core.exceptions` y `sldb.api`) y `RollbackError(SLDBStoreError)` (`unrestored`, encadenada a la excepción original; en `sldb.store.io.rollback`, reexportada por `sldb.api`).
  - **Cambio de contrato (DA2)** en `POST /save`: una falla a mitad de lote ya no deja `completed` parcial; responde 500 `{"ok": false, "error": ..., "rolled_back": true}` con el store como antes. Mismo request, misma respuesta exitosa, mismos 409/422; acepta además `expected_source_hash` y las acciones `move`, `track` y `untrack`. Un `update` con payload inválido responde 422 (antes se perdía en un 500).
  - G4: `tests/api/test_write_paths_validate.py` prueba que `sldb fields update`, `sldb docs update`, `/save`, `apply_batch` y `transaction` rechazan un payload que el `model_validator` del modelo rechaza, sin mover archivo, entrada ni índice.
- Reglas como documentos (GO06, plan grafo-operable; `docs/architecture/rules.md`):
  - `sldb.models.rule_doc.RuleDoc` (exportado en `sldb.models`): `subject` (`model <= X` o una conjunción de nivel superior de esos términos), `where` opcional, `condition`, `severity` (`error` | `alert`), `moment` (`on_write` | `on_transition` | `on_check`) y `message` opcional. Sus validadores pydantic rechazan una `condition` o un `where` que no parsean, un `subject` con otra forma y un valor fuera del vocabulario; escribir una RuleDoc cuyo `subject` nombra un modelo no registrado se rechaza con el error existente `Model 'X' not registered.` (`create_document`, `save_document_payload`, `sldb docs create|update`).
  - `sldb.api.rules` (`rules_check`, `rules_explain`, `explain_exit`, `refuse_unknown_family`; también en `sldb.api`): las reglas son las RuleDoc del store local, leídas de la proyección del índice y evaluadas con `GraphBackend.eval`.
  - CLI `sldb rules check [--subject DOC]`: cada resultado `false` es un `Finding` de core con la severidad de la regla y código `rules/<nombre>`; cada `incomplete`, un alert `rules/<nombre>/incomplete`. Sale 1 solo si hay algún error. Sin `--subject`, solo las reglas `on_check` sobre los documentos locales de su familia.
  - CLI `sldb rules explain RULE SUBJECT`: `data = {rule, subject, finding}` con el finding de eval (`node`, `holds`, `clause`, `seen`), también cuando se cumple; exit 0/1/2 por `holds` y 3 cuando la regla no aplica (`applies: false`, `reason: subject|where`, `detail`).
  - `contracts/layers.toml`: la arista `models → store` (el parser del lenguaje, importado de forma diferida por los validadores de `RuleDoc`) queda contada como R6 pendiente.
  - `docs/opsys/bridge_primitives/README.md`: la sección `Constraint` se marca como reemplazada por `RuleDoc`.
- Lenguaje de predicados unificado (GO05, plan grafo-operable; `docs/architecture/rules-language.md`):
  - `sldb.store.graph.language`: parser (`parse_predicate` → `Predicate`) y evaluador del lenguaje de GO02: `and`/`or`/`not` con paréntesis, caminos `campo`, `rel:<tipo>`, `^` y clausura `+` (pasos unidos por `.`), cuantificadores `any`/`all`/`none`, `count(...) cmp n`, sustitución `{campo}` desde el sujeto, `incomplete` (Kleene fuerte) en el borde de links y findings `{node, holds, clause, seen}`. `sldb.store.query_engine.rules` es la fachada de los tests de spec (52 verdes).
  - `GraphBackend.eval` evalúa caminos sobre el índice compuesto y, sin sujeto, el dominio entero (la proyección cargada, o todos los documentos). Al atravesar un campo `F` con `F__anchor_state` en el origen, cada elemento expone `anchor_state`.
  - API única: `where_matches`, `edges_holding`, `StructuredQuery` y `--where` evalúan con el lenguaje; nuevas `sldb.api.where.where_findings` (un store, sin re-extraer) y `where_records`.
  - CLI: `sldb find --where` acepta el lenguaje completo (caminos sobre el índice del store) y `--explain` agrega `findings` por documento evaluado. `sldb --envelope graph query` con filtros `FieldCondition` lleva un warning `deprecated/field-condition` que nombra el predicado de reemplazo; la salida no cambia.
  - Deprecados (GO10 los retira): `where_parse.compile_where`, `where_parse.where_parse` y construir `FieldCondition` emiten `DeprecationWarning`.
  - Cambios de resultado declarados (tabla de equivalencia, goldens en `tests/fixtures/where_goldens/`): `f != <número>` ya no cumple sobre un campo ausente; ordenar `None` o tipos mezclados da `false` en vez de `TypeError`; en `StructuredQuery`, `contains` sobre una cadena es subcadena e `is_null`/`is_not_null` tratan `""` como ausente.
- Transclusión de campos y segmentos ricos de diagramas y vistas en /document/segments (SV03):
  - `sldb.api.segments`:
    - `source_ref.py`: `SourceRef` incorpora el campo opcional `field: str | None = None`.
    - `composition_spec.py`: Soporta `ref: Literal["document", "field", "view", "spec"]`.
    - `composition_piece.py` y `field_segment.py`: incorporan los campos opcionales `projection: dict | None = None` y `table_data: dict | None = None`.
    - `field_ref_resolver.py`: `FieldRefResolver` resuelve referencias `Model:name#campo`, `docs/<Model>/<name>/<campo>` y `docs/<name>/<campo>` devolviendo `{model, doc, path, field, value, payload}`.
    - `segment_enrichment.py`: Enriquecimiento de segmentos con vistas resueltas (`resolve_view` / `evaluate_projection_view`) y tablas estructuradas (`table_data`).
    - `build_document_segments.py`: Inyecta `FieldRefResolver` en `render_with_spans` y enriquece los nodos con `projection` y `table_data`.
  - `sldb.models.structured_doc`: `StructuredNLDoc.compose_field` y `render_payload` aceptan `field_resolver`; cuando `ref == "field"`, resuelve campos remotos emitiendo `CompositionPiece` con `SourceRef(model, doc, path, field)`. Sin resolver inyectado, rinde vacío preservando la pureza del renderizador.
  - Documentación de arquitectura en `docs/architecture/segments-and-transclusion.md`.
  - Suite de tests en `tests/segments/test_field_transclusion_and_diagram_segments.py`.
- Visual notation and projection view resolver, store synchronization, CLI, and serve routes (SV02):
  - `sldb.api.notations`:
    - `notation_view.py`: `resolve_view` and `resolve_documents` resolving glyphs, compartments (`data.attributes`), template/keyword interpolation, edge ordering, UML fragments, and legends.
    - `projection_view.py`: `evaluate_projection_view`, `list_projection_views`, and `save_projection_view` evaluating node where-predicates, relation filters, layout, palette ink, and notation styling.
    - `notation_sync.py`: `sync_palette` and `sync_notation` writing `PaletteDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, and `RelationTypeDoc` into stores without intermediate YAML dependencies.
    - Re-exported in `sldb.api` and `sldb.api.notations`.
  - CLI: `sldb notations (list, sync, view, resolve)` with JSON output and envelope support (`sldb --envelope notations ...`).
  - HTTP serve routes in `sldb serve`: `GET /notations`, `GET /notations/view`, `POST /notations/resolve`, `GET /views/projection`, `GET|POST /views/projection/evaluate`, `POST /views/projection/save`.
  - Documentation updated in `docs/architecture/notations-and-views.md`.
  - Comprehensive test suite in `tests/notations/test_notation_view_and_routes.py`.
- Declaración y edición draft de containment, references, compositions, semantics y authority en modelos (SV04):
  - `sldb.api.create_model` y `ModelSource` aceptan `containment`, `references`, `compositions`, `semantics`, `authority`; validan que los campos referenciados existan y que las composiciones tengan marcador `⸢render•<name>⸥` en template (o lo generan en `default_template`), emitiendo las asignaciones correspondientes en el código Python generado.
  - `describe_model` y `ModelDescription` exponen `containment`, `references`, `compositions`, `semantics_map`, `authority`, `template`, `has_draft`, `draft_path`.
  - `sldb.api.edit_model_metadata` en `sldb.api.model_drafts` edita `__containment__`, `__references__`, `__compositions__`, `__semantics__` y `__authority__` en el `.draft.py` (`.py.temp`) mediante manipulación AST en `metadata_literals.py`, y sincroniza secciones de composiciones en el template.
  - `validate_template_contract` y `check_and_plan` validan coherencia de referencias/containment/compositions contra campos declarados y template, rechazando errores con `SLDBModelEditError`. `promote_model_draft(..., backfill=True)` re-renderiza documentos y reconstruye índices de modelo, semántico y de aristas.
  - Expuesto en CLI (`sldb models metadata edit`, `sldb models validate --promote --backfill`, y flags de creación) y HTTP serve (`POST /models/create`, `POST /models/metadata-edit`, `POST /models/promote` con `backfill`).
  - Documentación de arquitectura en `docs/architecture/model-authoring.md`.
- Visual vocabulary models, palettes and builtin notations absorbed from spec2viz (SV01):
  - 7 models in `sldb.models.notation_models` (re-exported in `sldb.models` and `sldb.api`):
    `SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, and `ViewDoc`.
    `ViewDoc` adds optional `params: dict` and `sections: list` for GD25 convergence.
  - Submodule `sldb.notations` containing palette (`palette.py`), notation (`notation.py`),
    and styling (`styling.py`) engines, along with builtin `palettes/default.yml` and the 8 builtin
    notations in `builtin/` (`uml-class`, `statechart`, `component`, `deployment`, `uml-sequence`,
    `activity`, `component-view-matrix`, `reflection`).
  - `resolve_model_ref` maps legacy `spec2viz.sldb_models:<Model>` references to
    `sldb.models.notation_models:<Model>` for transparent backwards compatibility with existing stores.
  - Architecture documentation in `docs/architecture/notations-and-views.md`.
- Each document node of the edge index carries its projected payload (GO04): `EdgeNodeRecord`
  gains `payload` (top-level fields holding a scalar or a list of scalars; dicts and lists of
  non-scalars are left out; a model's `__indexed__` picks exactly those names), `field_hashes`
  (the entry's whole map), `source_hash` (hash_c) and `contract_signature` (sha256 of the model's
  field names and `__references__` / `__containment__` / `__compositions__` names), persisted in
  the shard; other nodes leave them empty. `EDGE_INDEX_VERSION` 4 -> 5: a version-4 shard reads
  as stale and is rebuilt on the next write or `stores build`. `EdgeIndex.stale` now also names
  a document whose Markdown was edited outside sldb and one built under another contract
  signature of its model (a new `__references__` entry). `StructuredQuery` filters on
  `FacetFilter(facet="payload", ...)` from the shard, with no re-extraction; a filter on a field
  no model projects raises `SLDBGraphArgumentError` naming it. An `__indexed__` name that is not
  a field or not scalar is `SLDBModelError` when the model loads. Existing queries answer as
  before. Edge index of this repo after `sldb stores build` (`du -sb` of the edges shards root,
  MB = 10^6; shards = `.yaml` files there; 2026-11-06): before (main 804f1ad4) 47.64 MB in
  3116 shards; after (wt/go04 on c1e50419, which tracks more documents) 58.54 MB in 3277 shards.
  `docs/architecture/graph-backend.md` documents the projection and what it leaves out.
- A bare id in a reference field that allows a model also names a document of one of its submodels
  (`depends_on: task-x` with `TaskDoc` allowed names `TaskCodeDoc:task-x`), read from `base_models`
  of the model nodes in the composed index (an inherited model's node takes them from its class, since
  its local index keeps none). The allowed model itself wins; several submodels with that
  name stay `ambiguous`. `resolve_indexed_document` also reads the bases of an inherited model from
  its owner store.
- `sldb.api.resolve_indexed_document(store_path, model, name)` finds `Model:name` when the document is
  tracked under a submodel of `Model` (`TaskDoc:task-x` finds `TaskCodeDoc:task-x`): an instance of a
  submodel is an instance of its bases, read from `base_models` in the model indexes, without importing
  any class. An exact match on the model wins; two submodels tracking the same name raise
  `AmbiguousDocument`. Consumers such as graph_ui resolve ids through it instead of comparing model names.
- The whole-graph analyses sit behind a `GraphBackend` seam (`load`, `eval`, `analyze`).
  `NetworkXBackend` wraps `sldb.store.graph.analysis` unchanged, so the six `sldb graph`
  analyses and the ten `api/graph/analyze.py` functions print the same output as before and
  can be given another backend by Python for tests. A store selects it with
  `graph_backend` in `.sldb/store.yaml`: absent means `networkx`; any other value fails on
  load with `graph_backend <value> no admitido; admitidos: ["networkx"]`. `eval` implements
  the GO02 subset without paths (finding shape in `rules-language.md` §4 and §6); a path
  raises `NotImplementedError` until GO05. `docs/architecture/graph-backend.md` fixes the
  seam: a future engine (Kùzu, Neo4j, Datalevin) enters behind it and the rules never see it.
- A project's declared-edge graph as a library (`sldb.api.edges.project_graph`): `ProjectGraph(root,
  ProjectGraphConfig)` reads the documents of configured surfaces and the files path rules
  classify as nodes, the schema edges and unresolved values of the project's own store from its
  cached composed edge index (`include_linked=False`), and from each document's text what its
  model does not declare (configured mapping fields, fenced YAML blocks, mentions under headings
  or on every line). `edges_from(node)` / `missing_from(node)` read one source alone and give
  what `extraction()` gives for it, so a reader asking about a few documents reads only those.
  The project owns only the configuration (deskops' desk is the first, `deskops/graph/desk_graph.py`).
  New `sldb.api.tracked_documents(store, refs)`: `doc_status` for many references from one read
  of the documents index.
- The store splits in two sibling directories: `.sldb/` (`store.yaml` and `core/`) is
  versioned whole, so that git holds the tree's past, and `.sldb_cache/` (edges, sections,
  semantic shards, graphs, locks; `.sldb/runtime/` until now) is regenerable and ignored
  (`docs/architecture/derived-store-boundary.md`; owner's decision, 2026-10-29).
  `sldb stores init` adds the line `.sldb_cache/` to the root `.gitignore` (idempotent, no
  other line touched); `sldb stores check` reports the error `stores/core_ignored` (exit 1)
  when git ignores `.sldb/core/` or `.sldb/store.yaml` and the alert `stores/cache_not_ignored`
  (exit 0) when the cache is not ignored; `stores build --check` leaves `.sldb_cache/` out of
  its copy. New `sldb stores migrate-layout [--store PATH] [--force]` moves the content of
  `.sldb/runtime/` to `.sldb_cache/` (refusing a non-empty cache unless `--force`, which
  deletes it first), deletes the journal without archiving it, removes `.sldb/runtime/` and
  rewrites the root `.gitignore`: only the lines whose pattern is `.sldb/core` or
  `.sldb/runtime` go, `.sldb_cache/` comes in, everything else stays verbatim. The
  `selfdoc python-sync` graph defaults to `.sldb_cache/graphs/python-source.graph.json`.
- The write journal is retired (2026-11-04): no write through `sldb.api` produces one, and
  `sldb journal show` (and `verify`) print `El journal fue retirado el 2026-11-04; el pasado
  del store se consulta con sldb docs history <doc>.` and exit 0. `sldb.api.journal()` answers
  `[]` and `verify_journal()` a valid, empty report, for importers; `SLDB_JOURNAL_OFF` is gone;
  the `actor` parameters stay (they still stamp a document's provenance where they did).
  `docs/architecture/journal-authority.md` records the decision: the tree is the authority
  and git is its memory.
- Edges can carry their evidence, on request: `sldb edges show --evidence` and
  `sldb.api.edges.edge_evidence.stamp_evidence` add `metadata.evidence` with `ref_hash` (the
  target's `content_hash`, a model's `model_hash`; for a section its document's, flagged
  `ref: document`, since sections have no hash of their own), `contract` (the source model's
  `contract_hash`) and `engine` (`{name, version}`) or, for an authored edge, `actor`
  (`relation_doc:<name>`). No timestamp. Computed on read, so the shards do not change, and
  `ref_hash` is the target's current hash: telling an edge went stale takes a caller that kept
  an earlier evidence to compare.
- `sldb --envelope <command> ...` prints one JSON value per run, `{ok, command, store,
  revision, data, warnings}` or `{ok: false, error: {type: "ns/name", message}, exit}`, and
  exits with a typed code: 0 ok, 1 missing, 2 ambiguous, 3 rejected input, 4 busy, 5 store or
  runtime failure, 6 usage, 70 unexpected (`docs/cli-envelope.md`). Opt-in: without the flag
  the CLI prints and exits as before, because callers parse that output today.
- `sldb stores declare` and `sldb stores build`. A store's source is `.sldb/store.yaml`: the
  models it registers (local, or inherited from a linked store), its links, its predicates,
  the generators that write derived documents (such as `selfdoc python-sync`), the paths
  they write, and `include` rules saying which file is tracked under which model and name.
  The index and the model and document indexes are rebuilt from it by `stores build`
  (idempotent); `stores build --check` rebuilds a scratch copy of the sources and fails when
  that copy does not pass `stores check`, a tracked document is not declared, or it tracks
  something other than the local store. `stores declare --write` writes the declaration the
  current index implies, to adopt the layout. Tracking or untracking a document through the
  API keeps the declaration current (a file outside the project is not declared), `stores
  check` notes a declared store whose `.sldb/core/` is versioned rather than ignored, and a
  declared file that is gone is reported by `build` as `missing`. `declare --write` writes
  the declaration the index implies: a model whose source is outside the project
  (sldb's own, from the installed package) is declared by `model_ref` alone, and a glob is
  written only for a folder with more than one tracked file, all of one model. Design:
  `docs/architecture/derived-store-boundary.md`.
- An inherited model whose owner uses a `src/` layout imports again. The import root was the
  owner's project root, so pron's models, which live under its `src/` directory, stayed unimportable in a
  store that inherits them; it is now the directory the owner's registered path puts the
  package in (`sldb.store.model_import_root`). sldb's own store inherits AnchorDoc,
  ProjectionDoc and MoveDoc from pron through a relative link (`../pron/.sldb`) instead of
  registering copies pinned to an absolute path that no longer existed.
- **Python 3.12 or newer is required** (`requires-python >=3.12`; it was `>=3.10`). Python
  3.10 reaches end of life this month, and the whole suite (sldb, deskops, spec2viz, graph_ui)
  moves to the same floor. CI tests 3.12 and 3.13. The compatibility code for 3.10 is gone:
  the `tomllib`/`tomli` fallback in the `tools/check_*.py` gates and the conditional `tomli`
  dev dependency. `uv.lock` is regenerated for the new floor.
- The pre-redesign singular groups `sldb store`, `sldb model` and `sldb doc` run again: they
  were parsed (and listed by `sldb doc --help`) but had no handler, so `sldb doc untrack`
  answered `Unknown command: doc`. The plural groups (`stores`, `models`, `docs`) remain the
  documented spelling.
- A change to a model's contract now rebuilds the edges of its documents. Adding
  `__reference_models__` to a model and running `stores update` used to reuse every document's
  edges shard (its hashes had not moved), so the new references never reached the index and
  `edges rebuild` walked nothing until the shards were deleted by hand. Each shard now records
  the contract it was built under; the first rebuild after upgrading rewrites every shard once.
- A store link can be removed or pointed elsewhere: `sldb.api.unlink_store(store, name)` /
  `sldb stores remove <name>`, and `link_store(..., replace=True)` / `stores add --replace`.
  Removing a link a model here is inherited from is refused (replace it instead). A link to a
  directory that is gone was only fixable by editing `store_index.yaml`; `stores check` now
  notes it (`broken_links` in `check_store`).
- A scalar list item reads back as written. An item whose text markdown reads as block syntax
  was lost or mangled on extract: `validation: ["```bash", "pytest", "```"]` came back as
  `["pytest"]` (so any rewrite of the document deleted the fence lines), and `# x`, `> x`,
  `- x`, `1. x`, `***`, `<b>` or a leading space lost their syntax. Such an item is now rendered
  with one leading backslash (a CommonMark escape) and extracted without it; only a value that
  opens its item (`- ⸢rev,list•x⸥`) is escaped. A hand-written item that already began with
  `\` before such syntax now reads without that backslash.
- Extracting and validating no longer re-parse the model's template each time: a template's
  recipes are computed once per template, `validate` renders once instead of twice, and the
  sections index reuses one markdown-it parser. On sldb's own store, extracting 153 documents
  went from ~420 ms to ~275 ms and their sections from ~205 ms to ~175 ms.
- The markdown AST keeps what a token carries beyond its text, in `SLDBNode.metadata`: a
  fence's language (`info`), its opening markup (`markup`) and its attributes.
- `sldb edges show <name>` with something that is no node of the index fails, and suggests the
  document's export id (`Did you mean PillDoc:pill-008?`), instead of printing `[]` as for a
  real node without edges.
- `models show`, `models template show` and `docs update` take `--format text|json|yaml`
  (`models show` keeps YAML as its default; the template comes wrapped as
  `{model, draft, path, template}`; `docs update` reports `{updated, model, path}`). An
  argument a subcommand does not know is reported with that subcommand's usage, not the
  root's.
- A model's `__family__` changed in the class reaches the store: `stores update` and
  `models update` re-read it (it was written only at `models add`).
- `sldb.api.registered_models(store)` and `is_model_registered(store, model)` (by name,
  `module:Class` or `module.Class`), and `sldb models check <model>...`, which reports each as
  registered or missing and exits 1 if any is missing.
- `stores check` notes ignore rules that break the store's split (`.sldb/core` ignored, or
  `.sldb/runtime` not ignored); `check_store` returns it as `gitignore_policy`.
- A registered model that does not import here no longer takes the store's AST down: it is
  listed with `resolved: false` and the error (a healthy model's entry is unchanged), so `models show` and `ast show` of the rest
  answer (in an environment without `pron`, `models show TaskDoc` failed).
- `models template show` (and every draft operation) finds a model's source by importing its
  `model_ref` when the recorded path is not a file here: a store copied without its models,
  an absolute path from another machine, or an inherited model, whose path is empty and
  failed with `Is a directory`. When neither works, the error names the model and the store.
- A template's literal paragraph (deskops' `_Describe the incoming message..._`) anchors only a
  paragraph with that text. A document written without the placeholder had its first real
  paragraph taken for it and dropped on extract, so any rewrite deleted it (the first
  paragraph of inbox notes; `why`, `goal` and `done_when` of a task). Documents that lacked
  the placeholder now extract more: `stores check` reports them as `data_mutation` until
  `sldb models update <Model>` re-extracts the model (`stores update` trusts a document whose
  text did not move). Headings still anchor by position.
- A document that ends before its template does keeps its last section: a field of a section
  the document does not have (`## When`, after a document that stops at `## Why`) no longer
  claims the last section's paragraph, which came out empty and was erased by any rewrite.
  Past a missing heading, only later headings end a section. The `purpose` of three of
  sldb's rituals came back (`models update RitualDoc`).
- `stores check` names the documents a rewrite would lose content from: blocks of the file
  that do not survive `render(extract(text))`, because the model does not read them (written
  by hand, or by an older template). Their hashes are consistent over the poor extraction, so
  nothing else showed it. Sections the template fills only with `render`/`py` markers are
  regenerated and not counted. `check_store` returns it as `rewrite_loss`.
- `stores check --quiet` prints the PASS/FAIL line alone, as documented: it printed the
  per-document notes too, and now also skips the scans behind them.
- A `data_mutation` over text that did not move (and an unchanged contract) is explained as
  what it is, sldb reading the same file differently after an upgrade, and points to
  `sldb models update <Model>`: `stores check` said `stores update` would accept it, but
  `stores update` trusts unchanged text and did nothing. It no longer asks for a decision.
- `stores check` says, for a document whose text disagrees with its index, where the indexed
  text sits in the file's git history: `stale` (an earlier committed version, with the commit:
  the index fell behind), `unmatched` (no committed version has it: an edit indexed and never
  committed, or damage), `orphan` (the file is gone) or `undetermined` (not a git work tree),
  with the `git log` command that shows it. The JSON report carries it as `history`.
- `sldb.store` imports the rest of sldb through three seams only: `store/exceptions.py`
  (errors), `store/runtime_codec.py` (extraction) and `store/model_contract.py` (what a model
  class declares, and the built-in relation types); it imports nothing from `sldb.api`, `cli`
  or `selfdoc`, and `tests/test_store_seams.py` keeps it so. `describe_field` and the field
  kinds moved to `sldb.models.field_schema` (still importable from `sldb.api.schema`), which
  closes the store → api edge R4 in `contracts/layers.toml`.
- `selfdoc python-check` and `python-sync` work again: a property with a setter (or an
  `@overload`) was two symbols with one document id, and both commands failed with "Python
  symbols collide". A name redefined in its scope is now one symbol.
- kgdb is part of sldb, and nothing invokes an external `kgdb` any more. `selfdoc python-sync`
  writes the source graph with sldb's own graph IO instead of running `kgdb ingest` (it failed
  once the separate package was gone). `--kgdb-command` and `--kgdb-output` were removed and
  are refused with a clear error; the graph goes to `--graph-output`, by default
  `.sldb/runtime/graphs/python-source.graph.json` (it was `.kgdb/python-source.graph.json`).
  `sldb.selfdoc.kgdb_sync` is now `sldb.selfdoc.source_graph_file` (`write_source_graph`), and
  the selfdoc report's `kgdb_stale` is `graph_stale`. The data contract
  `sldb_kgdb_semantic_export` keeps its name (see the entry on kgdb names below).
- Docstring metadata is parsed strictly (`sldb.selfdoc.docstring_metadata`, spec section 2):
  only an opening line exactly `---` starts it, a closing `---` is required, and the block is a
  YAML mapping with unique keys among `id` (required), `kind` and `tags` (`namespace:value`,
  deduplicated). Malformed metadata and an id declared twice are reported as `path:line:
  problem` in the selfdoc report's `metadata_errors`, and `selfdoc python-sync` writes nothing
  while any remain; they were silently ignored and the declaration lost its identity.
- The source graph gives every module and symbol node its `local_tags` and `effective_tags`,
  inherited along the lexical chain package -> module -> class/function -> nested declaration
  within the scan (spec section 3): `system:*` and `workspace:*` from the nearest declaration,
  `topic:*` as a union, any other tag local only; nothing through imports, base classes or
  siblings. Each effective tag names the declaration and `path:line` it comes from. Two
  `system:` (or `workspace:`) tags on one declaration are a metadata error.
- An import in the source graph follows explicit re-export chains to the definition
  (`from sldb.api import open_store` reaches `sldb.api.stores.open_store:open_store`), through
  module-level imports only, with the chain in the edge's `via`; `from pkg import submodule`
  reaches the submodule. A star import, a cycle or a module outside the scan stays
  unresolved. A relative import inside a package's `__init__.py` resolves against that
  package (it was resolved against the parent: `pkg.impl` for `pkg.inner.impl`).
- `stores check` reuses its per-document content scans (rewrite loss and structural noise)
  while a document's text, its model's contract and the sldb that reads it have not moved, in
  the user's cache directory; the rewrite-loss scan also reuses the extraction the check
  already has instead of extracting again. On sldb's store (2775 documents) a full check went
  from 43 s to 23 s cold and 7 s warm, with the same findings.
- The source graph keeps the condition an import lives under (`context`: `type_checking`,
  `conditional`, `try`), and marks an import a later same-scope binding shadows
  (`shadowed_at`); a reference after the shadowing no longer resolves to the import.
- `selfdoc python-check` reports, apart from errors and drift, the declarations without
  metadata (`undeclared`), the declared ones without an explanation (`unexplained`) and the
  annotation references nothing resolves (`unresolved_references`, which were dropped).
- A symbol document's `purpose` is generated from the first paragraph of its docstring when it
  is a placeholder or was generated before; an authored purpose is kept and listed in
  `purpose_conflicts` for a decision.
- `selfdoc python-sync` reports on what is on disk after writing: it reported the plans made
  before writing, so a sync that wrote everything returned 1.
- Deleting `.sldb/runtime/` and rebuilding brings the sections and semantic indexes back. The
  user cache (`~/.cache/sldb/runtime-cache-built/`) and the in-process dirty set vouched for
  shards that were gone, so a rebuild wrote only the edges and a graph snapshot lost
  `has_section` and `semantic_parent` (reported by graph-ui).
- The last kgdb names in sldb's public surface are sldb's now (kgdb merged into sldb):
  - `sldb.store.export.export_kgdb_semantic_payload` is `export_semantic_payload`;
  - the semantic export contract keeps its name, `sldb_kgdb_semantic_export` version 1, and so
    do its schema and fixture (`contracts/schemas/sldb_kgdb_semantic_export.schema.json`,
    `contracts/fixtures/sldb_kgdb_semantic_export.v1.json`). It is a frozen data identifier,
    like the `sldb://...` node ids: renaming a data contract breaks every reader of files
    already written, so a format change goes behind a new contract version, never a rename.
    Main wrote `sldb_semantic_export` for a while before release; an export under that name is
    still read, never written. `tests/store/test_export_contract_frozen.py` pins the contract,
    the ids and the keys of the store index and of the document entries. The reading function is `sldb_semantic_export_to_snapshot`;
  - `stores semantic-export --format kgdb` is `--format sldb`;
  - the `sldb serve` route `/kgdb/snapshot` is `/semantic-export`;
  - the store's tracked relation types moved from `kgdb/relation_types/` to
    `sldb/relation_types/`, where `edges init` already wrote the new ones.
- `stores init` fails cleanly: what a failed init wrote is removed, the message says where it
  failed and what to check (instead of `Unexpected: [Errno 13] ...`), and the exit code tells
  a caller what happened: 0 created or already there, 2 the place refused it (permissions),
  1 failed half-way. `init_store` raises `StoreInitError` (an `SLDBStoreError`).

## 0.1.12 - 2026-10-18 — declared references resolve bare ids and paths, and report what names nothing

- Declared references resolve bare ids and paths. A value of a `__references__` or
  `__containment__` field names its document as an export id, as the path a tracked document
  lives at, or as a bare id tried against the models the field allows — the new
  `__reference_models__ = {"field": ["Model", ...]}`, or the containment list; one match
  resolves, several are `ambiguous`. It is decided when the index is composed, so tracking the
  target later resolves it. What names nothing is reported, never an edge:
  `sldb.api.unresolved_references(store)` / `sldb edges unresolved` /
  `EdgeIndex.unresolved_references` (`UnresolvedReference`: source, model, field, target,
  target_export_id, relation, reason, source_path). A free reference field only reports export
  ids. `EDGE_INDEX_VERSION` is 4: shards rebuild. `__reference_models__` enters the contract
  hash only for a model that declares it.
- An edge sldb derives (structural, schema, alias) is checked against sldb's own definition of
  its builtin type, even where the store authored a type under that name (selfdoc's code
  `contains` / `references`).
- `edges check` of a store that links others fails only on its own edges: what only a linked
  store's edges commit (an owner's stale shards, its cardinality violations) is reported apart
  (`EdgeCheckReport.linked_errors`, `linked_stale`; a `note:` line in the CLI). Edges read
  from a linked store carry `metadata["from_store"]`.
- Inheriting a model into a store (`models inherit`, or `alias:Model` on first use) signs its
  empty roster, so `stores check` passes without a `stores update` first.
- A section no longer counts as the owner of a path: a bare composition or reference value
  equal to a heading path resolved to that section instead of a document.

## 0.1.11 - 2026-10-18 — models are defined once and inherited; a free `attributes` on relations

- `RelationDoc.attributes`: a free dict of the edge's own attributes (a multiplicity, a role, a
  transition's action), written in the frontmatter and copied to the index edge as
  `metadata["attributes"]`. A RelationDoc written before has none. Its contract moved: run
  `sldb stores update` in a store that tracks RelationDoc documents.
- `sldb.api.StructuredNLDoc`: the base class of models, from the public surface.
- `sldb.api.graph.query_snapshot(snapshot, query)`: a StructuredQuery over a GraphSnapshot held
  in memory, no store needed. `sldb.api.graph` also exports `Edge` and `SystemIdentity`.
- `models inherit` and the `stores check` note tell a copy by its class, not by the reference
  string: `deskops.models.atom:AtomDoc` is a copy of `deskops.models:AtomDoc` when the package
  re-exports it. A converted copy takes the owner's `model_ref`.
- `edges check` over linked stores: one edge that two stores both emit (a shared model's
  `has_field`) counts once for cardinality; `has_model` is many-to-many, since stores share a
  model they inherit; `links_to` is a builtin relation type. `sldb edges init` now also
  rewrites a tracked builtin relation type whose spec moved (`updated` in its report), and no
  longer writes a builtin over an authored relation type of the same name.
- Models are defined once, in the store that owns them, and inherited by the others.
  `sldb models inherit alias:Model` / `sldb.api.inherit_model` registers an inherited entry
  (`origin: <alias>`, no source path) or converts a local copy in place, keeping its documents,
  roster and signed contract. Using `alias:Model` as a model name now inherits instead of
  copying. An inherited model imports from the owner's project root, so no `--pythonpath` is
  needed and a moved owner is one link to update; with the owner unreachable the store keeps
  working on its own signature. `stores check` notes a local model under a name a linked store
  owns (a convertible copy, or an override to rename). The graph gains `links_to` between
  stores and `origin_store` on `has_model`. A store with no inherited models writes no
  `origin` key, so existing indexes do not change.
- `stores update` re-signs the roster of a model whose class does not import. It used to skip
  the model whole, so a stale roster (a merge that brought its shards in, say) stayed
  `roster stale` in `stores check`. Its documents are still not rehashed, it is still reported
  as skipped, and it keeps the contract it signed.
- `stores check` no longer reports a moved contract for a model with `extra="allow"` (deskops'
  TaskDoc) whose documents carry undeclared frontmatter keys. Such a key is still produced by
  the current class, so it is not a field the model dropped; the check only counts a key the
  current extraction of the same document no longer yields. `stores update` could never clear
  the old finding.
- A template whose frontmatter is one `dict` placeholder (`⸢rev,dict•frontmatter⸥`) declares
  every key: `docs track` and `docs create` no longer refuse a document's extra keys, which that
  dict carries back on re-render.
- `producer.version` in a semantic export is the real package version: read from the source
  checkout's `pyproject.toml`, else from the installed `structuredLanguageDB` metadata. It
  asked for a distribution named `sldb`, which never exists, and always fell back to `0.1.0`.
- `click` is an optional extra (`pip install structuredLanguageDB[click]`), imported only when
  `ClickScanner` is used; it was imported unconditionally without being declared.
- `sldb.examples.pandoc_cv` ships in the wheel, with its Markdown files.
- `tools/check_identity.py` reads `git ls-files -z`: a quoted non-ASCII path no longer shows
  up as a top-level entry named `"docs`.

## 0.1.10 - 2026-10-17 — references to a relation type reach it; a document by absolute path

- A `__references__` field that points at `RelationTypeDoc:<doc>` now lands on the
  `sldb://relation_type/<name>` node. The index stores relation types under that node, so the
  schema edge used to point at a document node that does not exist and was dropped silently
  while `doc_exists` said yes. `resolve_edges` moves that end to the relation-type node.
- `find_doc` (behind untrack and delete) accepts a document's absolute path as well as the path
  relative to the project root.
- Design notes for the surface in `docs/surface/`, with tests for the MachineDoc editor and an
  optimistic-lock client. The editor test compiles on Python 3.10/3.11 (no nested PEP 701
  f-string).

## 0.1.9 - 2026-10-16 — a dropped field is a contract move, and `stores update` fixes it

- A document whose `field_hashes` name a field its model no longer declares was signed under
  another contract. Any write of another document of the model re-stamps the model's contract,
  so the model looked unmoved: `stores check` blamed the untouched document (`data_mutation`,
  "confirm the change was intended") and `stores update` trusted its unchanged text and never
  re-extracted it, so the check stayed red. Now the model reads as `contract moved` (safe to
  run: `stores update`) and `stores update` re-extracts those documents.

## 0.1.8 - 2026-10-16 — a deleted model class no longer locks the store

- Derived-index rebuilds skip a model whose class does not import instead of raising; the
  semantic rebuild names it in `models_unresolved`, as the edge rebuild already did, and its
  documents keep their last tags. `untrack_document` (and every write that rebuilds) works
  while another registered model's class is gone.
- `sldb models remove <name> --with-documents` / `remove_model(..., untrack_documents=True)`:
  drops a model and its tracked documents without importing the class; the Markdown files stay.
- A write that raises halfway leaves no trace: `untrack_document` puts the document's shard,
  the models index and the store index back as they were; `remove_model` changes the registry
  first and deletes the model's files only once every rebuild succeeded.

## 0.1.7 - 2026-10-16 — `models remove`

- `sldb models remove <name>` / `sldb.api.remove_model(store, name)`: unregisters a model that
  tracks no documents, with its indexes and shards; the class is never imported, so a model
  whose code was deleted can go. A model that still tracks documents is refused (untrack them
  first). `stores check` already passes with such a model registered (0.1.5); its note now
  names the unimportable models with no documents as removable.

## 0.1.6 - 2026-10-16 — the graph as a state machine

- `--where` joins predicates with ` and ` (outside literals; no `or`, no parentheses), and
  `nonempty(f)` is `has(f)` that also rejects `[]` and `{}` (`has` keeps its meaning).
- `sldb.api.where_matches(expression, payload, subject=None)`: a `--where` predicate on a plain
  payload, tracked or not; `{field}` fills from `subject` (default: the payload). An unparseable
  part raises `WherePredicateError`, now exported from `sldb.api`.
- `sldb.api.edges_holding(store, node, subject, relation=None)`: the edges leaving a node whose
  condition (the edge's, else its type's) holds on the subject; `sldb edges show <node>
  --holds-for <doc>` is the same from the CLI. A self-loop is a valid edge (a terminal
  transition).

## 0.1.5 - 2026-10-16 — an unimportable model is named, not blamed on its documents

- `stores check`: when a model's class cannot be imported (a clean clone without the model's
  package, a consumer's CI with another `sldb` first on PATH), its fields cannot be
  re-extracted. Every document used to read as a `data_mutation` ("decide first", restore the
  file). Intact text now stands for intact fields, and the report names the unresolved models;
  changed text still fails. JSON: `models[].resolved`.
- CI: the structural gates pass (`legacy_contract` mapped to the `migracion` axis, unit coupling
  updated; the surface gate no longer compares the five-consumer total with a partial view),
  and `selfdoc check` passes (knowledge/ synced with the CLI, the store committed with it).

## 0.1.4 - 2026-10-16 — `fields update` leaves the store passing

- A field write (`fields update|append`, `sldb.api.save_document_payload`) rewrote the Markdown
  and the model's roster but not the document's record, so `stores check` failed with a
  `data_mutation` on the write sldb had just made. The shard cache handed out its own instance:
  the caller edited it in place and the save, comparing against the cache, saw no change and
  skipped the write. Loads now return a copy (`sldb.store.io.shards`), which also covers the
  semantic, sections and edges shards.

## 0.1.3 - 2026-10-16 — upgrading sldb no longer fails unchanged stores

Found on Governance's `pulse`, which installs sldb from git: both checks failed on a store whose
content had not changed.

- `stores check`: a model whose stored contract hash equals the formula sldb used before
  cecd97b (fields and template only) passes, with a note naming those models, instead of
  "contract moved" on every model. A class that really changed still fails. `stores update`
  re-seals the hash under the current formula. JSON: `models[].legacy_contract`.
- `edges check`: in a store that ran `edges init`, an edge sldb derives itself whose builtin
  type was added later (`composes`) is checked against the definition sldb ships and reported in
  `untracked_builtins`, not as an error. A store that never ran `edges init` still fails;
  authored edges still need a tracked type.

## 0.1.2 - 2026-10-16 — referencing documents of linked stores

- `stores add` links were recorded but no document lookup read them: `docs show
  alias:doc` answered `Unknown document target`. `docs show` (and `sections show|fields`,
  serve's document routes) now take `alias:ref` — name, `Model/name` or tracked path — and
  read only the store linked directly as `alias`. A bare ref still reads only the local store;
  a prefix that names no link leaves the ref whole, so existing refs resolve as before.
- Add `docs exists <[alias:]ref>` and `sldb.api.doc_status|doc_exists`: whether a reference
  resolves, from the indexes alone (no model import, nothing written). Exit 0 ok, 1 missing,
  2 ambiguous, 5 `link-missing` / `link-broken`, so a missing document is told apart from a
  sibling repo that is not there.
- `stores list` (and `sldb.api.store_links`) report each link's state: `ok`, `missing` or
  `not-a-store`; a broken link is reported, never raised.
- `stores add` records the link relative to the project root (it was absolute outside it), and
  refuses linking a store to itself, aliases outside `[A-Za-z0-9][A-Za-z0-9._-]*` and the
  reserved `local`. Links already written are read as before.
- `stores init` seals the root hash over the empty model layer: a new store, or one that
  only links others, passes `stores check` without a `stores update`.
- `docs show` of a linked doc reads its file from the linked project (`absolute_path` was
  built from the local root).

## 2026-10-01 — SLDB is the substrate again

- The README no longer calls this generation frozen: the v2 seed (`knowledge`) was frozen in
  turn and its evaluator moved to `pron`, so nothing supersedes this package. SLDB is the
  store every surface (`surface/`, `tools/graph_ui`, `tools/sldb-ui`) is a view over. <!-- gone -->
- New README section "Serving and surfaces": `sldb serve` routes grouped by what a UI needs,
  and where the surfaces and their design docs live.

## 2026-09-07 — v1 frozen

- The README marks this generation frozen, with `knowledge` as its successor. Earlier modularization and v0.6 removal plans are historical and do not promise further v1 releases.

## Working tree — `docs delete`

- Add `docs delete` (and `sldb.api.delete_document`): untrack a document **and** remove
  its Markdown file. `docs untrack` was the only way to drop a document, and it keeps
  the file on purpose — so "delete this document" meant untrack, then `rm` by hand, then
  remember that `runtime/cache/extracted.json` still describes the deleted path until
  some later full load rewrites it. `delete` does the three.
- Confirms before removing the file unless `--yes` is given; a non-interactive stdin
  answers no.
- Add `runtime_cache_disk.forget(store, predicate)` so cache entries can be dropped
  without a full store load.

## Working tree — self-documentation follow-up

- Add `selfdoc scan|sync|check` to derive CLI facts from argparse, preserve authored explanations, and synchronize tracked command/surface documents from the selected store root.
- Report obsolete documents without deleting them; check freshness without writing documents or indexes.
- Expose public parser help for the supported `init` and `example` commands.
- Split knowledge document definitions into one class per file, keeping public import references and resolving re-exported definitions for template editing.
- Separate follow-up work into self-documentation, store context/federation, and AST ownership/section contracts. No package version bump or publication is included.

## Historical pending changes

- Add reversible `rev,table[...]` template markers for rendering and extracting Markdown tables backed by `list[dict]` fields.
- Add generic cross-store document writes through linked store aliases and federated model namespaces for workflow tools such as `deskops`.

## 0.2.0 - 2026-05-16

- **Store write concurrency**: atomic writes + advisory `fcntl` locks on all index write paths; `--wait` flag for `stores update`
- **Rebuild auditability**: `RebuildReport` dataclass tracks missing docs, empty sections, and unparseable headings in both semantic and section rebuilds; `--verbose` flag for details
- **CLI deprecation surface**: old singular commands (`store`, `model`, `doc`, `ls`, `get`, etc.) emit deprecation warnings; v0.6 was the historical removal target (see freeze note above).
- **Read-side hot path**: `sections show` and `sections fields` prefer persisted index over full IR rebuild; `--rebuild` flag available on `find`/`sections find`
- **Marker ownership robustness**: field name from the canonical `parse_marker()` is validated against known payload paths; unknown markers log a warning

## 0.1.2 - 2026-04-24

- Reorganize the package into `core`, `models`, `runtime`, `cli`, `assets`, and `examples` subpackages while keeping compatibility re-exports
- Add explicit link recovery and transclusion composition with `recover` and `compose`
- Add structural store queries under `st` with `ls`, `get`, `glob`, and `find --where`
- Add store-local semantic indexing under `se` and explicit federated semantic navigation under `gse`
- Add model semantic metadata, canonical model registration, semantic equivalence mapping, and bundled tests for the new workflows

## 0.1.1 - 2026-04-24

- Add current-system architecture docs and diagrams under `docs/architecture/`
- Add feature proposal docs under `desk/` for future SLDB features: link/recover/compose, store tree indexing, semantic DAG indexing, canonical/global-local semantics
- Add desk workspace with task board, self-docs, and operating procedures

## 0.1.0 - 2026-04-21

- Rename the package and CLI from `nldb` to `sldb`
- Add safe-by-default Python marker execution with configurable unsafe mode
- Ship the SLDB example bundle and CLI workflows for extract, render, validate, init, and example
- Add release basics: MIT license, package metadata, and CI
