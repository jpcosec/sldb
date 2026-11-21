---
sldb:
  by: agent
  at: '2026-11-21T06:31:43Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-21T03:25:15'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:31:19'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en tarea task-respaldar-562847e2-surface-asistente-tour-y-workbench-demo-con-la-suite-completa-y-sldb-stores-build
  (suite completa + stores build --check + ignorar .herdr-coordination.md). workbench_demo
  versionado: ya cubierto por task-clasificar-workbench-demo-en-contracts-identity-toml-producto-autoaplicacion-o-ajeno-la-puerta-ident.
  .gitattributes manual de 830dfe08: cubierto por task-el-merge-driver-de-sldb-se-instala-solo-en-un-clon-que-tiene-las-lineas-de-gitattributes-pero-no-la.'
---

# Trabajo de surface (562847e2) entró a main sin tarea ni suite completa; .gitattributes y .herdr-coordination.md

_Describe the incoming message with enough evidence to triage._

Sesión local de JP, 2026-11-20. El commit 562847e2 (feat(surface): AssistantDock, TourOverlay, WorkbenchAssist, surface/assistant/vite-plugin.ts, DESIGN.md, PRODUCT.md y el store workbench_demo/, 4,3 MB) entró directo a main sin tarea del desk. Se verificó solo con tsc, vitest de surface (407 pruebas) y tools/check.sh --fast; no se corrió la suite completa de sldb ni sldb stores build --check. Pedido: una tarea que lo respalde con la suite completa y stores build --check, y que decida si workbench_demo/ se queda versionado. Aparte: (1) 830dfe08 agregó .gitattributes (merge driver) instalado a mano con sldb stores merge-driver --install, adelantándose a la tarea del auto-install; (2) .herdr-coordination.md sigue sin trackear y sin ignorar en este repo y en el checkout local.
