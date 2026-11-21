---
sldb:
  by: agent
  at: '2026-11-21T06:53:09Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a-preflight-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a@sha256:fbc67d25acc16f76045da73692959a887f227baf767ebf47573c7038f39a5dda
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-065115/context-review/task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a/preflight/164e125349cadf3a03918372d85dec4fc0cc71086ee728c3de229354ce1fee31/attempt-1
input_sha256: 164e125349cadf3a03918372d85dec4fc0cc71086ee728c3de229354ce1fee31
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 645a0b1421b31be4296fb0a255a85fc19c02c4b318682b1ca5f0f9c39c439a53
output_sha256: 3f684b239c456c6f9c7d41a12de132bdae3de89eca18d6534199c2fc47bf085b
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones (origin/main): 1) docs/architecture/current-cli-tree.md
  tiene un solo bloque ```text (grep -c da 1); el chequeo lee ese y solo ese; si apareciera
  más de uno, es un hallazgo de error, no se elige. 2) Gramática del bloque: la raíz
  es la línea ''sldb'' (sin prefijo); cada nivel de indentación es el prefijo de árbol
  (├── / └── / │ más 4 columnas); una línea con varios nombres separados por '' /
  '' declara hermanos (p. ej. ''└── init / add / check'' bajo ''stores''); una línea
  ''template show / edit'' bajo ''models'' declara el grupo ''template'' con subcomandos
  show y edit; lo que va entre corchetes ([topic]) es argumento y se ignora. Profundidad
  la que tenga el parser (hay grupos anidados como models template). 3) Se excluye
  solo el subcomando ''help'' de los grupos que lo registran y los alias de argparse;
  -h/--help son flags y nunca cuentan como subcomandos. El ''help [topic]'' de primer
  nivel es un subcomando real de sldb y sí cuenta. 4) Solo cuenta el bloque de árbol;
  las menciones en prosa fuera del bloque no cuentan (precisión bundle-2 de la tarea).
  Commit en el worktree que dispatch le da al ejecutor con trailer ''Task-Id: task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a''
  en el cuerpo; la puerta identidad de tools/check.sh --fast falla por workbench_demo
  (excepción autorizada f055723d).'
# ISO 8601 timestamp
created_at: '2026-11-21T06:51:31.827857+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T06:52:34.720231+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-065115/context-review/task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a/preflight/164e125349cadf3a03918372d85dec4fc0cc71086ee728c3de229354ce1fee31/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones (origin/main): 1) docs/architecture/current-cli-tree.md tiene un solo bloque ```text (grep -c da 1); el chequeo lee ese y solo ese; si apareciera más de uno, es un hallazgo de error, no se elige. 2) Gramática del bloque: la raíz es la línea 'sldb' (sin prefijo); cada nivel de indentación es el prefijo de árbol (├── / └── / │ más 4 columnas); una línea con varios nombres separados por ' / ' declara hermanos (p. ej. '└── init / add / check' bajo 'stores'); una línea 'template show / edit' bajo 'models' declara el grupo 'template' con subcomandos show y edit; lo que va entre corchetes ([topic]) es argumento y se ignora. Profundidad la que tenga el parser (hay grupos anidados como models template). 3) Se excluye solo el subcomando 'help' de los grupos que lo registran y los alias de argparse; -h/--help son flags y nunca cuentan como subcomandos. El 'help [topic]' de primer nivel es un subcomando real de sldb y sí cuenta. 4) Solo cuenta el bloque de árbol; las menciones en prosa fuera del bloque no cuentan (precisión bundle-2 de la tarea). Commit en el worktree que dispatch le da al ejecutor con trailer 'Task-Id: task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a' en el cuerpo; la puerta identidad de tools/check.sh --fast falla por workbench_demo (excepción autorizada f055723d).
