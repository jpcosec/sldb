FILE:desk/drawer/plans/grafo-operable/context-review-guide.md
# Guía para revisar un nodo de este plan

Va en todo input de revisión en frío. Deriva de brief.md, alcance.md y decisiones.md; no agrega requisitos.

## Qué evalúas

Si este nodo, tal como está escrito, se entiende como **encargo de planificación**: propósito, resultado, repo dueño, límites, dependencias y aceptación comprobable. No evalúas si el diseño es bueno ni ejecutas nada.

## Cómo leer

- `dag.yaml` es la fuente de ids, aristas y gates. Ningún nodo tiene ejecución autorizada.
- ROOT y PK son agrupaciones; un nodo `aggregate` no se ejecuta: termina cuando terminan sus hijos.
- Una flecha `depends_on` significa prerrequisito → dependiente. Hermanos sin arista no se entregan nada entre sí.
- Un gate `pending` es intencional, no un defecto.
- Las decisiones D1–D4 y D8 están tomadas. D5, D6 y D7 son recomendaciones pendientes de confirmación explícita: un nodo que las asume debe decirlo; no es ambigüedad del nodo, es un gate.
- Los bloques `edge` son contratos de vecinos; no los revises.

## Qué cuenta como ambigüedad

Solo lo que obligaría al ejecutor de ESTE nodo a inventar: resultado indefinido, aceptación no comprobable, repo o actor ausente, dependencia que falta o sobra, contradicción con otra fuente suministrada, o un límite que permita exceder el alcance.

No cuentan: nombres exactos de archivos, funciones o tests que el TaskDoc fijará al promover; contratos que produce una dependencia nombrada; trabajo de nodos dependientes; lo excluido en brief.md §Fuera de alcance.

Cita la frase del input que origina cada ambigüedad.

FILE:desk/drawer/plans/grafo-operable/brief.md
# Brief: grafo operable de sldb

Fecha: 2026-11-04. Repo dueño: sldb. Estado: plan en drawer, ninguna tarea activa, `execution_authorized: false`.

## Encargo

Que sldb evalúe por sí mismo reglas declaradas sobre documentos, aristas y hashes, de modo que un consumidor como deskops pueda escribir sus gates de workflow (activar una tarea, cerrar dependencias, reglas por tipo de tarea, recibos de revisión atados a un hash) como documentos, y sldb los evalúe con explicación, sin que el consumidor reimplemente la lógica en Python.

## Por qué ahora

- deskops tiene hoy gates calculados en Python que se escriben como hechos dentro del payload antes de evaluar (`closeout_evidence_verified`), un ciclo de vida con dos fuentes de verdad (grafo y YAML) y una herencia reimplementada aunque las aristas `inherits_from` ya existen. Ver `alcance.md` §Estado de partida.
- El dueño decidió el 2026-11-04 gates de activación bloqueantes sin bandera de salto; la vía de escape es especializar tipos de tarea. Eso exige reglas por tipo evaluadas de forma uniforme.
- kimun (sucesor) decidió evidencia con hash en cada arista, estados derivados y Datalog, pero no tiene nada de eso en código y su capa G está bloqueada por decisiones pendientes del dueño. sldb v1 tiene que cargar esto ahora, en una forma que kimun pueda absorber después.

## Resultado esperado del plan completo

1. Un lenguaje de predicados único en sldb, con `and/or/not`, paréntesis, caminos sobre relaciones y cuantificadores, con semántica de Datalog estratificado y explicación de fallo.
2. Los campos de los documentos proyectados en el grafo, para evaluar sin volver a extraer Markdown.
3. `RuleDoc`: regla como documento, con sujeto por familia de modelo, condición, severidad y momento de evaluación.
4. Anclas a documentos con hash de contrato pinneado (subconjunto declarado de campos) y estados `intact / changed / lost`.
5. Evaluación incremental en escritura, transición y `stores check`, con hechos derivados a punto fijo.
6. Transiciones como datos en las aristas; la máquina de estados es genérica.
7. Una costura `GraphBackend` detrás de la cual vive networkx hoy y podría vivir otro motor después.

