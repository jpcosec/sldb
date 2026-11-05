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

Autenticación; motor externo (Neo4j, Kùzu) en esta fase; migrar a kimun; cambiar código o documentos de deskops (deskops consume el resultado en su propio plan, ver `alcance.md` §Consumidor; la única escritura permitida en deskops es una nota a su inbox por el canal entre desks, `deskops message send --to deskops`, según D3); el journal y el split `.sldb`/`.sldb_cache` (tareas activas del Board de sldb, prerrequisito operativo pero no parte de este plan).

FILE:desk/drawer/plans/grafo-operable/alcance.md
# Alcance y estado de partida

## Estado de partida de sldb (verificado 2026-11-04, `src/sldb`)

- **Nodos sin contenido.** Un nodo de documento guarda `export_id`, nombre, modelo, ruta, tags, `hash_c`, `hash_d` (`store/edge_index/doc_structure.py:23-25`). La entrada del documento guarda `source_hash`, `content_hash`, `field_hashes`, tags y procedencia, no el payload (`store/models/document_entry.py:11-18`).
- **`--where` re-extrae.** Carga cada documento del modelo, extrae el payload del Markdown y filtra en Python (`store/query_engine/structural_queries.py:69-80`). Caché en memoria y en el directorio de caché del usuario, fuera del store (`store/runtime_cache.py`, `runtime_cache_disk.py`).
- **Dos lenguajes de condición.** `where_parse.py` (`has`, `nonempty`, `in`, `~`, `model <=`, comparaciones, solo ` and `) y `FieldCondition` de `StructuredQuery` (`eq ne gt lt contains starts_with is_null`). Ninguno cruza relaciones; ninguno tiene `or`, `not` ni paréntesis. `propuesta/07-LO-QUE-FALTA.md:190-202` ya lo nombra.
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

1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de sldb, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review).
2. La validación corre con pytest en el host que el dueño indique; en esta serie fue robocop2. Un nodo no cierra con tests rojos ni con tests saltados.
3. Toda capacidad nueva entra con: modelo o documento spec, comando CLI con envelope JSON, pruebas, entrada en CHANGELOG y doc en `docs/architecture/`. Nada queda "solo en el código".
4. Compatibilidad: `--where` actual sigue funcionando durante la transición; se marca deprecado y se retira en un nodo explícito, no de paso.
5. Nada se persiste del resultado de una regla. Los hechos derivados se recalculan; si un consumidor quiere persistir, escribe un documento propio.
6. Ante un contrato ausente de una dependencia no ejecutada, el nodo registra la hipótesis en su TaskDoc y no inventa API.
7. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.
8. Toda medición que un nodo exige (tamaño del índice, tiempo de escritura) se registra en la sección Validation del TaskDoc del nodo con unidad, método y fecha; si cambia un número de usuario, también en CHANGELOG.

FILE:desk/drawer/plans/grafo-operable/decisiones.md
# Decisiones registradas

Cada entrada dice quién decidió, con qué fuente y en qué fecha. Una recomendación aceptada tácitamente se marca como tal; no se la hace pasar por decisión explícita.

| Id | Decisión | Actor | Fuente | Fecha |
|---|---|---|---|---|
| D1 | sldb se modifica a fondo para evaluar reglas sobre documentos, aristas y hashes ("operativicemos esto lo más posible en sldb; si hay que modificarlo a fondo, démosle"). La pill `pill-keep-sldb-generic-and-move-workflow-behavior-toward-deskops` se reescribe: evaluador genérico en sldb, reglas autoradas fuera. | Dueño | Chat de la sesión de deskops, 2026-11-04; pill editada con `deskops edit pill` | 2026-11-04 |
| D2 | Los gates de activación de una tarea son bloqueo duro, sin bandera de salto. La vía de escape es especializar tipos de tarea (`task.refactor` ≠ `task.debug`), cada tipo con sus gates. | Dueño | Respuesta a la pregunta "qué tan duro debe ser" | 2026-11-04 |
| D3 | No hay coordinación central entre desks: cada desk tiene sus tareas y pide feedback al resto. Scion coordina ejecución; deskops coordina conocimiento. | Dueño | Respuesta a la pregunta "quién acepta la disposición" | 2026-11-04 |
| D4 | El revisor barato bajo Scion sigue siendo pi deepseek, con bundle propio en el fork. | Dueño | Respuesta a la pregunta sobre el harness del revisor | 2026-11-04 |
| D5 | No saltar a Neo4j ahora: costura `GraphBackend` con networkx (ya dependencia de sldb) en proceso; otro motor entra detrás de la misma costura si hace falta. Reglas independientes del backend. | Dueño | Pregunta explícita en el chat de la sesión; respuesta "Sí, networkx tras la costura" | 2026-11-04, confirmada |
| D6 | Semántica del lenguaje de reglas: subconjunto de Datalog estratificado (sin funciones más allá de comparaciones, negación estratificada, mundo cerrado por store), para que kimun pueda adoptar reglas y recibos sin traducirlos. | Dueño | Pregunta explícita en el chat; respuesta "Sí" a Datalog estratificado con `incomplete` en el borde de links | 2026-11-04, confirmada |
| D7 | sldb no construye autenticación de actores; identidad viene de git y de la capa de ejecución. | Dueño | Pregunta explícita en el chat; respuesta "Sí" | 2026-11-04, confirmada |
| D8 | kimun no absorbe sldb v1 todavía: migra documentos, no al consumidor (deskops es escritor y kimun abandonó el round-trip estricto; sin cliente Python; modelos en rediseño; capa G bloqueada por D0 y D-G). Criterios para revisarlo: D0 y D-G decididos, spec 16 implementada, camino de escritura con round-trip, cliente o envelope estable, equivalente de condiciones por arista, `migrate` limpio en los cuatro desks. | Hecho verificado por el asistente, aceptado por el dueño al autorizar el plan sobre sldb v1 | Informe sobre kimun, 2026-11-04 | 2026-11-04 |

