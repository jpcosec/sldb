FILE:desk/tasks/task-go07-anclas-a-documentos-con-hash-de-contrato.md
---
id: task-go07-anclas-a-documentos-con-hash-de-contrato
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/models/structured_doc.py
- src/sldb/models/doc_anchor_value.py
- src/sldb/models/provenance.py
- src/sldb/store/model_contract.py
- src/sldb/store/edge_index/doc_contribution.py
- src/sldb/store/edge_index/compose.py
- src/sldb/store/edge_index/payload_projection.py
- src/sldb/api/documents/payload_save_steps.py
- src/sldb/api/anchors/__init__.py
- src/sldb/api/anchors/check_doc_anchors.py
- src/sldb/api/__init__.py
- src/sldb/cli/commands/anchors.py
- docs/architecture/anchoring.md
- CHANGELOG.md
- tests/api/test_doc_anchors.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# GO07: Anclas a documentos con hash de contrato

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO07 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK03. Hoy solo hay anclas de codigo (CodeAnchorDoc); Provenance.from_ acepta doc:<Model:name> pero el verify disenado nunca se implemento (alcance.md). GO07 agrega anclas a documentos pinneadas con el hash de contrato de GO02 y expone su estado al lenguaje de GO05 (alias anchor_state) sin tocar el shard de GO04.

## Goal

_Describe the concrete result this task must produce._

Campos __doc_anchors__ y from: de Provenance con la forma doc:Model:name@sha256:<hash>, validados al escribir y pinneados en el guardado; estados intact/changed/lost; check_doc_anchors(store) -> list[Finding] usado por anchors check; aristas references desde los campos __doc_anchors__; entrada derivada <campo>__anchor_state en la facet payload calculada al leer; docs/architecture/anchoring.md y CHANGELOG.

## Scope

_State what is in scope and what is out of scope._

En alcance: el atributo __doc_anchors__ y su validacion en los modelos, Provenance.from_, el pinneado en payload_save_steps, las aristas references de los campos __doc_anchors__, la entrada derivada <campo>__anchor_state al componer o leer la proyeccion, check_doc_anchors y el comando anchors check, docs/architecture/anchoring.md, CHANGELOG.md, tests. Fuera: el cableado en stores check y la evaluacion incremental (GO08), cambios al lenguaje (GO05 ya define el alias anchor_state), cambios al formato del shard o a EDGE_INDEX_VERSION, reconnected para documentos.

PRINCIPIO DEL DUENO (2026-11-05): invariantes de UN documento = validadores pydantic del modelo; entre documentos = RuleDoc; los tests solo prueban rechazo. Aplicado aqui: (q1) la forma de un valor en un campo __doc_anchors__ y en from: (vacio/null o doc:Model:name[@sha256:<64 hex>]) es un validador pydantic (en el modelo base para los campos que el modelo declara en __doc_anchors__, y en Provenance para from:): escribir un valor malformado levanta el ValidationError del modelo con el campo y el motivo. Lo que depende de otro documento (que el destino exista, su hash actual, el estado intact/changed/lost) NO es validacion del modelo: es el pinneado al guardar y check_doc_anchors. Las invariantes de la definicion del modelo (__doc_anchors__ nombra campos str o list[str]; ningun campo termina en __anchor_state) se comprueban al cargar la definicion, como __indexed__ en GO04 (store/model_contract.py, SLDBModelError). (q2) Los tests de forma invalida prueban rechazo: texto no doc:, @sha256: vacio, hash que no es de 64 hex, tambien en from:; y la definicion de modelo invalida (campo no str/list[str], sufijo reservado).

