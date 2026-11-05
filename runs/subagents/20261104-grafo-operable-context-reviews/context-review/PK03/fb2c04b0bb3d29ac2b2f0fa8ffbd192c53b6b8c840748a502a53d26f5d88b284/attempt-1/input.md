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
- Las decisiones D1–D8 están tomadas (D5, D6 y D7 confirmadas el 2026-11-04). Un gate `pending` que dependa de una revisión aceptada no es ambigüedad del nodo.
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

FILE:desk/drawer/plans/grafo-operable/dag.yaml#node:PK03
id: PK03
title: Reglas y anclas
owner_repo: sldb
node_role: aggregate
children:
- GO06
- GO07
scope: 'Reglas como documentos y anclas a documentos con hash de contrato. Un ancla
  doc: es el valor de un campo declarado por el modelo en __doc_anchors__ (o el from:
  de la procedencia), con la forma doc:Model:name@sha256:<hash de contrato visto>;
  el hash lo escribe sldb al guardar si el escritor lo omite; si el escritor trae
  un hash, se conserva tal cual como hash visto (anchors check dirá changed si no
  coincide). anchor_state es una propiedad del ancla, es decir del valor del campo
  en el documento que lo contiene; en un camino que atraviesa un campo de ancla, cada
  elemento alcanzado expone el anchor_state del ancla por la que se llegó. Un recibo
  (documento de un consumidor que afirma un hecho externo) se ata a su sujeto con
  esa ancla; sldb no define modelos de recibo. GO06 define RuleDoc y rules check;
  GO07 define el ancla doc: y sus estados.'
acceptance: sldb rules check reporta findings con severidad y cláusula fallida; sldb
  anchors check reporta intact/changed/lost para anclas doc:; un documento con un
  campo __doc_anchors__ queda consultable desde una regla por anchor_state (verificado
  en la aceptación de GO07).

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO06
id: GO06
title: RuleDoc, rules check y rules explain
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK03
scope: 'Modelo RuleDoc: sujeto = familia de modelo (expresión model <= X, resuelta
  con la herencia de modelos ya existente en sldb: base_models del registro, la misma
  que usan source_types y target_types de RelationTypeDoc) más un campo where opcional
  (predicado en el lenguaje, evaluado sobre cada candidato antes de la condición;
  false o incomplete = la regla no aplica a ese documento); condición (campo condition);
  severidad (error | alert); momento (on_write | on_transition | on_check); message
  opcional (si existe, Finding.what = message seguido de la explicación de GO02; si
  no, solo la explicación). Validación al escribir una RuleDoc: condition y where
  parsean, severidad y momento están en su vocabulario, el sujeto resuelve a un modelo
  registrado; cualquier fallo rechaza la escritura con el error. Registro como cualquier
  documento. Comando sldb rules check [--subject DOC]: con --subject evalúa sobre
  ese documento todas las reglas cuyo sujeto lo incluye, de cualquier momento; sin
  --subject evalúa todas las reglas on_check sobre todos los documentos de su familia.
  Emite Finding (src/sldb/core/finding.py: level, code, subject, what, fix, document)
  por el canal existente: level = severidad de la regla, code = rules/<nombre de la
  RuleDoc>, subject = el documento, what = message seguido de la explicación de GO02
  (o solo la explicación si no hay message). rules check convierte a Finding de core
  solo los resultados false e incomplete: false → level = severidad de la regla, code
  rules/<nombre>; incomplete → level alert, code rules/<nombre>/incomplete, sin importar
  la severidad. Exit 1 si hay al menos un Finding error, 0 en otro caso (los alerts
  nunca fallan). DOC en --subject y SUBJECT en explain aceptan Model:name o ruta;
  RULE acepta RuleDoc:<nombre>, <nombre> o ruta. Una referencia que no resuelve (documento
  o regla) es el error existente de documento desconocido de sldb, con su exit y mensaje.
  Una RuleDoc mal formada se rechaza con el error de validación existente al escribir
  documentos (el ValidationError del modelo en el envelope, con el campo y el motivo).
  sldb rules explain RULE SUBJECT imprime en el envelope el finding de eval tal como
  lo define GO02 (node, holds, clause, seen), también cuando holds es true; exit 0
  si true, 1 si false, 2 si incomplete, 3 si la regla no aplica al sujeto (familia
  o where), con el motivo en el envelope; la severidad no afecta el exit. Hash de
  regla = content_hash del RuleDoc; GO08 lo incluye en la clave de su caché derivada.
  docs/opsys/bridge_primitives/README.md: la sección Constraint se marca como reemplazada
  por RuleDoc con enlace a rules.md.'
