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

FILE:desk/drawer/plans/grafo-operable/dag.yaml#node:PK01
id: PK01
title: Fundamentos
owner_repo: sldb
node_role: aggregate
children:
- GO01
- GO02
- GO03
scope: 'Dejar escritas la frontera, la semántica del lenguaje y la costura del backend
  antes de cambiar el comportamiento del store. En serie: GO01 registra la decisión;
  GO02 fija semántica, gramática y la firma de evaluación; GO03 fija el protocolo
  del backend con esa firma y lo implementa sobre networkx sin cambiar ninguna salida.
  GO03 escribe bajo src/sldb/store/graph/, lo cual está permitido: la restricción
  es no cambiar el comportamiento observable de los comandos existentes sobre stores
  existentes; una clave nueva de store.yaml con validación propia es comportamiento
  nuevo, no un cambio.'
acceptance: G_BOUNDARY, G_SEMANTICS y G_SEAM satisfechos.

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO01
id: GO01
title: Registrar la decisión de frontera y su atom
kind: decision
owner_repo: sldb
node_role: delivery
parent_id: PK01
scope: 'La pill ya está reescrita y commiteada con este plan (rev 5; su texto está
  en el repo). GO01 agrega un atom nuevo en desk/atoms (creado con deskops add atom
  --title "sldb evaluates declared rules; consumers author them" --five-wh-one-plus
  what --answer ..., los tres campos obligatorios del subject atom; el what es el
  título) cuyo answer diga que sldb evalúa reglas declaradas sobre documentos, aristas
  y hashes y que los consumidores las autoran como documentos; la pill enlaza el atom
  en su campo where o how (deskops edit pill). Dos commits en main: el primero con
  el atom y la pill enlazada; el segundo edita solo gates.G_BOUNDARY en este dag.yaml
  a state satisfied con el hash del primero como evidence (ambos alcanzables desde
  main; sin amend). Nota a deskops con el canal sancionado entre desks: deskops message
  send --to deskops --kind suggestion desde el checkout de sldb (D3), con título "sldb
  evalúa reglas declaradas: plan grafo-operable en sldb/desk/drawer/plans/grafo-operable"
  y cuerpo = dos párrafos: la ruta del plan relativa a la raíz de sldb (desk/drawer/plans/grafo-operable/)
  y la fila D1 de decisiones.md copiada entera; eso escribe un archivo en deskops/desk/inbox
  y es lo único que toca deskops. No cambia código.'
acceptance: git log de main de sldb muestra un commit con el atom y la pill enlazada;
  el atom aparece en la pill; existe un archivo nuevo en deskops/desk/inbox cuyo título
  es el indicado y cuyo cuerpo contiene la ruta del plan y el texto D1; gates.G_BOUNDARY
  en dag.yaml tiene state satisfied y evidence con el hash del primer commit, alcanzable
  desde main.
output_scope: desk/contexts/pill-keep-sldb-generic-and-move-workflow-behavior-toward-deskops.md,
  desk/atoms/, desk/drawer/plans/grafo-operable/dag.yaml (solo gates.G_BOUNDARY),
  deskops/desk/inbox (vía message send)
