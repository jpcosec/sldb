# Set bootstrap de modelos tras la convergencia átomo/field

Estado (2026-11-07): documento de diseño de la tarea
`task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field`. Evalúa la propuesta punto
por punto y recomienda; **no decide**. Cada punto termina con una línea de decisión que marca el
dueño. No cambia código ni modelos y no crea ninguno de los siete modelos.

Las citas `archivo:línea` son de sldb en `c59db0c5` y de deskops en `f0a4a476`. Las rutas sin
prefijo son de sldb; las de deskops llevan `deskops/` delante (repo hermano
`../deskops`). Los ejemplos nombran documentos trackeados en `.sldb/store.yaml` de sldb por su
export id `Model:name`; todos resuelven con `sldb docs show Model/name --store .sldb`.

## 1. Contexto y fuentes

### 1.1 De dónde viene la propuesta

- **La nota.** `desk/inbox/20261001-031225-unclear-atomo-y-field-convergieron-falta-un-set-bootstrap.md`
  (2026-10-01), promovida al drawer en `12162791`. Su texto vive hoy en la sección Scope de
  `desk/drawer/tasks/task-atomo-y-field-convergieron-falta-un-set-bootstrap.md`.
- **La espiral.** `docs/surface/PROPUESTA-SUPERFICIE.md` §16 «El ciclo» (`:505-536`) y §16.1
  «La espiral» (`:538-555`): «Cada vuelta deja un modelo que antes no existía, y el texto
  siguiente nace más gobernado»; «Los anchors que se repiten con el mismo `kind` son candidatos a
  campo. Suficientes campos con posición estable son un `__template__`»; «El modelo no se
  escribe: se destila», y el `motive` de cada anchor hace auditable la destilación. §16.2
  (`:557-569`) dice qué tramo funciona y cuál no: «Anchors → regularidad → modelo: **no existe**».
- **H1** (procedencia por fragmento), que la regla cita: `docs/surface/PROPUESTA-SUPERFICIE.md:69-86`.
- **El encuadre de §15.1** (`:423-435`): «SLDB no conoce "atoms" ni "anchors": conoce
  documentos gobernados por un contrato». Es la objeción de fondo a varios puntos de abajo.

### 1.2 El marco que este documento toma como dato

- **Principio del dueño (2026-11-05).** Las invariantes de **un** documento son validadores
  pydantic del modelo; las que relacionan **varios** documentos son `RuleDoc`
  (`docs/architecture/rules.md:36-48`; aplicado a las anclas en `docs/architecture/anchoring.md:101-109`;
  se fijó en las tareas GO06-GO09 del plan `desk/drawer/plans/grafo-operable`).
- **G_BOUNDARY** (`desk/drawer/plans/grafo-operable/dag.yaml:15-20`, satisfecho en GO01) y el
  átomo `AtomDoc:atom-sldb-evaluates-declared-rules-consumers-author-them`: sldb evalúa reglas
  declaradas; qué reglas existen, qué es un tipo de tarea o qué significa un gate lo autoran los
  consumidores (deskops) en sus propios desks.
- **Átomos de sldb que tocan contrato, field y procedencia:**
  - `AtomDoc:atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill`:
    el contrato se declara (`create_model`) y se edita por drafts con validación y backfill (SV04).
  - `AtomDoc:atom-el-dueño-de-un-field-es-la-sección-del-template-que-lo-contiene-no-la-línea-donde-quedó-renderizado`:
    la identidad de un field es estructural (su sección en el template), no su línea.
  - `AtomDoc:atom-el-path-guardado-de-un-modelo-es-una-pista-model-ref-es-la-identidad`: la
    identidad de un modelo es su `model_ref` (`module:Class`), no un archivo.
  - `AtomDoc:atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo`: lo que
    el store sabe de un modelo (contrato, familia) es una copia de la clase que se relee.
  - `AtomDoc:atom-una-task-de-diseno-entrega-un-documento-y-su-doc-puede-decir-que-lo-disenado-no-existe`:
    este documento describe cosas que no existen; §2-§3 separan propuesta de estado.
- **Documento hermano.** `docs/architecture/evidence-model-family.md` (rama `wt/diseno-evidencia`)
  concluye que en sldb «familia» ya significa herencia (`base_models`, `model <= X`), que
  `__family__` es una etiqueta que ningún evaluador lee, y que una raíz abstracta registrada con
  cero documentos es barata y es requisito para escribir `RuleDoc` sobre la familia. Este
  documento usa esa conclusión en los puntos 2 (Átomo) y 4 (Grupo) y no la repite.