## Pendientes del dueño

- D5, D6 y D7 confirmadas el 2026-11-04 (tres preguntas explícitas, tres "Sí"). Sin pendientes de decisión para PK01.
- Las decisiones ya registradas en el Board de sldb que condicionan la operación (journal congelado; `.sldb` versionado y `.sldb_cache` ignorado) siguen en sus tareas; este plan no las reabre.

FILE:desk/drawer/plans/grafo-operable/dag.yaml#node:PK04
id: PK04
title: Operación
owner_repo: sldb
node_role: aggregate
children:
- GO09
- GO08
- GO10
scope: 'Que las reglas se evalúen cuando importa, que la máquina de estados sea entera
  datos y que los lenguajes viejos se retiren. En serie: GO09 lleva el efecto de una
  transición a la arista y agrega effects al resultado de edges_holding; GO08 (depende
  de GO09) evalúa en escritura, transición y check y agrega findings al mismo resultado,
  sin tocar effects; GO10 retira los shims. Frontera en edges_holding: GO09 es dueño
  de la clave effects, GO08 de la clave findings.'
acceptance: Una escritura que viola una regla error es rechazada con explicación;
  una alerta no falla; edges_holding devuelve effects (GO09) y findings (GO08) en
  claves separadas; edges check valida condiciones; el ejemplo end-to-end definido
  en GO08 pasa como test de integración; where_parse y FieldCondition ya no existen.

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO09
id: GO09
title: Transiciones como datos de la arista
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK04
scope: 'Convención documentada para RelationDoc.attributes de una transición: sets
  = mapa campo → valor que la transición escribe en el sujeto (p. ej. {status: closed});
  terminal = booleano que sldb solo transporta. Defaults: attributes ausente, o sin
  sets, equivale a sets = {}; sin terminal equivale a false. Valores de sets admiten
  {campo} con la misma sintaxis y fuente que where_subject (payload del sujeto). edges_holding
  devuelve, con cada arista que se cumple, la clave effects = {sets resueltos, terminal};
  GO08 agregará la clave findings al mismo resultado sin tocar effects. Función pura
  apply_effects(subject, effects, model) → nuevo payload: copia del sujeto con sets
  fusionado en superficie y validado contra model (el llamante lo conoce: edges_holding
  sabe el Model:name del sujeto); levanta el error de validación si no valida; nunca
  persiste.'
acceptance: 'En un store de prueba con tres estados y tres transiciones, edges_holding
  devuelve la transición que aplica con effects resueltos (incluida una sustitución
  {campo}); apply_effects produce el payload esperado y rechaza un valor inválido
  para el modelo; una arista sin attributes devuelve effects = {sets: {}, terminal:
  false}; la doc de edges describe la convención; CHANGELOG; deskops puede retirar
  sets_status/terminal de su YAML (lo verifica deskops en G_CONSUMER).'
output_scope: src/sldb/api/edges/, src/sldb/models/relation_doc.py, docs/architecture/,
  CHANGELOG.md