depends_on: []
requires: []

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO02
id: GO02
title: Semántica, gramática y firma de evaluación del lenguaje de reglas
kind: design
owner_repo: sldb
node_role: delivery
parent_id: PK01
scope: 'Documento docs/architecture/rules-language.md que fija: (a) gramática: and/or/not
  con precedencia not > and > or, asociativos a la izquierda, paréntesis para agrupar
  (la "conjunción de nivel superior" es la cadena de and que queda arriba tras parsear
  con esa precedencia), comparaciones = != < <= > >=, in [...], regex ~ (sabor Python
  re, semántica de búsqueda como el ~ actual de where_parse, regex inválida = error
  de parseo: la excepción WherePredicateError existente, que la CLI convierte en Finding
  error en el envelope), model <= X, has/nonempty, y las construcciones equivalentes
  a los operadores actuales contains, starts_with, is_null, is_not_null (como operadores
  propios o como derivadas documentadas); (b) caminos: un paso se escribe como nombre
  de campo (depends_on: sigue las aristas references que ese campo declara), rel:<tipo>
  (sigue las aristas de ese tipo de relación, p. ej. rel:task_activates) o con prefijo
  ^ para la inversa (^subject: los documentos cuyo campo subject apunta al actual);
  cuantificadores any/all/none sobre los elementos alcanzados, con un predicado entre
  paréntesis; count(camino: predicado) es un entero que solo se usa dentro de una
  comparación (count(depends_on: status = "open") = 0); clausura transitiva: el signo
  + pegado al paso (depends_on+, rel:tipo+, ^subject+) sigue ese paso repetidamente
  en la misma dirección, origen excluido, resultado como conjunto sin duplicados,
  termina ante ciclos; sustitución {campo} desde el payload del sujeto, con la sintaxis
  que ya usa where_subject: el nombre del campo entre llaves, sin escapes, reconocido
  solo fuera de literales entre comillas, y un campo ausente o no escalar hace que
  el predicado no se cumpla; (c) semántica: bivaluada dentro del store (mundo cerrado
  por store, Datalog estratificado, negación solo estratificada, sin funciones salvo
  comparaciones); una referencia a un documento inexistente dentro de un store disponible
  no produce elemento: se omite del conjunto alcanzado por el camino (ver (f)); una
  referencia que cae en un store enlazado no disponible (no resoluble al evaluar)
  da incomplete; incomplete se combina con lógica trivaluada de Kleene fuerte para
  and/or/not, any = or sobre los elementos, all = and, none = not any, una comparación
  con count es incomplete si algún elemento del camino es incomplete; una regla error
  con resultado incomplete falla con explicación "incomplete", una alert lo reporta;
  (d) formato de explicación: cláusula fallida, nodo, valor visto, en el envelope;
  (e) hash de contrato: el modelo declara el subconjunto de campos con el atributo
  de clase __contract__ (lista de nombres; ausente = todos los campos del payload);
  se calcula como sha256 de las líneas "<campo>=<field_hash>" ordenadas por los bytes
  UTF-8 del nombre del campo, unidas por \n, sin salto final, codificadas en UTF-8;
  (f) la firma de evaluación que GO03 implementa: eval(predicado parseado, sujeto
  opcional) devuelve una lista de findings con node, holds (true/false/incomplete),
  clause, seen; con sujeto, un finding para ese sujeto; sin sujeto, un finding por
  cada documento del dominio: todos los documentos del store, salvo que el predicado
  sea una conjunción de nivel superior que contenga model <= X, en cuyo caso el dominio
  son los documentos de esa familia (un model <= X anidado bajo not, or, un cuantificador
  o un camino no restringe el dominio); seen = mapa campo → valor leído para las hojas
  de la cláusula que decidió el resultado. Una referencia a un documento inexistente
  se omite del conjunto alcanzado por un camino (all sobre conjunto vacío = true,
  any = false, count = 0). __contract__ vacío = error al cargar el modelo; un campo
  listado ausente del payload aporta la línea "<campo>=" con hash vacío. Tabla de
  equivalencia con where_parse y FieldCondition, operador por operador. Sin código
  salvo los ejemplos como tests de spec marcados xfail.'
acceptance: El documento existe y cada construcción de (a) y (b) tiene un ejemplo
  con resultado esperado, incluidos regex inválida y clausura con ciclo; la tabla
  cubre has, nonempty, in, ~, model <=, = != < <= > >=, eq, ne, gt, lt, contains,
  starts_with, is_null, is_not_null; el ejemplo de regex inválida espera WherePredicateError;
  la tabla trivaluada cubre and, or, not, any, all, none y la comparación con count;
  la sintaxis de caminos (campo, rel:tipo, ^) tiene un ejemplo cada una; __contract__,
  su orden canónico y la firma de eval están definidos; los ejemplos están como tests
  xfail (no skipped) hasta GO05; revisión en frío aceptada. Produce G_SEMANTICS.
output_scope: docs/architecture/rules-language.md, tests de spec xfail
depends_on:
- GO01
requires:
- G_BOUNDARY