## 2. Resumen de la propuesta

La nota observa que **átomo y field tienen la misma forma** (un tramo tipado con dirección) y que
el código los trata igual; lo que los distingue es **de dónde sacan identidad**:

- el **átomo**, de su procedencia: ancla, motivo, estado;
- el **field**, de su posición en un contrato.

«Un field es un átomo al que la regularidad le dio un lugar» (la espiral). De ahí propone un
**set bootstrap de siete modelos que modelan el modelar**: Fuente, Átomo, Relación +
TipoDeRelación, Grupo, Composición, Publicación y Modelo («el contrato como documento, salida de
la espiral; hoy no existe»). Una **regla**: «un átomo nunca lleva posición, un field nunca lleva
ancla; se conectan por procedencia (H1) y por promoción». Y una **pregunta abierta**: lo que se
modele encima de este set, ¿es el dominio de cada caso (Levira, MEPU) o SLDB mismo (`desk/`,
pills, requests, `docs/models.py`)?

La nota no define los campos de ningún modelo, salvo lo que se deduce de la espiral. Donde abajo
se interpreta un nombre (Grupo y Publicación sobre todo), se dice.

## 3. Puntos

### 3.1 Fuente

**Qué propone.** Un modelo para el material de afuera, sin organizar ni estructurar (la capa
«LENGUAJE NATURAL» de §16: PDFs, correos, actas, `PROPUESTA-SUPERFICIE.md:508-509`, `:530`), sobre el
que se ponen los anchors.

**Qué existe hoy.**

- **La autoridad `source_raw`** ya nombra exactamente ese papel: «material de afuera: un correo
  pegado, una transcripción, una spec recibida […] **error**: la fuente no muta; otra versión es
  otro documento» (`docs/architecture/provenance.md:42`). El vocabulario está en
  `src/sldb/models/provenance.py:16-17`, y la política ya hace error de editar un documento
  `source_raw` declarado (`src/sldb/api/stores/policy.py:51`). La invariante central de una
  Fuente («no muta») ya está implementada.
- **La derivación desde una fuente** también: `Provenance.from_` admite `doc:Model:name@sha256:…`
  y `code:…` (`src/sldb/models/provenance.py:28`), con estado `intact`/`changed`/`lost`
  (`docs/architecture/anchoring.md` §6). Para código hay un modelo con huella por nodo,
  `CodeAnchorDoc` (`src/sldb/models/code_anchor_doc.py:18-46`).
- **Lo que falta:** un ancla a un **tramo de texto** dentro de una fuente («Texto → anchors:
  contrato listo, **sin superficie**», `PROPUESTA-SUPERFICIE.md:561`), y un modelo genérico que
  sirva de contenedor de una fuente cualquiera. Ningún modelo de sldb declara
  `__authority__ = "source_raw"` (los únicos usos del literal son el vocabulario y la política).

**Ejemplo.** `RequestDoc:req-ontology-feature-request` (`docs/requests/sldb-ontology-feature-request.md`).
Es un pedido que llegó de otros repos (hum, analyzer), es decir «una spec recibida»: el caso de
manual de una Fuente. Hoy se trackea con `RequestDoc`, que declara `__authority__ = "authored"`
(`docs/models.py:255-256`) y guarda todo el cuerpo en un solo field `body` (`:275-277`): si
alguien lo reescribe es una alerta, no un error, y nada permite anclar a un párrafo suyo. Muestra
que el papel existe en el vocabulario pero no tiene modelo.

**Recomendación del redactor: adoptar con cambios.** La Fuente no necesita una semántica nueva:
es **un rol que ya marca la autoridad `source_raw`**. El cambio es agregar a sldb un modelo
genérico mínimo (p. ej. `SourceDoc`: `title`, `origin`, `received_at`, `body`) con
`__authority__ = "source_raw"`, para que haya dónde guardar una fuente sin que cada consumidor
invente uno. Las invariantes de un documento (forma de `received_at`, `origin` no vacío) son
validadores; la inmutabilidad ya la hace la política. El ancla a un tramo de texto es otro
trabajo (la superficie del Lector, `PROPUESTA-SUPERFICIE.md` §6.1) y no se resuelve con este
modelo.

Decisión del dueño: PENDIENTE (adoptado / rechazado)

### 3.2 Átomo