## El límite (lo que este plan no promete)

El store juzga consistencia entre hechos declarados; no es oráculo de verdad. En concreto:

- **No autentica actores.** Un recibo dice quién lo escribió; probarlo es tarea de git (autor, firma, rama) y de la capa de ejecución (Scion: identidad de agente, delegación). sldb no construye auth.
- **No produce hechos externos.** Que un commit esté en HEAD, que un archivo exista o que los tests pasen entra como recibo o como ancla (git y archivos son content-addressed; un evento como "tests verdes" solo puede ser un recibo de quien corrió).
- **Mundo cerrado solo dentro de un store, a un commit.** Entre desks enlazados por git la consistencia es eventual; una regla sobre otro desk vale lo que vale el checkout.
- **No juzga.** Si una descomposición es buena o una pill alcanza lo dicen revisores, testers y humanos, que producen recibos. Los engines son externos.

## Vocabulario

- **Regla**: documento `RuleDoc` con sujeto (familia de modelo y filtro), condición en el lenguaje de predicados, severidad (`error` o `alert`) y momento (`on_write`, `on_transition`, `on_check`).
- **Hecho derivado**: valor calculado por el evaluador a partir de documentos y aristas; nunca se persiste, se recalcula (punto fijo, incremental).
- **Recibo**: documento escrito por un actor o engine que afirma un hecho externo (revisión, corrida, veredicto) y lo ata al hash de contrato de su sujeto.
- **Hash de contrato**: hash sobre el subconjunto de campos de un documento que el modelo declara como contrato; sldb ya guarda `field_hashes` por campo. Cambiar un campo fuera del contrato no invalida recibos.
- **Ancla a documento (`doc:`)**: referencia a `Model:name` que guarda el hash de contrato visto; su estado es derivado: `intact`, `changed`, `lost`.
- **Backend**: implementación del protocolo `GraphBackend` (`load`, `eval`); networkx es la primera.
- **Mundo cerrado**: dentro de un store, "no existe X" es un hecho; a través de links es solo "no se ve X".

## Fuera de alcance

Autenticación; motor externo (Neo4j, Kùzu) en esta fase; migrar a kimun; tocar deskops (deskops consume el resultado en su propio plan, ver `alcance.md` §Consumidor); el journal y el split `.sldb`/`.sldb_cache` (tareas activas del Board de sldb, prerrequisito operativo pero no parte de este plan).

FILE:desk/drawer/plans/grafo-operable/alcance.md
# Alcance y estado de partida

## Estado de partida de sldb (verificado 2026-11-04, `src/sldb`)

- **Nodos sin contenido.** Un nodo de documento guarda `export_id`, nombre, modelo, ruta, tags, `hash_c`, `hash_d` (`store/edge_index/doc_structure.py:23-25`). La entrada del documento guarda `source_hash`, `content_hash`, `field_hashes`, tags y procedencia, no el payload (`store/models/document_entry.py:11-18`).
- **`--where` re-extrae.** Carga cada documento del modelo, extrae el payload del Markdown y filtra en Python (`store/query_engine/structural_queries.py:69-80`). Caché en memoria y en el directorio de caché del usuario, fuera del store (`store/runtime_cache.py`, `runtime_cache_disk.py`).
- **Dos lenguajes de condición.** `where_parse.py` (`has`, `nonempty`, `in`, `~`, `model <=`, comparaciones, solo ` and `) y `FieldCondition` de `StructuredQuery` (`eq ne gt lt contains starts_with is_null`). Ninguno cruza relaciones; ninguno tiene `or`, `not` ni paréntesis. `propuesta/07-LO-QUE-FALTA.md:190-202` ya lo nombra.
- **Condiciones por arista.** `RelationTypeDoc.condition` y `RelationDoc.condition`; `edges_holding(store, node, subject)` devuelve las aristas cuya condición se cumple sobre un solo payload (`api/edges/edges_holding.py:13-31`). `edges check` no valida que las condiciones parseen.
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

