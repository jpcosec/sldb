---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-11T08:01:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# SEGURIDAD: live_stale lee todos los archivos trackeados y sigue symlinks fuera de la raíz al cargar el índice de aristas

_Describe the incoming message with enough evidence to triage._

Hallado por la integración de graph_ui (wt/deskops-ui, test_mindmap_workspace_reader), 2026-11-11, sldb 84eb7f75, introducido por GO04 d7eefdeb. live_stale._file_hash abre y hashea CADA archivo trackeado del store en cuanto un proceso nuevo llama load_edge_index; en el desk de prueba abrió las 28 md. Lee archivos que el consumidor tiene marcados como protegidos y sigue un symlink que escapa de la raíz (secreto-externo.md) antes de que el consumidor pueda aplicar sus guardas. Rompe la garantía de graph_ui de 'no abrir lo no autorizado', y graph_ui no lo puede evitar sin dejar de usar load_edge_index. Esperado: live_stale no sigue symlinks ni lee rutas que resuelvan fuera de la raíz del store (comprobar con resolve + is_relative_to antes de abrir); mejor aún, el chequeo de frescura usa stat (mtime/size) y solo hashea cuando cambió, o es perezoso por documento. Hasta el arreglo, test_mindmap_workspace_reader de graph_ui queda rojo con esta causa (sin skip ni xfail).