**Qué propone.** Un modelo de átomo cuya identidad sale de su procedencia: ancla, motivo,
estado. Es la capa «KB GRÁFICA (atoms): organizado, sin estructura» de §16.

**Qué existe hoy.**

- **El átomo es de deskops, no de sldb.** `AtomDoc` (`deskops/deskops/models/atom.py:28-80`)
  responde una pregunta 5WH1+ fija (`:54-59`) con un `answer`; su procedencia es un campo libre
  `provenance: str | None` (`:74-80`), sin forma de ancla ni estado. `ProtoAtomDoc`
  (`deskops/deskops/models/protoatom.py:10-48`) es el átomo sin tipo: título, contenido y tags.
- **El motivo existe en `AnchorDoc`** (`src/sldb/models/anchor_doc.py:9-60`): `kind`, `ref`
  tipado y `motive` obligatorio (`:43-53`). Pero ese «anchor» es una entrada de diccionario
  (`PROPUESTA-SUPERFICIE.md:470-471`), un alias que resuelve sin guardar lo que vio
  (`docs/architecture/anchoring.md:17-25`).
- **La procedencia con estado existe** desde GO07: `doc:Model:name@sha256:<hash>` en campos
  `__doc_anchors__` y en `from:` (`src/sldb/models/doc_anchor_value.py:1-9`,
  `src/sldb/models/structured_doc.py:15`), con estados `intact`/`changed`/`lost` y `anchor_state`
  en el lenguaje (`docs/architecture/anchoring.md` §6).
- **En contra:** §15.1 dice que SLDB no conoce «atoms» (`PROPUESTA-SUPERFICIE.md:429-431`), y
  G_BOUNDARY deja la semántica de dominio (qué es un átomo de conocimiento, 5WH1+) del lado de
  los consumidores.

**Ejemplo.** `AtomDoc:atom-sldb-evaluates-declared-rules-consumers-author-them`
(`desk/atoms/atom-sldb-evaluates-declared-rules-consumers-author-them.md`). Su procedencia es
precisa («Owner decision D1 of 2026-11-04 (desk/drawer/plans/grafo-operable/decisiones.md)»),
pero está escrita en prosa dentro de `answer` y su campo `provenance` está vacío: si
`decisiones.md` cambia, nada lo nota. Muestra la distancia entre «identidad por procedencia» y
lo que el modelo guarda hoy.

**Recomendación del redactor: adoptar con cambios.** Adoptar **la procedencia como contrato**,
no un modelo «Átomo» con semántica de conocimiento. Concretamente, una raíz abstracta en sldb
(p. ej. `GroundedDoc`) cuyo único contenido sea la procedencia anclada: un campo
`grounds: list[str]` declarado en `__doc_anchors__` (o el `from:` del bloque `sldb`), un
`motive` y un validador de un documento «`grounds` no vacío». Los átomos de deskops
(`AtomDoc`, `ProtoAtomDoc`) heredarían de ella y conservarían su semántica (5WH1+, dominio). Es
coherente con el documento hermano: la familia es herencia y la raíz se registra aunque tenga
cero documentos, para que una `RuleDoc` pueda decir «todo `model <= GroundedDoc` tiene sus
anclas intactas» (`any(grounds: anchor_state = "intact")` es una regla entre documentos). El
estado es de lectura (`anchor_state`), nunca un campo escrito.

Decisión del dueño: PENDIENTE (adoptado / rechazado)

### 3.3 Relación + TipoDeRelación

**Qué propone.** Las aristas como documentos (Relación) y el vocabulario de verbos como
documentos (TipoDeRelación).

**Qué existe hoy.** Los dos modelos, en sldb y con ese reparto exacto:

- `RelationDoc` (`src/sldb/models/relation_doc.py:13-78`): una arista autorada
  `source_id → target_id` de un `relation_type`, con `condition` y `attributes` (transiciones,
  GO09, `:63-78`), «content-blind» (`:16-19`).
- `RelationTypeDoc` (`src/sldb/models/relation_type_doc.py:12-75`): nombre, dirección,
  cardinalidad, eje del predicado, tipos de origen y destino (con herencia, `:61-68`), condición
  heredada y la descripción como «el motivo del verbo» (`:73-74`).
- Los tipos estructurales que el propio índice produce también son `RelationTypeDoc`
  (`src/sldb/models/relation_type_doc.py:17-20`): «el grafo se describe entero con documentos».
  Diecinueve están trackeados en el store de sldb.