acceptance: En un store temporal con modelos Base, X < Base, Y < X y Z < Base, una
  RuleDoc con sujeto model <= X aplica a X e Y y no a Z; rules check reporta error
  y alert como Finding con cláusula y nodo, con exit 1 solo ante error; rules check
  sin --subject recorre solo on_check; --subject acepta Model:name y ruta; rules explain
  devuelve el finding de eval y los exits 0/1/2, y exit 3 con una regla cuyo where
  excluye al documento; un resultado incomplete en rules check sale como alert rules/<nombre>/incomplete;
  una regla mal formada en condition, where, severidad, momento o sujeto es rechazada
  al escribirla con el error correspondiente; documentación en docs/architecture/rules.md;
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
  define GO02); si el destino no existe, se guarda sin hash. Estados: intact (hash
  igual), changed (hash distinto), lost (sin destino, o con destino pero sin hash);
  un ancla sin hash cuyo destino ya existe se pinnea en la siguiente escritura del
  documento que la contiene. GO07 expone check_doc_anchors(store) → list[Finding]
  y extiende el comando anchors check (src/sldb/cli/commands/anchors.py) para usarla;
  el cableado en stores check lo hace GO08 (dueño de api/stores); no hay reconnected
  para documentos. Severidad: changed y lost son alertas, nunca error, como las anclas
  de código. Un campo __doc_anchors__ solo admite vacío/null o valores con forma doc:Model:name[@sha256:<hash>];
  otro texto es error de validación al escribir; <hash> son 64 caracteres hexadecimales
  y un @sha256: vacío o malformado es error. from: de Provenance es escalar (str);
  un from: que no empieza por doc: (p. ej. code:) no es ancla de documento y este
  nodo no lo toca. El verify que provenance.md diseñó y nunca se implementó (alcance.md)
  es el mismo mecanismo aplicado a from:: Finding alert con code anchors/provenance_changed
  (destino con contrato distinto) o anchors/provenance_lost (sin destino o sin hash),
  emitido por anchors check por el canal de alertas; un from: sin hash se pinnea en
  la siguiente escritura igual que cualquier ancla. anchor_state se expone sin tocar
  el lenguaje ni el shard: al componer o leer la proyección, GO07 agrega a la facet
  payload, por cada campo __doc_anchors__, una entrada derivada <campo>__anchor_state
  (escalar para un campo str; lista alineada para list[str]) calculada en ese momento
  comparando el hash visto en el valor del campo con el hash de contrato actual del
  destino, que se calcula desde los field_hashes del destino ya presentes en el índice
  (GO04); no se persiste en el shard, así que editar el destino no exige invalidar
  al contenedor y EDGE_INDEX_VERSION no cambia; el sufijo __anchor_state queda reservado:
  un modelo que declare un campo con ese sufijo es error al cargar la definición del
  modelo. El lenguaje de GO05 la lee como cualquier campo; ^subject es el recorrido
  inverso de las aristas references que el campo subject declara, y en ese recorrido
  el evaluador adjunta a cada elemento alcanzado, bajo el nombre anchor_state, la
  entrada derivada del campo por el que se llegó. Varias anclas en un campo lista
  = un estado por elemento.'
acceptance: 'Un documento A con campo subject en __doc_anchors__ se guarda con doc:TaskDoc:b
  y queda pinneado con el hash de B; editar un campo del __contract__ de B deja el
  ancla changed; editar un campo fuera del contrato la deja intact; borrar B la deja
  lost; anchors check lo reporta como alertas (stores check lo hará vía GO08); con
  un modelo Review (campos subject en __doc_anchors__ y verdict) y una Task B como
  sujeto, la regla any(^subject: anchor_state = "intact" and verdict = "accepted")
  evalúa true cuando existe una Review con subject pinneado a B intacto y verdict
  accepted, y false sin Review, con verdict distinto o con el ancla changed; un valor
  no doc: en subject es rechazado al escribir; un documento con from: doc:B emite
  provenance_changed tras editar el contrato de B; docs/architecture/anchoring.md
  documenta __doc_anchors__, la forma con hash, el pinneado y la ausencia de reconnected;
  CHANGELOG.'
output_scope: src/sldb/api/anchors/, src/sldb/cli/commands/anchors.py, src/sldb/models/provenance.py,
  src/sldb/models/ (atributo __doc_anchors__ en el modelo base), src/sldb/api/documents/payload_save_steps.py
  (pinneado), src/sldb/store/edge_index/ (entrada derivada <campo>__anchor_state en
  la proyección), docs/architecture/anchoring.md, CHANGELOG.md
depends_on:
- GO04
- GO05
requires:
- G_SEMANTICS

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
  queda como shim que traduce al AST nuevo con el mismo aviso; en la CLI, --where
  entra siempre por la vía nueva y nunca avisa; el único comando de la CLI que entra
  por la vía vieja es el que recibe filtros FieldCondition como dicts (la consulta
  estructurada, graph query con sus filtros JSON), y ese agrega una entrada a la lista
  warnings del envelope (docs/cli-envelope.md); en Python, llamar a where_parse/compile_where
  o construir FieldCondition emite DeprecationWarning; los operadores de where_parse
  no avisan por sí mismos, porque la gramática nueva los incluye idénticos. Los tests
  de equivalencia comparan el resultado nuevo con los goldens. Los tests xfail de
  GO02 pasan a verdes. API única detrás de where_matches, edges_holding, StructuredQuery
  y --where. El retiro de los shims es GO10.'