HEREDADO: (h1) el hash de contrato es contract_hash(modelo, field_hashes) de src/sldb/store/graph/language/contract_hash.py (GO02 seccion 5, GO05 H12). (h2) El alias anchor_state ya existe en el lenguaje (GO05 p10): al atravesar el campo F lee F__anchor_state del payload del documento origen (lista alineada para list[str]); GO07 solo produce esa entrada. (h3) En el codigo actual Provenance.from_ es list[str] (alias from), no un escalar como dice el contrato: cada elemento que empieza por doc: es un ancla independiente; los que no (code:...) no se tocan. (h4) Los valores intact/changed/lost reutilizan el vocabulario de AnchorState (src/sldb/models/anchor_state.py) de las anclas de codigo; changed y lost son alertas.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO07 scope): Un ancla doc: es el valor de un campo: la forma doc:Model:name@sha256:<hash de contrato visto>. Los campos que llevan anclas son los que el modelo declara en el atributo de clase __doc_anchors__ (lista de nombres de campos de str o de list[str]) y el from: de Provenance, que pasa a admitir la forma con hash. Persistencia: en el propio documento, en el texto del campo; nada aparte. Pinneado: en los pasos de guardado de payload, un valor doc:Model:name sin @sha256 en un campo __doc_anchors__ o en from: se completa con el hash de contrato actual del destino (calculado como define GO02); si el destino no existe, se guarda sin hash. Estados: intact (hash igual), changed (hash distinto), lost (sin destino, o con destino pero sin hash); un ancla sin hash cuyo destino ya existe se pinnea en la siguiente escritura del documento que la contiene. GO07 expone check_doc_anchors(store) → list[Finding] y extiende el comando anchors check (src/sldb/cli/commands/anchors.py) para usarla; el cableado en stores check lo hace GO08 (dueño de api/stores); no hay reconnected para documentos. Severidad: changed y lost son alertas, nunca error, como las anclas de código. Un campo __doc_anchors__ solo admite vacío/null o valores con forma doc:Model:name[@sha256:<hash>]; otro texto es error de validación al escribir; <hash> son 64 caracteres hexadecimales y un @sha256: vacío o malformado es error, también en from:. from: de Provenance es escalar (str); un from: que no empieza por doc: (p. ej. code:) no es ancla de documento y este nodo no lo toca. Todo campo __doc_anchors__ se trata además como campo de __references__: genera aristas references con el nombre del campo, resolviendo doc:Model:name sin el sufijo @sha256; así ^subject existe en el grafo. El verify que provenance.md diseñó y nunca se implementó (alcance.md) es el mismo mecanismo aplicado a from:: Finding alert con code anchors/provenance_changed (destino con contrato distinto) o anchors/provenance_lost (sin destino o sin hash), emitido por anchors check por el canal de alertas; un from: sin hash se pinnea en la siguiente escritura igual que cualquier ancla. anchor_state se expone sin tocar el lenguaje ni el shard: al componer o leer la proyección, GO07 agrega a la facet payload, por cada campo __doc_anchors__, una entrada derivada <campo>__anchor_state (escalar para un campo str; lista alineada para list[str]) calculada en ese momento comparando el hash visto en el valor del campo con el hash de contrato actual del destino, que se calcula desde los field_hashes del destino ya presentes en el índice (GO04); no se persiste en el shard, así que editar el destino no exige invalidar al contenedor y EDGE_INDEX_VERSION no cambia; el sufijo __anchor_state queda reservado: un modelo que declare un campo con ese sufijo es error al cargar la definición del modelo. El lenguaje de GO05 la lee como cualquier campo y su alias genérico anchor_state (definido en GO05) la expone al atravesar el campo; ^subject es el recorrido inverso de las aristas references que el campo subject genera. Varias anclas en un campo lista = un estado por elemento. ACEPTACION: Un documento A con campo subject en __doc_anchors__ se guarda con doc:TaskDoc:b y queda pinneado con el hash de B; editar un campo del __contract__ de B deja el ancla changed; editar un campo fuera del contrato la deja intact; borrar B la deja lost; anchors check lo reporta como alertas (stores check lo hará vía GO08); con un modelo Review (campos subject en __doc_anchors__ y verdict) y una Task B como sujeto, la regla any(^subject: anchor_state = "intact" and verdict = "accepted") evalúa true cuando existe una Review con subject pinneado a B intacto y verdict accepted, y false sin Review, con verdict distinto o con el ancla changed; un valor no doc: en subject es rechazado al escribir; un documento con from: doc:B emite provenance_changed tras editar el contrato de B; docs/architecture/anchoring.md documenta __doc_anchors__, la forma con hash, el pinneado y la ausencia de reconnected; CHANGELOG. OUTPUT_SCOPE: src/sldb/api/anchors/, src/sldb/cli/commands/anchors.py, src/sldb/models/provenance.py, src/sldb/models/ (atributo __doc_anchors__ en el modelo base), src/sldb/api/documents/payload_save_steps.py (pinneado), src/sldb/store/edge_index/ (entrada derivada <campo>__anchor_state en la proyección), docs/architecture/anchoring.md, CHANGELOG.md REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 2: no cierra con tests rojos ni saltados; regla 3: spec, CLI con envelope JSON, pruebas, CHANGELOG y doc en docs/architecture; regla 5: nada se persiste del resultado de una regla (anchor_state se calcula al leer); regla 6: ante un contrato ausente registrar la hipotesis, no inventar API). Lenguaje: docs/architecture/rules-language.md; proyeccion y costura: docs/architecture/graph-backend.md; reglas: docs/architecture/rules.md (GO06).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest tests/api/test_doc_anchors.py sin fallos ni saltados
- A con subject en __doc_anchors__ guardado con doc:TaskDoc:b queda pinneado con el hash de B; editar un campo del __contract__ de B -> changed; editar fuera del contrato -> intact; borrar B -> lost; anchors check lo reporta como alertas
- modelo Review (subject en __doc_anchors__, verdict) y Task B: any(^subject: anchor_state = "intact" and verdict = "accepted") true con Review intacta y accepted; false sin Review, con verdict distinto o con el ancla changed
- valor no doc: en subject rechazado al escribir; un test de rechazo por forma invalida (tambien en from:) y por definicion de modelo invalida
- from: doc:B emite anchors/provenance_changed tras editar el contrato de B
- tests existentes de anclas de codigo, provenance, proyeccion (test_payload_projection) y lenguaje (test_predicate_language, spec GO02) sin cambios
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde y tools/check_layers.py PASS
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO07 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-go07-anclas-a-documentos-con-hash-de-contrato: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