- Diferencia menor con la idea de «procedencia con estado»: `source_id`/`target_id` son
  `__references__` (`src/sldb/models/relation_doc.py:29`), no `__doc_anchors__`; una relación no
  guarda el hash de lo que unió.

**Ejemplo.** `RelationDoc:execution-task_activates` (`desk/lifecycle/execution-task_activates.md`)
con su tipo `RelationTypeDoc:type-task_activates` (`desk/lifecycle/type-task_activates.md`). Es
el par completo en uso real: la arista `RitualDoc:ritual-execution → RitualDoc:ritual-testing`
del ciclo de vida del desk y el tipo que fija sus extremos (`RitualDoc`), eje `HOW` y
cardinalidad.

**Recomendación del redactor: adoptar** (ya existe; el set los incluye sin cambios). Pasar
`source_id`/`target_id` a anclas pinneadas es posible pero no lo pide la propuesta ni lo
necesita el set; si el dueño lo quiere, es una tarea aparte.

Decisión del dueño: PENDIENTE (adoptado / rechazado)

### 3.4 Grupo

**Qué propone.** La nota solo da el nombre. Interpretación del redactor: un conjunto con nombre
de documentos (átomos, sobre todo), **sin orden ni plantilla**: pertenencia sin posición. Es lo
que distingue a un Grupo de una Composición (3.5), que sí tiene orden y render.

**Qué existe hoy.** Cuatro maneras de agrupar, cada una con su uso:

- **Por lista en un documento:** `__containment__` (`src/sldb/models/structured_doc.py:13`,
  `docs/architecture/model-authoring.md:11`), que el grafo materializa como aristas `contains`.
- **Por etiqueta:** el DAG de tags y las relaciones `tagged_as` y `semantic_parent`
  (`sldb/relation_types/tagged_as.md`, `sldb/relation_types/semantic_parent.md`); en deskops, el
  árbol de dominio con `CrossroadDoc` como padre obligatorio de cada camino
  (`deskops/deskops/models/crossroad.py:17-45`).
- **Por consulta:** `ViewDoc.nodes` es una unión de `{model, where}`
  (`src/sldb/models/notation/view_doc.py:31-34`), y un selector `st.{Model+}` o un `--where`
  nombran conjuntos sin escribirlos.
- **Por herencia,** para grupos de modelos: `model <= X` (documento hermano, §1.2).

**Ejemplo.** `BoardDoc:Board` (`desk/tasks/Board.md`). Su campo `pills` es un grupo puro: diez
pills contenidas por `__containment__` (`deskops/deskops/models/board.py:7`) y ningún render;
nadie lee un orden en esa lista. El mismo documento tiene, en `tasks`, una composición (3.5), y
por eso sirve para ver la diferencia.

**Recomendación del redactor: no adoptar** como modelo propio. Un `GroupDoc` duplicaría lo que
ya hacen una lista contenida (cuando el grupo es de alguien), una etiqueta (cuando es una
clasificación) o una `ViewDoc` (cuando es una consulta con nombre y portable). Si el dueño
quiere un grupo con nombre propio y sin dueño, `ViewDoc` es ese documento.

Decisión del dueño: PENDIENTE (adoptado / rechazado)

### 3.5 Composición

**Qué propone.** La operación que baja de la KB gráfica al Markdown compuesto (§16:
«composición ⟶ / ⟵ indexación», `PROPUESTA-SUPERFICIE.md:516-517`, `:534-536`) como modelo del set.

**Qué existe hoy.** La composición es un **atributo del contrato**, no un documento:

- `__compositions__` (`src/sldb/models/structured_doc.py:12`), renderizado en
  `render_payload`/`compose_field` (`:27-40`), por documento o por field (`ref: field`, `:38-39`);
  declarado y validado con el resto del contrato (`docs/architecture/model-authoring.md:13`,
  `:31-32`, `:60-61`).
- Llega al grafo: una arista `composes` por ref (`src/sldb/store/edge_index/composition_edges.py:1-28`).
- **H1 ya está en parte:** el render instrumentado guarda de qué documento salió cada pedazo
  (`src/sldb/models/structured_doc.py:95-102`), y `CompositionPiece.source` lo expone en los
  segmentos (`src/sldb/api/segments/composition_piece.py:15-30`, SV03), con `editable: false`
  porque un pedazo se edita en su fuente (`:25`). §16.2 lo daba por faltante; hoy lo que falta
  es el camino de vuelta (editar el pedazo y bajarlo al hijo), no el mapa.
