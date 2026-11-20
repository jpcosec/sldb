---
sldb:
  by: agent
  at: '2026-11-20T13:38:38Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskRefactorDoc:task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo@sha256:2ebf0fa7bd3dc6c9db37cad01e1b5a0c9bbdba85b5efd1f69edc2cfbeab4e9e9
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-133619/context-review/task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo/preflight/30276b8a216b7ebfc378104ce87a04a6f36b29e33fcf3a5d519d2f8d5936b571/attempt-1
input_sha256: 30276b8a216b7ebfc378104ce87a04a6f36b29e33fcf3a5d519d2f8d5936b571
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 62c25d494dee07a3571d3fce9ee6ebeb85d8117dbe7147571f9f762e02a62c70
output_sha256: ff6329f1c6c75504ffebe52359bc485ea98d9d9484228d28974f86639b1ab674
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador. 1) y bundle 2) ''Carpeta con eje''
  es una ruta que cae dentro de algún paths de un bloque [[axis]] de contracts/layers.toml
  (desde la línea 206). Un módulo nuevo en la misma carpeta que el archivo que se
  parte (por ejemplo src/sldb/api/rules/rule_graph_*.py junto a rule_graph.py) queda
  en el mismo eje y no se declara nada. Solo si el módulo cae en una carpeta que ningún
  axis cubre se agrega su ruta al paths del eje que corresponda; la puerta ''ejes''
  de tools/check.sh --fast lo verifica. 2) ''Líneas efectivas'' es lo que mide tests/test_clean_code_rules.py:48:
  líneas no vacías menos líneas de import. ''Líneas de lógica'' de una función (línea
  39) es del primer al último statement del cuerpo, docstring excluida. 3) y bundle
  1) Son cuatro tareas con cinco archivos de tests: on_write usa dos (test_on_write_entering.py
  y test_rules.py), y raw_atoms_by_view, notations y stores check sin build usan uno
  cada una. Los cinco son obligatorios (bundle 5). 4) y bundle 3) Criterio: extraer
  a un módulo hermano en la misma carpeta funciones privadas enteras, con nombre <archivo>_<tema>.py
  (p. ej. rule_graph_edges.py), hasta quedar en 80 o menos; para funciones de más
  de 10 líneas, partir en auxiliares privadas en el mismo archivo. La API pública
  (lo que se importa desde fuera) no cambia de módulo. 5) y bundle 4) Solo se acepta
  en rojo ''identidad'' cuando el único motivo que imprime es ''workbench_demo''.
  Cualquier otro motivo, u otra puerta en rojo, es FALLA. En result-summary.md se
  copia la línea de identidad. 6) Ningún otro agente toca estas rutas: el coordinador
  mantiene un solo ejecutor por repo. Si ''git status'' muestra cambios ajenos en
  esas rutas antes de empezar, el ejecutor para y lo informa. Bundle 6) El trailer
  es ''Task-Id: task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo''.'
# ISO 8601 timestamp
created_at: '2026-11-20T13:36:31.129464+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T13:38:15.101948+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-133619/context-review/task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo/preflight/30276b8a216b7ebfc378104ce87a04a6f36b29e33fcf3a5d519d2f8d5936b571/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador. 1) y bundle 2) 'Carpeta con eje' es una ruta que cae dentro de algún paths de un bloque [[axis]] de contracts/layers.toml (desde la línea 206). Un módulo nuevo en la misma carpeta que el archivo que se parte (por ejemplo src/sldb/api/rules/rule_graph_*.py junto a rule_graph.py) queda en el mismo eje y no se declara nada. Solo si el módulo cae en una carpeta que ningún axis cubre se agrega su ruta al paths del eje que corresponda; la puerta 'ejes' de tools/check.sh --fast lo verifica. 2) 'Líneas efectivas' es lo que mide tests/test_clean_code_rules.py:48: líneas no vacías menos líneas de import. 'Líneas de lógica' de una función (línea 39) es del primer al último statement del cuerpo, docstring excluida. 3) y bundle 1) Son cuatro tareas con cinco archivos de tests: on_write usa dos (test_on_write_entering.py y test_rules.py), y raw_atoms_by_view, notations y stores check sin build usan uno cada una. Los cinco son obligatorios (bundle 5). 4) y bundle 3) Criterio: extraer a un módulo hermano en la misma carpeta funciones privadas enteras, con nombre <archivo>_<tema>.py (p. ej. rule_graph_edges.py), hasta quedar en 80 o menos; para funciones de más de 10 líneas, partir en auxiliares privadas en el mismo archivo. La API pública (lo que se importa desde fuera) no cambia de módulo. 5) y bundle 4) Solo se acepta en rojo 'identidad' cuando el único motivo que imprime es 'workbench_demo'. Cualquier otro motivo, u otra puerta en rojo, es FALLA. En result-summary.md se copia la línea de identidad. 6) Ningún otro agente toca estas rutas: el coordinador mantiene un solo ejecutor por repo. Si 'git status' muestra cambios ajenos en esas rutas antes de empezar, el ejecutor para y lo informa. Bundle 6) El trailer es 'Task-Id: task-reglas-de-codigo-limpio-de-0f91540d-cinco-archivos-pasan-los-limites-rule-graph-rules-on-write-compo'.
