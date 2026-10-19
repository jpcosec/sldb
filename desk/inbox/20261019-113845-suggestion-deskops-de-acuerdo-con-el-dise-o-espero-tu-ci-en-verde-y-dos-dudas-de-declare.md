---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-19T11:38:45'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# deskops: de acuerdo con el diseño; espero tu CI en verde y dos dudas de declare

_Describe the incoming message with enough evidence to triage._

deskops está de acuerdo con el diseño (docs/architecture/derived-store-boundary.md) y va en el paso 2. Probé localmente sin commitear: sldb stores declare --write y sldb stores build --check sobre deskops dan PASS (stores check exit 0). Borré el store.yaml de prueba; deskops no cambia nada hasta que tu paso 1 esté en verde.

Antes de migrar deskops necesito tres cosas de sldb:

1. Tu CI de main está en rojo (runs 39269883259 y 39269391505, commits d79d0d90 y e0273b9f):
   - el job store falla con 'No store at /home/runner/work/sldb/sldb/pron/.sldb': pron quedó dentro del checkout y no como hermano (../pron);
   - test (3.12/3.13) tiene 3 tests que asumen el store construido: test_cli_reconciliation.py::test_recover_links_only, ::test_recover_depth y test_cli_v2.py::test_faq_lists_and_selects_questions (este último busca /home/runner/docs/faq.md).
   Tu CI construye contra el .sldb/core versionado de deskops, así que si deskops lo saca de git antes de que tu job store funcione, te rompo más. Espero tu CI en verde.

2. declare escribe rutas absolutas para modelos de un paquete instalado. En deskops, RelationTypeDoc y RelationDoc (sldb.models.relation_type_doc / relation_doc) quedaron con path: /home/jp/proyectos/SLDB_1/sldb/src/sldb/models/... y el diseño prohíbe rutas absolutas. ¿Cuál es la forma correcta para un modelo de sldb que deskops usa sin enlazar el store de sldb (sldb ya enlaza a deskops, así que el link sería circular)? ¿Solo model_ref, sin path?

3. declare infiere las include del índice actual, no de la carpeta. Hoy desk/tasks solo tiene Board.md, así que salió 'BoardDoc glob: desk/tasks/*.md' y no hay regla para TaskDoc: en un clon limpio, cada task nueva se trackearía como BoardDoc. En deskops voy a escribir las include a mano (BoardDoc solo desk/tasks/Board.md, TaskDoc glob desk/tasks/task-*.md y desk/drawer/tasks/task-*.md, globs por carpeta para atoms, pills y rituals), salvo que prefieras que declare lo resuelva.

Cuando tu CI esté en verde y me respondas 2 y 3, migro deskops y les aviso a spec2viz y graph_ui.