- Decisión vigente: composición determinista por listas explícitas (`PROPUESTA-SUPERFICIE.md:616-626`).

**Ejemplo.** `BoardDoc:Board` (`desk/tasks/Board.md`). `task_summaries` compone los TaskDoc de
`tasks` con la plantilla `- {title} [{status}] - {goal}` (`deskops/deskops/models/board.py:9-15`)
en la sección «Task Details» (`:45-49`). Es la única composición en uso en el store de sldb.

**Recomendación del redactor: adoptar con cambios.** Adoptar la composición como parte del set,
pero **como sección del Modelo (3.7)**, no como un modelo aparte: una composición no tiene vida
propia, es lo que un contrato dice de uno de sus fields. Si el dueño adopta 3.7, el
`ModelDoc` lleva sus composiciones; si no, `__compositions__` sigue siendo la forma y no hace
falta nada nuevo.

Decisión del dueño: PENDIENTE (adoptado / rechazado)

### 3.6 Publicación

**Qué propone.** La nota solo da el nombre. Interpretación del redactor: el último tramo de
§16, del Markdown compuesto al «TEXTO» que lee una persona (`PROPUESTA-SUPERFICIE.md:524-525`),
como documento: qué se publica, desde qué átomos, dónde.

**Qué existe hoy.**

- **En sldb, el mecanismo:** render y compose (`sldb docs compose` expande transclusiones),
  vistas de proyección `ViewDoc` (`src/sldb/models/notation/view_doc.py:11-50`,
  `docs/architecture/notations-and-views.md` §2 y §5) y la autoridad `generated` para lo
  producido (`docs/architecture/provenance.md:45`).
- **En deskops, el contrato de publicación ya existe:** `MaterializationContractDoc`
  (`deskops/deskops/models/materialization.py:8-60`) con `source_atoms` (`:37-40`),
  `target_kind`, `target_identity` y `validation`; y el átomo de deskops
  `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md` («los docs son
  materializaciones de átomos para humanos»). El store de sldb trackea 135 de estos contratos.
- `source_atoms` es `list[str]` sin `__doc_anchors__`: la publicación no sabe si sus átomos
  cambiaron.

**Ejemplo.** `MaterializationContractDoc:materialization-gd23-architecture-selectors`
(`desk/materializations/materialization-gd23-architecture-selectors.md`): publica
`atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error` en
`docs/architecture/selectors.md`, con `target_kind: doc` y un comando de validación. Es una
Publicación en todo menos en el nombre.

**Recomendación del redactor: no adoptar** como modelo de sldb. Qué es una publicación, qué
cuenta como validada y a quién se dirige es política de un consumidor (G_BOUNDARY), y deskops ya
tiene el modelo. sldb pone el mecanismo (render, compose, `ViewDoc`, anclas). Mejora sugerida,
fuera de este set y del lado de deskops: declarar `source_atoms` en `__doc_anchors__`, para que
una `RuleDoc` diga «toda materialización con un átomo `changed` está atrasada».

Decisión del dueño: PENDIENTE (adoptado / rechazado)

### 3.7 Modelo

**Qué propone.** «El contrato como documento, salida de la espiral; hoy no existe». La espiral
termina en «MODELO» (`PROPUESTA-SUPERFICIE.md:544-546`) y «el modelo no se escribe: se destila»
(`:553-555`).

**Qué existe hoy.**

- **El contrato es una clase Python.** Su identidad es `model_ref` (`module:Class`), no un
  archivo (átomo `…-model-ref-es-la-identidad`); su resolución está en
  `src/sldb/api/model_registry/model_reference.py:67`.
- **Lo que el store guarda es una copia derivada,** no un documento: `ModelsIndex`
  (`src/sldb/store/models/models_index.py:4-21`: hashes, `family`, `base_models`), releída de la
  clase cada vez que el store firma (átomo `…-se-relee-cada-vez-que-el-store-firma-el-modelo`);
  y su firma, `contract_signature` (`src/sldb/store/model_contract.py:89-101`).
- **El grafo ya tiene el modelo como nodo** y cada field como nodo hijo
  (`src/sldb/store/edge_index/model_contribution.py:46-56`; tipos `has_field`, `extends`,
  `has_document` en `sldb/relation_types/`).