acceptance: Tests de spec de GO02 verdes; tests de equivalencia contra goldens verdes;
  sldb docs find --where con any()/all() sobre una relación responde desde la CLI
  con envelope y, con --explain, la cláusula fallida por documento; un test cuenta
  cero llamadas a Validator.extract al evaluar un --where sobre todos los documentos
  de un modelo de este repo; un test captura el DeprecationWarning al llamar a where_parse
  y al construir un FieldCondition, otro captura la entrada en warnings del envelope
  de graph query con filtros dict, y otro comprueba que --where con la misma expresión
  no avisa; CHANGELOG y docs/architecture actualizados.
output_scope: src/sldb/store/query_engine/, src/sldb/store/graph/language/, src/sldb/api/where.py,
  src/sldb/api/edges/edges_holding.py (enrutado a la API única), CLI --where, docs/architecture/,
  CHANGELOG.md
depends_on:
- GO02
- GO04
requires:
- G_SEMANTICS
- G_SEAM

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO04
id: GO04
title: Payload proyectado al grafo y staleness correcta
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK02
scope: 'Cada nodo de documento del índice de aristas lleva una facet payload: mapa
  plano campo → valor con los campos del payload cuyo valor es escalar (str, int,
  float, bool, null) o lista de escalares (incluida la lista vacía); diccionarios
  y listas con elementos no escalares se omiten de la proyección y se documenta; por
  defecto todos esos campos, o, si el modelo declara el atributo de clase __indexed__,
  exactamente los nombres listados en lugar del conjunto por defecto (un nombre ausente
  en el payload de un documento se omite; un nombre cuyo tipo declarado en el modelo
  (la anotación pydantic del campo) no es escalar ni lista de escalares es error al
  registrar o cargar la definición del modelo, no por documento). content_hash ya
  está en el nodo (hash_c); field_hashes se agrega. Formato de shard: se agregan cuatro
  claves al registro del nodo, payload, field_hashes, source_hash y contract_signature;
  nada más cambia; EDGE_INDEX_VERSION pasa de 4 a 5; al abrir el store, un shard con
  versión menor se marca stale; la reconstrucción ocurre en la siguiente reconstrucción
  del índice (la próxima escritura o stores build), con el dirty set existente. La
  invalidación la gobierna el source_hash del archivo (content_hash deriva de él):
  stale por source_hash o por contract_signature; la proyección se recalcula al reconstruir.
  Arreglar EdgeIndex.stale: el shard guarda source_hash del documento y la firma de
  contrato del modelo: sha256 del JSON canónico (claves ordenadas, UTF-8, sin espacios)
  de {fields: todos los nombres de campo del modelo tras la herencia (propios y heredados
  por base_models), ordenados (no solo los proyectados), references: nombres de __references__
  ordenados, containment: nombres de __containment__ ordenados, compositions: nombres
  de __compositions__ ordenados; cada atributo ausente aporta la lista vacía}, solo
  nombres; stale cuando el source_hash del archivo difiere o la firma de contrato
  del modelo cargado difiere (inbox 20261102-065705); la comprobación se hace donde
  hoy se consulta EdgeIndex.stale: al abrir el store y antes de cada consulta o reconstrucción
  del índice. StructuredQuery acepta filtros sobre la facet payload con sus operadores
  actuales y la semántica que facet_match ya aplica a las facets existentes; sobre
  null solo deciden is_null e is_not_null (los demás dan false); sobre una lista,
  contains es pertenencia y eq/ne comparan la lista entera, gt/lt dan false; en structural_queries.py
  y en su executor (src/sldb/store/graph/executor.py, el que ejecuta StructuredQuery;
  no es el eval de GO03). Un filtro sobre un campo no proyectado (anidado, fuera de
  __indexed__ o inexistente en el modelo) es un error de consulta que nombra el campo;
  un campo proyectable ausente en todos los payloads da conjunto vacío; nunca re-extrae.
  GO04 no cambia el resultado de ninguna consulta existente.'
acceptance: Tras una escritura, el nodo expone los campos proyectados y omite los
  anidados; editar el Markdown por fuera marca stale y la reconstrucción los actualiza;
  agregar un campo a __references__ marca stale; una consulta estructurada por campo
  (status = closed) responde con cero llamadas a Validator.extract (contadas en el
  test); EDGE_INDEX_VERSION = 5; un shard de versión 4 queda stale al abrir y se reconstruye
  en la siguiente escritura; los tests existentes de StructuredQuery pasan sin cambios;
  tamaño del índice en MB y número de shards de este repo antes y después, registrados
  en la sección Validation del TaskDoc y en CHANGELOG.
output_scope: src/sldb/store/edge_index/, src/sldb/store/edge_sync.py, src/sldb/store/graph/facet_match.py,
  src/sldb/store/graph/executor.py, src/sldb/store/query_engine/structural_queries.py,
  docs/architecture/graph-backend.md (sección de la proyección y sus omisiones), CHANGELOG.md
depends_on:
- GO03
requires:
- G_SEAM

FILE:instruccion
Revisa el nodo PK03 siguiendo context-review-guide.md. Es un agregado: reformula el resultado sustantivo del paquete y da un DRY-RUN hipotético de sus hijos en orden, con entradas y salidas entre ellos y la validación conjunta. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

