---
sldb:
  by: agent
  at: '2026-11-21T07:03:00Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest-preflight-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest@sha256:131106937668e6788eccd72fdd3f74955d89103f347af3e1832b2c83e3c63bf1
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-070137/context-review/task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest/preflight/1a2d000553e90b21e63bc35c79286b92d3ca3da996e3fe2232b8729100844a99/attempt-1
input_sha256: 1a2d000553e90b21e63bc35c79286b92d3ca3da996e3fe2232b8729100844a99
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 5abb1614d72982ace748914c1c7957873ddc04f8558b96873588d02ddceebab5
output_sha256: 95b02e8bd65c2dadd71d47e27c709cf7b94d6068161d82e170f2ab27e333af8b
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones: 1) ''Sin lógica'' es estrictamente: docstring, sentencias
  import/from-import a nivel de módulo, asignaciones de nombres reexportados y __all__.
  Cualquier otra cosa (if, try, def, class, llamadas con efecto, __getattr__ dinámico)
  hace que el módulo NO sea cáscara y se conserva. 2) Solo protegen las referencias
  en src/, tests/, tools/, docs/ y pyproject.toml (entry points). Una mención en docs/
  cuenta como uso solo si nombra la ruta importable (sldb.api.x o src/sldb/api/x.py);
  en ese caso se conserva o se actualiza la doc en el mismo commit. Consumidores de
  otros repos (deskops, IR, pron, graph_ui) no se buscan aquí, salvo que importen
  el módulo por un nombre que esté en un __all__: eso es API pública y se conserva.
  getattr/plugins dinámicos: si git grep encuentra el nombre del módulo como cadena
  en src/, se conserva. 3) API pública = lo que aparece en algún __all__ de sldb.api
  o de sus subpaquetes; un símbolo fuera de todo __all__ no es API pública, pero si
  se importa en src/ o tests/ se conserva igual. 4) Inventario de stores.py: el ejecutor
  lista con git grep cada función y constante de nivel de módulo de src/sldb/cli/parsers/stores.py
  y borra solo las que no tienen ningún uso fuera de su propia definición; los subcomandos
  registrados no se tocan. Los cuatro archivos nombrados existen hoy en origin/main
  (cli/parsers/graph.py, cli/commands/help_texts_graph.py, store/graph/ingest_sldb.py,
  selfdoc/python_source_graph.py). Commit en el worktree que dispatch le da al ejecutor
  con trailer ''Task-Id: task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest''
  en el cuerpo; la puerta identidad de tools/check.sh --fast falla por workbench_demo
  (excepción autorizada f055723d).'
# ISO 8601 timestamp
created_at: '2026-11-21T07:01:52.788915+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T07:02:29.102672+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-070137/context-review/task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest/preflight/1a2d000553e90b21e63bc35c79286b92d3ca3da996e3fe2232b8729100844a99/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones: 1) 'Sin lógica' es estrictamente: docstring, sentencias import/from-import a nivel de módulo, asignaciones de nombres reexportados y __all__. Cualquier otra cosa (if, try, def, class, llamadas con efecto, __getattr__ dinámico) hace que el módulo NO sea cáscara y se conserva. 2) Solo protegen las referencias en src/, tests/, tools/, docs/ y pyproject.toml (entry points). Una mención en docs/ cuenta como uso solo si nombra la ruta importable (sldb.api.x o src/sldb/api/x.py); en ese caso se conserva o se actualiza la doc en el mismo commit. Consumidores de otros repos (deskops, IR, pron, graph_ui) no se buscan aquí, salvo que importen el módulo por un nombre que esté en un __all__: eso es API pública y se conserva. getattr/plugins dinámicos: si git grep encuentra el nombre del módulo como cadena en src/, se conserva. 3) API pública = lo que aparece en algún __all__ de sldb.api o de sus subpaquetes; un símbolo fuera de todo __all__ no es API pública, pero si se importa en src/ o tests/ se conserva igual. 4) Inventario de stores.py: el ejecutor lista con git grep cada función y constante de nivel de módulo de src/sldb/cli/parsers/stores.py y borra solo las que no tienen ningún uso fuera de su propia definición; los subcomandos registrados no se tocan. Los cuatro archivos nombrados existen hoy en origin/main (cli/parsers/graph.py, cli/commands/help_texts_graph.py, store/graph/ingest_sldb.py, selfdoc/python_source_graph.py). Commit en el worktree que dispatch le da al ejecutor con trailer 'Task-Id: task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest' en el cuerpo; la puerta identidad de tools/check.sh --fast falla por workbench_demo (excepción autorizada f055723d).