- **Hay una declaración del contrato como datos, pero efímera:** `create_model` recibe
  `[{name, type, description, required?, default?, enum?}]` y containment, references,
  compositions, semantics y authority (`src/sldb/api/model_create/create_model.py:21-35`,
  validación en `src/sldb/api/model_create/model_declaration.py:11-27`), genera el módulo y lo
  registra; los cambios van por drafts `.py.temp` con validación y backfill
  (`src/sldb/api/model_drafts/model_draft.py:10-14`,
  `src/sldb/api/model_drafts/draft_validation.py:21-58`). Esa declaración no queda trackeada.
- **Lo que un documento no puede llevar:** los validadores pydantic. Por el principio del dueño,
  las invariantes de un documento **son** código del modelo; un `ModelDoc` puede declarar
  fields, plantilla, referencias, composiciones y semántica, pero no un `model_validator`.

**Ejemplo.** `AtomicDocumentDoc:atom-structurednldoc-model` (`docs/atoms/structurednldoc-model.atom.md`).
Explica qué es un modelo y en su sección «Where It Lives» dice: «It lives in Python code». Es la
descripción en prosa, mantenida a mano y aparte, de algo que la propuesta quiere que sea un
documento con contrato.

**Recomendación del redactor: adoptar con cambios.** Un `ModelDoc` como **salida de la
espiral, no como fuente de autoridad**: guarda la declaración que hoy recibe `create_model`
(fields, plantilla, containment, references, compositions, semantics) más un `from:` con las
anclas a las fuentes y átomos que justifican cada field (lo que hace auditable la
destilación, `PROPUESTA-SUPERFICIE.md:553-555`), y `create_model` lo consume para generar la
clase. Una vez generada, la clase sigue siendo el contrato (porque es la única que puede llevar
los validadores) y el `ModelDoc` queda como su procedencia, con autoridad `theorem`
(`docs/architecture/provenance.md:44`): si la clase cambia sin que cambie su `from:`, es una
alerta `verify`. Hacer del `ModelDoc` la fuente de verdad partiría el contrato en dos (datos en
el documento, validadores en Python), y eso no lo recomiendo.

Decisión del dueño: PENDIENTE (adoptado / rechazado)

### 3.8 La regla átomo/field

**Qué propone.** «Un átomo nunca lleva posición, un field nunca lleva ancla; se conectan por
procedencia (H1) y por promoción».

**Qué existe hoy.**

- **La identidad de un field es su posición en el contrato:** el dueño de un field es la sección
  del template que lo contiene (átomo `…-el-dueño-de-un-field-es-la-sección-del-template…`), y
  en el grafo un field es `field_node_id(modelo, nombre)`
  (`src/sldb/store/edge_index/model_contribution.py:51-56`). Esta mitad de la regla ya se cumple.
- **Contradicción literal:** desde GO07 un field **sí puede llevar un ancla como valor**
  (`__doc_anchors__`, `src/sldb/models/structured_doc.py:15`; forma en
  `src/sldb/models/doc_anchor_value.py:51-56`), y `Provenance.from_` las lleva en el bloque
  `sldb` (`src/sldb/models/provenance.py:28`). Lo que la regla quiere decir, según la nota, es
  que la **identidad** de un field no sale de un ancla, no que un field no pueda guardar una.
- **El átomo, como documento, sí tiene fields con posición:** `AtomDoc.answer` es un field de
  su propio modelo (`deskops/deskops/models/atom.py:43-45`, `:60-65`). Lo que no tiene es
  posición **en otro contrato**: cuando un padre lo compone, la posición es del padre (su lista
  de refs), no del átomo.
- **Procedencia (H1):** está, en la vía de lectura (`CompositionPiece.source`,
  `src/sldb/api/segments/composition_piece.py:27`; ver 3.5).
- **Promoción:** existe a nivel de documento en deskops: `type_protoatom` convierte un
  protoatom en un documento de un modelo tipado (su contenido va a un `content_field`) y deja
  un stub con `typed_as: Model:id` (`deskops/deskops/domain_tree.py:142-168`;
  `deskops/deskops/models/protoatom.py:44-47`). No existe la promoción de átomo a **field de un
  contrato** que describe la espiral (varios átomos con el mismo `kind` pasan a ser un field).

**Ejemplo.** `AtomDoc:atom-el-dueño-de-un-field-es-la-sección-del-template-que-lo-contiene-no-la-línea-donde-quedó-renderizado`
(`desk/atoms/…`). Ilustra las dos mitades a la vez: como átomo, su identidad es lo que lo
respalda (`provenance: tests/test_field_ownership.py`, escrita como texto libre, sin estado),
y su contenido dice que la identidad de un field es su posición estructural en el template.