1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de sldb, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review).
2. La validación corre con pytest en el host que el dueño indique; en esta serie fue robocop2. Un nodo no cierra con tests rojos ni con tests saltados.
3. Toda capacidad nueva entra con: modelo o documento spec, comando CLI con envelope JSON, pruebas, entrada en CHANGELOG y doc en `docs/architecture/`. Nada queda "solo en el código".
4. Compatibilidad: `--where` actual sigue funcionando durante la transición; se marca deprecado y se retira en un nodo explícito, no de paso.
5. Nada se persiste del resultado de una regla. Los hechos derivados se recalculan; si un consumidor quiere persistir, escribe un documento propio.
6. Ante un contrato ausente de una dependencia no ejecutada, el nodo registra la hipótesis en su TaskDoc y no inventa API.
7. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

FILE:desk/drawer/plans/grafo-operable/decisiones.md
# Decisiones registradas

Cada entrada dice quién decidió, con qué fuente y en qué fecha. Una recomendación aceptada tácitamente se marca como tal; no se la hace pasar por decisión explícita.

| Id | Decisión | Actor | Fuente | Fecha |
|---|---|---|---|---|
| D1 | sldb se modifica a fondo para evaluar reglas sobre documentos, aristas y hashes ("operativicemos esto lo más posible en sldb; si hay que modificarlo a fondo, démosle"). La pill `pill-keep-sldb-generic-and-move-workflow-behavior-toward-deskops` se reescribe: evaluador genérico en sldb, reglas autoradas fuera. | Dueño | Chat de la sesión de deskops, 2026-11-04; pill editada con `deskops edit pill` | 2026-11-04 |
| D2 | Los gates de activación de una tarea son bloqueo duro, sin bandera de salto. La vía de escape es especializar tipos de tarea (`task.refactor` ≠ `task.debug`), cada tipo con sus gates. | Dueño | Respuesta a la pregunta "qué tan duro debe ser" | 2026-11-04 |
| D3 | No hay coordinación central entre desks: cada desk tiene sus tareas y pide feedback al resto. Scion coordina ejecución; deskops coordina conocimiento. | Dueño | Respuesta a la pregunta "quién acepta la disposición" | 2026-11-04 |
| D4 | El revisor barato bajo Scion sigue siendo pi deepseek, con bundle propio en el fork. | Dueño | Respuesta a la pregunta sobre el harness del revisor | 2026-11-04 |
| D5 | No saltar a Neo4j ahora: costura `GraphBackend` con networkx (ya dependencia de sldb) en proceso; otro motor entra detrás de la misma costura si hace falta. Reglas independientes del backend. | Recomendación del asistente, aceptada tácitamente ("dale") al autorizar este plan | Chat 2026-11-04; el dueño había planteado Neo4j/networkx y que no se decide a saltar a kimun | 2026-11-04, **pendiente de confirmación explícita** |
| D6 | Semántica del lenguaje de reglas: subconjunto de Datalog estratificado (sin funciones más allá de comparaciones, negación estratificada, mundo cerrado por store), para que kimun pueda adoptar reglas y recibos sin traducirlos. | Recomendación del asistente | Informe sobre kimun: decisión 30 (Datalog), evidencia con `ref-hash`, estados derivados | 2026-11-04, **pendiente**: se confirma al aceptar G02 |
| D7 | sldb no construye autenticación de actores; identidad viene de git y de la capa de ejecución. | Recomendación del asistente | Sección "El límite" del brief | 2026-11-04, **pendiente** |
| D8 | kimun no absorbe sldb v1 todavía: migra documentos, no al consumidor (deskops es escritor y kimun abandonó el round-trip estricto; sin cliente Python; modelos en rediseño; capa G bloqueada por D0 y D-G). Criterios para revisarlo: D0 y D-G decididos, spec 16 implementada, camino de escritura con round-trip, cliente o envelope estable, equivalente de condiciones por arista, `migrate` limpio en los cuatro desks. | Hecho verificado por el asistente, aceptado por el dueño al autorizar el plan sobre sldb v1 | Informe sobre kimun, 2026-11-04 | 2026-11-04 |