depends_on:
- GO05
requires:
- G_SEAM

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO08
id: GO08
title: Evaluación en escritura, transición y check, incremental y a punto fijo
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK04
scope: 'on_write: en los pasos de guardado de payload, antes de persistir; una regla
  error rechaza la escritura con la explicación en el envelope y nada queda escrito;
  una alert deja pasar y reporta. on_transition: edges_holding evalúa las reglas on_transition
  cuyo sujeto es el documento y agrega la clave findings a su resultado (la clave
  effects es de GO09 y no se toca). on_check: stores check evalúa todas las on_check
  del store y las reporta como Finding. Caché derivada por dirty set cuya clave incluye
  los content_hash de las reglas (GO06); hechos derivados a punto fijo (semi-naive)
  para reglas recursivas; nunca persistidos. edges check valida que toda condición
  de arista parsee. Ejemplo end-to-end (el de ROOT), como test de integración y documentado
  en rules.md: store temporal con modelos Task (__contract__: title, goal) y Review
  (__doc_anchors__: subject; campo verdict); regla on_transition sobre Task: any(reviews:
  anchor_state = "intact" and verdict = "accepted"), donde reviews es la relación
  inversa de Review.subject; escenario: Task sin Review → la transición no aplica
  y el finding nombra la cláusula any(...); con Review accepted pinneada → aplica;
  editar goal de la Task → el ancla queda changed → vuelve a no aplicar con explicación
  anchor_state = changed. Medición: 20 escrituras de un TaskDoc del store de este
  repo, mediana del tiempo de pared, antes y después, registradas en la sección Validation
  del TaskDoc.'
acceptance: 'Escritura que viola una regla error: rechazada, nada persistido, explicación
  en el envelope; alert: persistida y reportada; edges_holding devuelve findings on_transition
  en su clave y effects intactos; stores check reporta los findings on_check; incrementalidad:
  tras evaluar, una segunda evaluación sin cambios no visita documentos fuera del
  dirty set (contado en el test) y cambiar una regla invalida la caché; grafo de prueba
  A→B→C→A con una regla all(depends_on+: status = "closed") sobre A: con C abierto
  falla nombrando C, con todos cerrados cumple, y la evaluación termina pese al ciclo;
  edges check falla ante una condición mal formada; el test de integración end-to-end
  pasa en sus tres pasos; medición registrada; CHANGELOG.'
output_scope: src/sldb/api/documents/payload_save_steps.py, src/sldb/api/edges/edges_holding.py,
  src/sldb/api/stores/, src/sldb/cli/commands/stores*.py, src/sldb/store/edge_index/validation.py,
  src/sldb/cli/commands/edges.py, docs/architecture/rules.md, CHANGELOG.md
depends_on:
- GO06
- GO07
- GO09
requires:
- G_OPS_PREREQ

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO10
id: GO10
title: Retiro de where_parse y FieldCondition
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK04
scope: 'Borrar los shims de GO05 (where_parse y FieldCondition) y el vocabulario viejo
  de la documentación, una vez que todos los llamantes del repo usan la API única
  (GO05 a GO09 ya migrados). Regla 4 de alcance.md: el retiro es un nodo explícito,
  este. Los goldens de equivalencia se conservan como tests del lenguaje nuevo.'
acceptance: grep de where_parse y FieldCondition en src/ y docs/ no devuelve nada
  salvo CHANGELOG; la suite completa verde; CHANGELOG registra el retiro con la versión.
output_scope: src/sldb/store/query_engine/, src/sldb/store/graph/language/, docs/,
  CHANGELOG.md
depends_on:
- GO08
requires: []

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO05
id: GO05
title: Lenguaje de predicados unificado
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK02
scope: 'Parser y evaluador del lenguaje de GO02 sobre el backend de GO03 y la facet
  payload de GO04: booleanos completos, caminos con cuantificadores, clausura transitiva,
  sustitución desde el sujeto, incomplete en el borde de links, explicación estructurada.
  Compatibilidad: antes de cambiar nada, se capturan goldens del resultado de cada
  expresión de la tabla de GO02 con where_parse y FieldCondition actuales; luego la
  gramática nueva (superconjunto) reemplaza a where_parse, que queda como shim que
  delega en el parser nuevo y emite warnings.warn(DeprecationWarning); FieldCondition
  queda como shim que traduce al AST nuevo con el mismo aviso; en la CLI, usar un
  operador viejo agrega una entrada a la lista warnings del envelope (docs/cli-envelope.md,
  canal de alertas existente). Los tests de equivalencia comparan el resultado nuevo
  con los goldens. Los tests xfail de GO02 pasan a verdes. API única detrás de where_matches,
  edges_holding, StructuredQuery y --where. El retiro de los shims es GO10.'
acceptance: Tests de spec de GO02 verdes; tests de equivalencia contra goldens verdes;
  sldb docs find --where con any()/all() sobre una relación responde desde la CLI
  con envelope y, con --explain, la cláusula fallida por documento; un test cuenta
  cero llamadas a Validator.extract al evaluar un --where sobre todos los documentos
  de un modelo de este repo; un test captura el DeprecationWarning y la entrada en
  warnings del envelope para un operador viejo; CHANGELOG y docs/architecture actualizados.
output_scope: src/sldb/store/query_engine/, src/sldb/store/graph/language/, src/sldb/api/where.py,
  CLI --where, docs/architecture/, CHANGELOG.md