**Recomendación del redactor: adoptar con cambios.** Reformular así: «la **identidad** de un
átomo es su procedencia (anclas pinneadas, con estado); la **identidad** de un field es su
posición en un contrato (`Modelo.field`, su sección del template). Un field puede **guardar**
un ancla como valor (`__doc_anchors__`), pero no se identifica por ella; un átomo no ocupa
posición en otro contrato: si se compone, la posición es de la lista del padre. Se conectan
por procedencia (H1: cada pedazo compuesto sabe de qué átomo viene) y por promoción (un átomo
tipado pasa a ser un documento de un modelo, `typed_as`; la promoción a field de un contrato
es la que falta)». Así formulada, la regla es una invariante entre documentos
(`RuleDoc`), no de un documento, salvo la forma del ancla, que ya es validador.

Decisión del dueño: PENDIENTE (adoptado / rechazado)

### 3.9 La pregunta abierta: ¿sobre el set se modela el dominio o SLDB mismo?

**Qué propone.** Decidir si lo que se modela encima del set es el dominio de cada caso
(Levira, MEPU) o SLDB mismo (`desk/`, pills, requests, `docs/models.py`).

**Qué existe hoy.**

- El store de sldb **ya modela a SLDB mismo**: modelos locales en `docs/models.py`
  (`ArchitectureNarrativeDoc`, `PlanDoc`, `RequestDoc`, …) y `desk/models.py`
  (`DeskSpecDoc`, `desk/models.py:41`; `DeskStandardsDoc`, `:8`), más los heredados de deskops
  (`AtomDoc`, `PillDoc`, `TaskDoc` y sus tipos, `MaterializationContractDoc`) y de pron
  (`AnchorDoc`, `MoveDoc`). Hay documentos reales de casi todos.
- **G_BOUNDARY** reparte: sldb evalúa, los consumidores autoran
  (`desk/drawer/plans/grafo-operable/dag.yaml:15-20`). El dominio de un caso es por definición
  de un consumidor.
- No hay en el workspace repos ni stores de Levira ni de MEPU (supuesto en §6).

**Ejemplo.** `DeskSpecDoc:desk-spec` (`desk/SPEC.md`). Es SLDB modelándose a sí mismo con un
modelo local (`desk/models.py:41`): la especificación de su propio desk, con secciones fijas
que ya son fields. Es el corpus donde una vuelta de la espiral se puede verificar hoy con
documentos reales.

**Recomendación del redactor: adoptar con cambios** la respuesta «**SLDB mismo primero**, y el
dominio después, en el repo de cada consumidor». Razones: (1) es el único corpus con documentos
reales trackeados donde probar que el set alcanza (los ejemplos de este documento salen todos de
ahí); (2) el set (3.1, 3.2, 3.7) es infraestructura genérica de sldb, y los modelos de dominio
de Levira o MEPU los autoran sus consumidores encima, como dice G_BOUNDARY; (3) no hay material
de esos dominios en el workspace para fundar una decisión sobre ellos. No es una exclusión: es
un orden.

Decisión del dueño: PENDIENTE (adoptado / rechazado)

## 4. Tabla resumen

| # | Punto | Recomendación del redactor | Ejemplo | Decisión del dueño |
| --- | --- | --- | --- | --- |
| 3.1 | Fuente | adoptar con cambios: rol `source_raw` + un `SourceDoc` genérico mínimo | `RequestDoc:req-ontology-feature-request` | PENDIENTE |
| 3.2 | Átomo | adoptar con cambios: la procedencia como raíz abstracta (`GroundedDoc`), no un átomo con semántica | `AtomDoc:atom-sldb-evaluates-declared-rules-consumers-author-them` | PENDIENTE |
| 3.3 | Relación + TipoDeRelación | adoptar (ya existen `RelationDoc` y `RelationTypeDoc`) | `RelationDoc:execution-task_activates`, `RelationTypeDoc:type-task_activates` | PENDIENTE |
| 3.4 | Grupo | no adoptar: lo cubren containment, tags y `ViewDoc` | `BoardDoc:Board` (`pills`) | PENDIENTE |
| 3.5 | Composición | adoptar con cambios: como sección del Modelo, no modelo aparte | `BoardDoc:Board` (`task_summaries`) | PENDIENTE |
| 3.6 | Publicación | no adoptar en sldb: es de deskops (`MaterializationContractDoc`) | `MaterializationContractDoc:materialization-gd23-architecture-selectors` | PENDIENTE |
| 3.7 | Modelo | adoptar con cambios: `ModelDoc` como salida y procedencia del contrato, no como su autoridad | `AtomicDocumentDoc:atom-structurednldoc-model` | PENDIENTE |
| 3.8 | Regla átomo/field | adoptar con cambios: reformulada sobre identidad, no sobre lo que un field guarda | `AtomDoc:atom-el-dueño-de-un-field-es-la-sección-del-template-que-lo-contiene-no-la-línea-donde-quedó-renderizado` | PENDIENTE |
| 3.9 | Pregunta abierta | SLDB mismo primero; el dominio después, en cada consumidor | `DeskSpecDoc:desk-spec` | PENDIENTE |

