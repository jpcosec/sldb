---
# unclear | suggestion
kind: suggestion
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
acknowledged_at: '2026-11-16T05:27:12'
---

# El registro del ecosistema guarda rutas absolutas de una máquina: en otra no resuelve nada

_Describe the incoming message with enough evidence to triage._

Escrita a mano desde mepu (14-11) por pedido de JP.

- **Qué.** Las seis entradas de `desk/registry/` (`repo-deskops`, `repo-graph_ui`, `repo-pron`, `repo-scion`, `repo-sldb`, `repo-spec2viz`) guardan `path: /home/jp/proyectos/SLDB_1/...`. En robocop el checkout está en `/mnt/ssd/proyectos/SLDB_1/` y ninguna resuelve.
- **Efectos vistos:**
  - `deskops message send --to sldb` desde mepu falla: «Current repository root '/mnt/ssd/proyectos/SLDB_1/sldb' is not registered», aunque `repo-sldb.md` existe.
  - mepu arrastra la alerta `the linked store is missing: /home/jp/proyectos/SLDB_1/deskops/.sldb` en cada `deskops doctor`.
  - Registrar desde robocop con `deskops repo register` deja el error al revés: guarda `/mnt/ssd/...`, que se rompe en la laptop. Por eso no se registró nada.
- **Relacionadas, sin resolver:** «stores check en verde sobre un store que no se construyó (enlaces entre stores no portables)» (20-10) y «sldb stores add guarda siempre el enlace relativo; no resuelve desde worktrees un nivel más hondo».
- **Propuesta.** Rutas relativas a la raíz del ecosistema, o una resolución por máquina (variable o archivo local no versionado). Que `doctor` nombre la ruta que no resuelve como hallazgo del registro, no como store ausente.
