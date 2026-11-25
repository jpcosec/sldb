FILE:desk/tasks/task-on-write-save-document-payload-devuelve-las-alertas-de-la-escritura-y-la-regla-ve-las-aristas-que-el.md
---
sldb:
  by: agent
  at: '2026-11-16T05:35:24Z'
  authority: generated
  via: save_document_payload
id: task-on-write-save-document-payload-devuelve-las-alertas-de-la-escritura-y-la-regla-ve-las-aristas-que-el
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/api/rules/rules_on_write.py
- src/sldb/api/rules/rule_graph.py
- src/sldb/api/documents/payload_save.py
- src/sldb/core/finding_route.py
- tests/api/test_rules.py
- tests/api/test_on_write_entering.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-evaluates-declared-rules-consumers-author-them
from_drawer: desk/drawer/tasks/task-on-write-alerts-sin-listener-se-pierden-por-la-api-y-la-regla-ve-las-aristas-previas-a-la-escritura.md
---

# on_write: save_document_payload devuelve las alertas de la escritura y la regla ve las aristas que el payload nuevo declara

## Rationale

_Explain why this task exists or the business driver behind it._

Hallazgos de GO08 (H2, H3). (1) Las alertas de on_write viajan por sldb.core.finding_route (route en src/sldb/core/finding_route.py:24-27 no hace nada sin listener) y solo la CLI instala alert_sink: un programa que usa sldb.api sin instalar listener no las recibe; check_on_write (src/sldb/api/rules/rules_on_write.py:30-42) solo las manda por route y save_document_payload (src/sldb/api/documents/payload_save.py:15) devuelve un DocumentReference sin findings. La tarea task-apply-batch-aristas-validadas-antes-de-escribir-alertas-on-write-en-batchreport-rules-check-sobre-re cubre esto solo para apply_batch (BatchReport.alerts), no para guardar un documento. (2) RuleGraph.with_payload (src/sldb/api/rules/rule_graph.py:62-64) deja el modelo y las aristas del índice, así que una regla on_write ve las aristas de antes de la escritura. Origen: drawer desk/drawer/tasks/task-on-write-alerts-sin-listener-se-pierden-por-la-api-y-la-regla-ve-las-aristas-previas-a-la-escritura.md.

## Goal

_Describe the concrete result this task must produce._

save_document_payload devuelve en el DocumentReference un campo alerts: list[dict] con las alertas on_write de esa escritura (además de enviarlas por route como hoy), y una regla on_write cuya condición depende de una arista declarada por el payload nuevo la ve al evaluarse.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) check_on_write devuelve la lista de findings de nivel alert que emitió; save_document_payload la pone en un campo nuevo alerts del DocumentReference (opcional, lista vacía por defecto, para no romper a quien lo construye); route sigue recibiéndolas. (2) En RuleGraph.with_payload, construir las aristas salientes declaradas (__references__ y __doc_anchors__) del documento a partir del payload nuevo y reemplazar con ellas las del documento en el grafo que evalúa la regla; las demás aristas quedan como están. Tests en tests/api/test_rules.py (una regla on_write de nivel alert: save_document_payload la devuelve en alerts sin listener instalado) y tests/api/test_on_write_entering.py (una regla que exige una arista references: guardar un payload que la agrega pasa; uno que la quita da el finding). CHANGELOG.md. No entra: BatchReport.alerts de apply_batch (otra tarea), cambiar el nivel de las reglas existentes.

Precisiones (preflight-1): cada alerta es Finding.as_dict() (el mismo dict que devuelve rules_check), solo las de nivel alert; DocumentReference.alerts: list[dict[str, Any]] = Field(default_factory=list). Las aristas del payload nuevo se construyen con la misma función que usa el índice para un documento (declared_reference_edges de src/sldb/store/edge_index/declared_references.py y doc_anchor_edges de doc_anchor_edges.py) aplicada al payload nuevo; with_payload devuelve un RuleGraph nuevo (no muta el del índice) con las aristas salientes de ese documento reemplazadas. Test de alerta: una RuleDoc on_write de nivel alert con condición falsa para el payload; sin listener se asegura con monkeypatch sobre la lista de listeners de finding_route. Test de aristas: RuleDoc on_write de nivel error con condición "exists(references)" o equivalente en el lenguaje de reglas; guardar con la referencia pasa; quitarla da el finding con ese code.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer finding_route.py, rules_on_write.py, rule_graph.py (with_payload) y payload_save.py, más la clase DocumentReference (grep -rn "class DocumentReference" src/sldb). 2) Devolver findings desde check_on_write. 3) Agregar alerts a DocumentReference. 4) Aristas del payload nuevo en with_payload. 5) Tests y CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_rules.py
- TMPDIR=/dev/shm pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rules_evaluation.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan con los tests nuevos; DocumentReference.alerts existe y viene vacía cuando no hay reglas; CHANGELOG y commit; aviso a deskops con deskops message send --to deskops.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-on-write-save-document-payload-devuelve-las-alertas-de-la-escritura-y-la-regla-ve-las-aristas-que-el: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

