---
sldb:
  by: agent
  at: '2026-11-17T11:20:46Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T08:07:24'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T08:20:18'
---

# project_graph de deskops: destinos de H1 que DeclaredFileTargets no puede declarar y closed: sin cuerpo (H2)

_Describe the incoming message with enough evidence to triage._

deskops (tarea task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y) migro H2 de CC33c: la superficie issue usa closed: y closed_document ya no se usa. H1 no se puede migrar: deskops ya declara DeclaredFileTargets(directory=desk/materializations, field=target_identity), pero los destinos existentes que hoy filtra deskops/graph/checks.py:declared_target_is_a_file no salen de un campo escalar de frontmatter fuera de las exclusiones. Casos (49 faltantes en graph missing de deskops, sin cambios): (1) campo lista: references: de desk/tasks/*.md nombra notas desk/inbox/*.md existentes (unas 28 tareas, p.ej. desk/tasks/task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y.md -> desk/inbox/20261116-012942-...md); DeclaredFileTargets solo lee un valor str (declared_target_nodes.py:_field_value). (2) mencion en el cuerpo (LineMentions locator source-file-reference): tests/e2e_agent/scenarios/inbox-to-task.yaml desde desk/tasks/task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li.md lineas 20/38/50; tests/fixtures/model_contract_hashes.json desde la tarea de arriba lineas 45/51; desk/drawer/plans/<plan>/dag.yaml en tareas del drawer. (3) destino excluido: target_identity de desk/materializations bajo tests/fixtures (tests/fixtures/model_contract_hashes.json, tests/fixtures/golden/help/*.txt, tests/fixtures/golden/scaffold/update.json); DeclaredTargetNodes los descarta por FileExclusions aunque el campo los declara. Pedido: una forma declarativa de que un destino de referencia (de cualquier ReferenceField/LineMentions/campo lista) que es archivo existente del proyecto no cuente como faltante, o que DeclaredFileTargets acepte listas y no aplique exclusiones a lo declarado. Ademas, sobre H2: closed: solo ve el payload (frontmatter); los issues de deskops (sin modelo, desk/drawer/issues) admiten el estado tambien en una seccion ## Status o una linea Status: del cuerpo, que el predicado no alcanza; deskops acepto esa perdida (no hay issues en ningun desk hoy).
