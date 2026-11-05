# Alcance y estado de partida

## Estado de partida de sldb (verificado 2026-11-04, `src/sldb`)

- **Nodos sin contenido.** Un nodo de documento guarda `export_id`, nombre, modelo, ruta, tags, `hash_c`, `hash_d` (`store/edge_index/doc_structure.py:23-25`). La entrada del documento guarda `source_hash`, `content_hash`, `field_hashes`, tags y procedencia, no el payload (`store/models/document_entry.py:11-18`).
- **`--where` re-extrae.** Carga cada documento del modelo, extrae el payload del Markdown y filtra en Python (`store/query_engine/structural_queries.py:69-80`). Caché en memoria y en el directorio de caché del usuario, fuera del store (`store/runtime_cache.py`, `runtime_cache_disk.py`).
- **Dos lenguajes de condición.** `where_parse.py` (`has`, `nonempty`, `in`, `~`, `model <=`, comparaciones, solo ` and `) y `FieldCondition` de `StructuredQuery` (`eq ne gt lt contains starts_with is_null is_not_null`). Ninguno cruza relaciones; ninguno tiene `or`, `not` ni paréntesis. `propuesta/07-LO-QUE-FALTA.md:190-202` ya lo nombra.
- **Condiciones por arista.** `RelationTypeDoc.condition` y `RelationDoc.condition`; `edges_holding(store, node, subject)` devuelve las aristas cuya condición se cumple sobre un solo payload (`api/edges/edges_holding.py:13-31`). `edges check` no valida que las condiciones parseen.
- **Herencia de modelos ya existe.** Un modelo declara `base_models`; `RelationTypeDoc.source_types` y `target_types` se verifican con esa herencia y el predicado `model <= Base` la consulta (`models/relation_type_doc.py:83-146`, `where_parse.py`). Las reglas por familia de modelo se apoyan en esto, no en un mecanismo nuevo.
- **Sin reglas.** No hay Datalog, reglas, vistas ni hechos derivados en `src/`. `Constraint` existe solo en `docs/opsys/bridge_primitives/README.md:111-130`.
- **Anclas solo de código.** `CodeAnchorDoc` con huellas por símbolo y estados `intact / changed / reconnected / lost` (`docs/architecture/code-anchoring.md:68-96`). `Provenance.from_` acepta `doc:<Model:name>` pero el `verify` diseñado no existe. `edges show --evidence` calcula `ref_hash` al leer y no lo guarda.
- **Índice de aristas.** Shards YAML por documento, reconstrucción incremental por dirty set en cada escritura (`store/edge_rebuild.py:27-39`), composición completa en memoria memoizada (`store/edge_index/compose.py:22-55`). Medido en este repo: 73 MB en 2.874 shards.
- **Análisis de grafo ya sobre networkx**: `graph path | cycles | order | components | central | similar`.
- **Deuda que afecta este plan**: `EdgeIndex.stale` no marca una edición externa del Markdown ni un campo nuevo de `__references__` (inbox 20261102-065705); el scope `descendant_of` del executor ignora el tipo de relación.
- **Decisiones del dueño ya en el Board de sldb**, no implementadas: journal congelado (git es la autoridad) y split `.sldb` versionado / `.sldb_cache` ignorado. Este plan las toma como prerrequisito operativo (gate `G_OPS_PREREQ`).

## Estado de partida del consumidor (deskops, para contexto; no se ejecuta aquí)

- Ciclo de vida: estados = RitualDoc, transiciones = RelationDoc con condición evaluada por sldb; pero el efecto (`sets_status`, `terminal`) sale del YAML y el grafo se escribe una sola vez. `advance` no usa `edges_holding`.
- Gates = hechos calculados en Python y escritos en el payload antes de evaluar (`closeout_evidence_verified`).
- `task_type` es un string plano usado solo al crear; `inherits_from` reimplementado; `depends_on` sin efecto; composición solo en scripts del drawer.
- Dos vías para saltar gates (`advance --to`, `edit task status`), contra D2.

## Qué produce este plan y qué consume deskops

El plan produce capacidades genéricas en sldb (lenguaje, proyección, `RuleDoc`, anclas `doc:`, evaluación, transiciones como datos, costura de backend). deskops las consume en su propio plan, en su propio desk (D3): tipos de tarea como documentos con jerarquía, recibos `ReviewDoc`, gate de activación como `RuleDoc`, cierre de `advance --to` y `edit task status`. Ese plan no existe todavía; la primera prueba de consumo es el gate `G_CONSUMER`, producida por deskops.

## Reglas comunes de ejecución

1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de sldb, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review). Una revisión en frío está aceptada cuando quien opera el desk de sldb (D3: no hay coordinación central) escribe su disposición en `reviews/rN.md` y no queda ninguna ambigüedad abierta según la guía; los hallazgos que la guía excluye se disponen como delegados al TaskDoc, con cita de la guía.
2. La validación corre con pytest en el host que el dueño indique; en esta serie fue robocop2. Un nodo no cierra con tests rojos ni con tests saltados.
3. Toda capacidad nueva entra con: modelo o documento spec, comando CLI con envelope JSON, pruebas, entrada en CHANGELOG y doc en `docs/architecture/`. Nada queda "solo en el código".
4. Compatibilidad: `--where` actual sigue funcionando durante la transición; se marca deprecado y se retira en un nodo explícito, no de paso.
5. Nada se persiste del resultado de una regla. Los hechos derivados se recalculan; si un consumidor quiere persistir, escribe un documento propio.
6. Ante un contrato ausente de una dependencia no ejecutada, el nodo registra la hipótesis en su TaskDoc y no inventa API.
7. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.
8. Toda medición que un nodo exige (tamaño del índice, tiempo de escritura) se registra en la sección Validation del TaskDoc del nodo con unidad, método y fecha; si cambia un número de usuario, también en CHANGELOG.