## 5. Qué cambiaría si se adopta todo

Descripción, no implementación; nada de esto se hace en esta tarea. «Todo» es la propuesta
original de siete modelos más la regla, no las recomendaciones de arriba; donde difieren se
dice.

- **sldb gana seis modelos builtin nuevos** (Fuente, Átomo, Grupo, Composición, Publicación y
  Modelo; Relación y TipoDeRelación ya existen). Cada uno se
  registraría en cada store que los use y cada uno con su `__template__`, como `RuleDoc` o
  `ViewDoc` hoy.
- **Átomo en sldb** obligaría a decidir la relación con `AtomDoc`/`ProtoAtomDoc` de deskops:
  que hereden del builtin (migración con `models update`, cambio de `base_models` y de su
  hash de contrato, backfill si se agregan campos obligatorios, como describe el documento
  hermano para `RunDoc`) o que convivan dos «átomos». Los 35 `AtomDoc` del store de sldb y los
  de deskops entrarían en la familia.
- **Grupo y Publicación** duplicarían containment/tags/`ViewDoc` y `MaterializationContractDoc`;
  habría que retirar uno de cada par o documentar cuándo usar cuál.
- **Composición como modelo** sacaría `__compositions__` de la clase o lo duplicaría; el
  renderer (`src/sldb/models/structured_doc.py:27-40`) y las aristas `composes` tendrían que
  leer un documento además de la clase.
- **Modelo como documento** es el cambio grande: `create_model` y los drafts de SV04 pasarían a
  leer y escribir un `ModelDoc` trackeado; `models add` y la firma del store
  (`stamp_model_node`) tendrían que conciliar clase y documento; los validadores seguirían en
  Python. Si el `ModelDoc` fuera la autoridad (la lectura literal de la propuesta), el
  contrato quedaría partido en dos; con la recomendación de 3.7 queda como procedencia.
- **La regla átomo/field**, en su redacción literal, prohibiría `__doc_anchors__` (GO07) en
  todo field y habría que retirarlo o reescribir `ReviewDoc.subject` de deskops; reformulada
  (3.8), no cambia código: es una `RuleDoc` posible sobre la familia del Átomo.
- **El tramo que falta de la espiral** (anchors → regularidad → modelo, §16.2) seguiría sin
  existir: el set da dónde escribir cada paso, no la operación que detecta la regularidad ni la
  promoción de átomo a field. Esa operación sería la siguiente tarea de diseño.
- **Documentación:** un átomo por decisión adoptada en `desk/atoms/`, y `model-authoring.md`,
  `anchoring.md` y `provenance.md` reflejándolos.

## 6. Dudas y supuestos del redactor

- **Grupo y Publicación** no tienen definición en la nota; las interpretaciones de 3.4 y 3.6 son
  mías. Si el dueño las entendía de otro modo, la recomendación puede cambiar.
- **Levira y MEPU** no están en el workspace (`~/proyectos/SLDB_1`); 3.9 no puede citar nada
  suyo.
- **Ejemplos:** el store de sldb no trackea ningún `AnchorDoc`, `ProtoAtomDoc` ni `PlanDoc`
  (antes de este documento); por eso 3.1 y 3.2 usan `RequestDoc` y `AtomDoc` y no el ancla de
  pron. `BoardDoc:Board` se usa en 3.4 y 3.5 a propósito, porque un mismo documento muestra
  grupo y composición.
- **`sldb docs show`** acepta `Model/name` (no `Model:name`) como argumento; el export id que
  usa este documento es `Model:name`, como en el resto de sldb.