FILE:desk/drawer/plans/grafo-operable/dag.yaml#edge:GO03
id: GO03
title: Costura GraphBackend sobre networkx
kind: code
owner_repo: sldb
node_role: delivery
parent_id: PK01
scope: 'Protocolo GraphBackend con tres operaciones: load(índice compuesto, proyección),
  eval(predicado parseado, sujeto opcional) → findings, y analyze(op, args) → resultado,
  donde op es uno de path, cycles, order, components, central, similar con los argumentos
  que hoy reciben; el backend nunca expone su grafo interno. Índice compuesto = el
  objeto que hoy devuelve compose (store/edge_index/compose.py: nodos y aristas ya
  resueltos); el backend lo recibe, no lo compone. Proyección = mapa export_id → facet
  payload o None; load la guarda; eval la lee cuando el sujeto se pasa como export_id
  y usa el payload cuando el sujeto se pasa como payload; en GO03 la proyección real
  es siempre None (GO04 la produce), así que los tests de GO03 pasan el sujeto como
  payload. Implementación networkx que envuelve lo que hoy hacen compose y el análisis
  de grafo; los seis comandos graph y la API api/graph llaman a analyze, sin cambiar
  ninguna salida. eval en este nodo acepta exactamente el subconjunto de GO02 sin
  caminos (has, nonempty, in, ~, model <=, comparaciones, and/or/not, paréntesis)
  evaluado sobre la facet del sujeto si el sujeto es un export_id con proyección cargada,
  o sobre el payload pasado; un predicado con camino levanta NotImplementedError hasta
  GO05. Selección por la clave graph_backend de store.yaml: un escalar string; admitidos
  en esta fase solo "networkx", sin nombres reservados; ausente = networkx; otro valor
  = error al cargar el store con el mensaje "graph_backend <valor> no admitido; admitidos:
  networkx". Documento docs/architecture/graph-backend.md con el protocolo y la regla:
  cualquier motor futuro (Kùzu, Neo4j, Datalevin) entra detrás de esta costura; las
  reglas no lo ven.'
acceptance: Goldens de los seis comandos graph idénticos a antes; los tests existentes
  de api/graph pasan sin cambios y un test con un backend espía comprueba que cada
  comando graph y cada función de api/graph invocan al backend; un test carga el índice
  compuesto del propio repo en el backend; un test evalúa has(id) and status != "x"
  por eval sobre un documento y recibe un finding con la forma de GO02, y un predicado
  con camino levanta NotImplementedError; store.yaml sin clave carga networkx, con
  clave inválida falla con mensaje que lista ["networkx"]; el protocolo está documentado;
  CHANGELOG. Produce G_SEAM.
output_scope: src/sldb/store/graph/backend*, src/sldb/api/graph/, src/sldb/cli/parsers/graph_analysis.py,
  store.yaml (clave graph_backend), docs/architecture/graph-backend.md, CHANGELOG.md
depends_on:
- GO02
requires:
- G_BOUNDARY

FILE:desk/drawer/plans/grafo-operable/dag.yaml#gates
G_BOUNDARY:
  title: Frontera sldb/deskops reencuadrada por el dueño y commiteada
  state: pending
  produced_by: GO01
  resolver: GO01 (commit en main de sldb de la pill ya editada, el atom y la nota
    a deskops)
  evidence: Decisión D1 registrada en decisiones.md; la pill reescrita entra en el
    commit de este plan (rev 5). El gate se satisface cuando GO01, en su segundo commit,
    reemplace este texto por el hash de su primer commit (el del atom y el enlace
    en la pill).
G_SEMANTICS:
  title: Semántica del lenguaje de reglas aceptada
  state: pending
  produced_by: GO02
  resolver: revisión en frío de GO02 aceptada por el desk de sldb (D6 ya confirmada
    por el dueño el 2026-11-04)
  evidence: docs/architecture/rules-language.md con gramática, semántica estratificada,
    mundo cerrado por store, resultado incomplete en el borde de links, formato de
    explicación, sintaxis __contract__; ejemplos ejecutables como tests de la spec
G_SEAM:
  title: Costura GraphBackend definida
  state: pending
  produced_by: GO03
  resolver: revisión en frío de GO03 aceptada (D5 ya confirmada por el dueño el 2026-11-04)
  evidence: protocolo GraphBackend (load, eval, analyze) documentado, comandos graph
    y api/graph enrutados por analyze con goldens y tests idénticos, eval probado
    en su subconjunto, clave graph_backend en store.yaml

FILE:instruccion
Revisa el nodo PK01 siguiendo context-review-guide.md. Es un agregado: reformula el resultado sustantivo del paquete y da un DRY-RUN hipotético de sus hijos en orden, con entradas y salidas entre ellos y la validación conjunta. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

