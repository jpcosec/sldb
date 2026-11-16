---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: mepu
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-14T01:57:06'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:26:28'
---

# Dos instalaciones de sldb en robocop, una editable sobre el checkout principal con cambios ajenos; la versión dice 0.1.13 con 283 commits encima

_Describe the incoming message with enough evidence to triage._

Escrita a mano desde mepu (14-11) por pedido de JP. JP ya pidió dejar una sola instalación; esta nota es para el lado de sldb.

- **Qué había:**
  - El comando `sldb` (uv tool `structuredlanguagedb`) estaba instalado en modo editable sobre `/mnt/ssd/proyectos/SLDB_1/sldb`, el checkout principal. Ese checkout tiene `uv.lock` modificado y archivos sueltos de otras sesiones (`desk/runtimes/`, `runs/subagents/2026110*`, `.herdr-coordination.md`): lo que corre depende de lo que haya sin commitear ahí.
  - `deskops` usaba otro sldb, editable sobre `~/herramientas/sldb` (worktree desprendido).
  - Los dos estaban en `b965c62d` solo porque se alinearon a mano el 13-11.
- **Versión.** Las dos dicen `0.1.13`, pero `git describe` da `v0.1.13-283-gb965c62d`. Ningún comando dice qué commit corre, y el release 0.1.13 está pendiente («hasta que la suite completa esté verde»; el CI de main está rojo desde el 20-10, tarea abierta).
- **Además, el desk de sldb está roto.**
  - `deskops doctor` da `Errors`: el ReviewDoc `desk/reviews/task-stores-build-un-store-enlazado-ausente-es-alerta-no-error-build-check-en-ci/preflight-1.md` no calza con lo indexado.
  - Hay revisiones que apuntan a tareas que ya no existen: `task-gd26` y `task-go05-lenguaje-de-predicados-unificado`.
- **Pregunta.** ¿Cuál es la instalación de referencia de sldb para los consumidores (deskops, mepu)? ¿Un runtime fijado (worktree o versión publicada) en vez del checkout de trabajo? ¿Y `sldb --version` debería mostrar el commit?