depends_on:
- GO02
- GO04
requires:
- G_SEMANTICS
- G_SEAM

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO06
id: GO06
title: RuleDoc, rules check y rules explain
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK03
scope: 'Modelo RuleDoc: sujeto = familia de modelo (expresión model <= X, resuelta
  con la herencia de modelos ya existente en sldb: base_models del registro, la misma
  que usan source_types y target_types de RelationTypeDoc) más un filtro opcional
  en el lenguaje; condición; severidad (error | alert); momento (on_write | on_transition
  | on_check); mensaje. Registro como cualquier documento. Comando sldb rules check
  [--subject DOC]: con --subject evalúa sobre ese documento todas las reglas cuyo
  sujeto lo incluye, de cualquier momento; sin --subject evalúa todas las reglas on_check
  sobre todos los documentos de su familia. Emite Finding (src/sldb/core/finding.py:
  level, code, subject, what, fix, document) por el canal existente: level = severidad
  de la regla, code = rules/<id de la regla>, subject = el documento, what = la explicación
  de GO02. sldb rules explain RULE SUBJECT imprime el finding completo en el envelope
  (exit 0 si holds, 1 si no, 2 si incomplete). Hash de regla = content_hash del RuleDoc;
  GO08 lo incluye en la clave de su caché derivada. docs/opsys/bridge_primitives/README.md:
  la sección Constraint se marca como reemplazada por RuleDoc con enlace a rules.md.'
acceptance: En un store temporal con modelos Base, X < Base, Y < X y Z < Base, una
  RuleDoc con sujeto model <= X aplica a X e Y y no a Z; rules check reporta error
  y alert como Finding con cláusula y nodo; rules check sin --subject recorre solo
  on_check; rules explain devuelve el finding y los tres exits; una regla mal formada
  es rechazada al escribirla con el error del parser; documentación en docs/architecture/rules.md;
  CHANGELOG.
output_scope: src/sldb/models/rule_doc.py, src/sldb/api/rules/, src/sldb/cli/commands/rules.py,
  docs/architecture/rules.md, docs/opsys/bridge_primitives/README.md, CHANGELOG.md
depends_on:
- GO05
requires:
- G_SEMANTICS

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO07
id: GO07
title: Anclas a documentos con hash de contrato
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK03
scope: 'Un ancla doc: es el valor de un campo: la forma doc:Model:name@sha256:<hash
  de contrato visto>. Los campos que llevan anclas son los que el modelo declara en
  el atributo de clase __doc_anchors__ (lista de nombres de campos de str o de list[str])
  y el from: de Provenance, que pasa a admitir la forma con hash. Persistencia: en
  el propio documento, en el texto del campo; nada aparte. Pinneado: en los pasos
  de guardado de payload, un valor doc:Model:name sin @sha256 en un campo __doc_anchors__
  o en from: se completa con el hash de contrato actual del destino (calculado como
  define GO02); si el destino no existe, se guarda sin hash y queda lost. anchors
  check (y stores check, que lo invoca) evalúan cada ancla a intact (hash igual),
  changed (hash distinto) o lost (documento ausente); no hay reconnected para documentos.
  Severidad: changed y lost son alertas, nunca error, como las anclas de código. El
  verify de provenance.md es el mismo mecanismo aplicado a from:: su alerta se llama
  provenance_changed. anchor_state es un campo derivado consultable desde el lenguaje
  de GO05 sobre el elemento alcanzado por un camino que atraviesa un campo __doc_anchors__.'
acceptance: 'Un documento A con campo subject en __doc_anchors__ se guarda con doc:TaskDoc:b
  y queda pinneado con el hash de B; editar un campo del __contract__ de B deja el
  ancla changed; editar un campo fuera del contrato la deja intact; borrar B la deja
  lost; anchors check y stores check lo reportan como alertas; una regla any(reviews:
  anchor_state = "intact" and verdict = "accepted") evalúa true/false según el caso;
  un documento con from: doc:B emite provenance_changed tras editar el contrato de
  B; docs/architecture/anchoring.md documenta __doc_anchors__, la forma con hash,
  el pinneado y la ausencia de reconnected; CHANGELOG.'
output_scope: src/sldb/api/anchors/, src/sldb/models/provenance.py, src/sldb/models/
  (atributo __doc_anchors__ en el modelo base), src/sldb/api/documents/payload_save_steps.py
  (pinneado), docs/architecture/anchoring.md, CHANGELOG.md
depends_on:
- GO04
- GO05
requires:
- G_SEMANTICS

FILE:instruccion
Revisa el nodo PK04 siguiendo context-review-guide.md. Es un agregado: reformula el resultado sustantivo del paquete y da un DRY-RUN hipotético de sus hijos en orden, con entradas y salidas entre ellos y la validación conjunta. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