## Pendientes del dueño

- Confirmar D5, D6 y D7 explícitamente (basta un "sí" por cada una en el chat o una nota al inbox de sldb).
- Las decisiones ya registradas en el Board de sldb que condicionan la operación (journal congelado; `.sldb` versionado y `.sldb_cache` ignorado) siguen en sus tareas; este plan no las reabre.

FILE:desk/drawer/plans/grafo-operable/dag.yaml#node:GO05
id: GO05
title: Lenguaje de predicados unificado
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK02
scope: 'Parser y evaluador del lenguaje de GO02 sobre el backend de GO03 y la proyección
  de GO04: booleanos completos, caminos con cuantificadores, clausura transitiva,
  sustitución desde el sujeto, explicación estructurada. Reemplaza where_parse y FieldCondition
  detrás de una misma API (where_matches, edges_holding, StructuredQuery, --where
  de la CLI); los dos lenguajes viejos quedan como alias deprecados con aviso y tests
  de equivalencia. Los tests xfail de GO02 pasan a verdes. Rendimiento: evaluar una
  regla sobre todos los documentos de un modelo en este repo no debe reextraer Markdown.'
acceptance: Tests de spec de GO02 verdes; tests de equivalencia con los operadores
  viejos verdes; sldb docs find --where con any()/all() sobre una relación responde
  desde la CLI con envelope y, con --explain, la cláusula fallida por documento; CHANGELOG
  y docs/architecture actualizados.
output_scope: src/sldb/store/query_engine/, src/sldb/store/graph/language/, src/sldb/api/where.py,
  CLI --where
depends_on:
- GO02
- GO04
requires:
- G_SEMANTICS
- G_SEAM

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO02
id: GO02
title: Semántica y gramática del lenguaje de reglas
kind: design
owner_repo: sldb
node_role: delivery
parent_id: PK01
scope: 'Documento docs/architecture/rules-language.md que fija: gramática (and/or/not,
  paréntesis, comparaciones, in [...], regex, model <= X, has/nonempty); caminos sobre
  relaciones por nombre de relación y de campo (p. ej. depends_on, reviewed_by) con
  cuantificadores any/all/none/count y clausura transitiva (+); sustitución {campo}
  desde el sujeto; semántica: Datalog estratificado, negación solo estratificada,
  mundo cerrado por store (a través de links: desconocido, no falso), sin funciones
  salvo comparaciones; formato de explicación (cláusula fallida, nodo, valor visto);
  hash de contrato: definido por el modelo como subconjunto de campos, calculado desde
  field_hashes. Incluye la tabla de equivalencia con where_parse y FieldCondition
  actuales. Sin código salvo ejemplos como tests de spec.'
acceptance: El documento existe; cada construcción tiene un ejemplo con resultado
  esperado; la tabla de equivalencia cubre todos los operadores actuales; los ejemplos
  están como tests marcados xfail hasta GO05; revisión en frío aceptada; dueño confirma
  D6. Produce G_SEMANTICS.
output_scope: docs/architecture/rules-language.md, tests de spec xfail
depends_on:
- GO01
requires:
- G_BOUNDARY

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO04
id: GO04
title: Payload proyectado al grafo y staleness correcta
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK02
scope: Los campos escalares y listas de escalares de cada documento (o los que el
  modelo declare en __indexed__) entran al nodo del índice de aristas como facet payload,
  con el content_hash y los field_hashes; la proyección se invalida por hash y se
  reconstruye con el dirty set existente. Arreglar EdgeIndex.stale para que una edición
  externa del Markdown y un campo nuevo de __references__ marquen stale (inbox 20261102-065705).
  StructuredQuery puede filtrar por campos del payload. Sin cambiar el formato de
  los shards más de lo necesario; EDGE_INDEX_VERSION sube.
acceptance: 'Tras una escritura, el nodo expone los campos declarados; editar el Markdown
  por fuera marca stale y la reconstrucción los actualiza; una consulta estructurada
  por campo (p. ej. status = closed) responde sin extraer Markdown (medido: ninguna
  llamada a Validator.extract en la consulta); tamaño del índice medido antes y después
  en este repo y registrado.'
output_scope: src/sldb/store/edge_index/, src/sldb/store/edge_sync.py, src/sldb/store/graph/facet_match.py
depends_on:
- GO03
requires:
- G_SEAM

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO06
id: GO06
title: RuleDoc y rules check
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK03
scope: 'Modelo RuleDoc: sujeto (familia de modelo vía base_models y un filtro en el
  lenguaje), condición, severidad (error | alert), momento (on_write | on_transition
  | on_check), mensaje de explicación. Registro de reglas en el store como cualquier
  documento; comando sldb rules check [--subject DOC] que evalúa las reglas aplicables
  y emite Finding por el canal existente de errores y alertas; sldb rules explain
  para una regla y un sujeto. Las reglas tienen hash: cambiar una regla invalida lo
  derivado que depende de ella (GO08 lo usa). Reemplaza al Constraint de docs/opsys
  que nunca tuvo código.'
acceptance: En un store temporal, una RuleDoc con sujeto por familia aplica a los
  subtipos y no a los hermanos; rules check reporta error y alert con cláusula y nodo;
  una regla mal formada es rechazada al escribirla con el error del parser; documentación
  en docs/architecture/rules.md.
output_scope: src/sldb/models/rule_doc.py, src/sldb/api/rules/, src/sldb/cli/commands/rules.py
depends_on:
- GO05
requires:
- G_SEMANTICS

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO09
id: GO09
title: Transiciones como datos de la arista
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK04
scope: 'Convención documentada para RelationDoc.attributes de una transición: sets
  (campos que la transición escribe en el sujeto, p. ej. status) y terminal; edges_holding
  devuelve con cada arista que se cumple sus efectos; una función aplica los efectos
  al sujeto sin persistir. Con esto la máquina de estados es entera datos del store
  y un consumidor no necesita un YAML paralelo. Compatibilidad: aristas sin attributes
  se comportan como hoy.'
acceptance: En un store de prueba con tres estados y tres transiciones, edges_holding
  devuelve la transición que aplica con sus efectos; aplicar los efectos produce el
  payload esperado; la doc de edges describe la convención; deskops puede retirar
  sets_status/terminal de su YAML (lo verifica deskops en G_CONSUMER).
output_scope: src/sldb/api/edges/, src/sldb/models/relation_doc.py, docs/architecture/
depends_on:
- GO05
requires:
- G_SEAM

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:PK02
id: PK02
title: Sustrato
owner_repo: sldb
node_role: aggregate
children:
- GO04
- GO05
scope: Que el grafo tenga los campos y que exista un solo lenguaje de predicados que
  los lea y cruce relaciones. GO04 proyecta el payload a los nodos y arregla la detección
  de staleness; GO05 implementa el lenguaje de GO02 sobre la proyección de GO04 y
  reemplaza los dos lenguajes actuales.
acceptance: --where nuevo evalúa sin re-extraer Markdown; una consulta con any()/all()
  sobre una relación responde desde la CLI con explicación; where_parse y FieldCondition
  marcados deprecados con tests de equivalencia.

FILE:desk/drawer/plans/grafo-operable/dag.yaml#gates
G_SEMANTICS:
  title: Semántica del lenguaje de reglas aceptada
  state: pending
  produced_by: GO02
  resolver: revisión en frío de GO02 aceptada por el desk de sldb y confirmación explícita
    del dueño de D6
  evidence: docs/architecture/rules-language.md con gramática, semántica estratificada,
    mundo cerrado por store y formato de explicación; ejemplos ejecutables como tests
    de la spec
G_SEAM:
  title: Costura GraphBackend definida
  state: pending
  produced_by: GO03
  resolver: revisión en frío de GO03 aceptada y confirmación de D5
  evidence: protocolo GraphBackend (load, eval) documentado y una implementación networkx
    que carga el índice compuesto actual sin cambiar ninguna salida existente

FILE:instruccion
Revisa el nodo GO05 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

