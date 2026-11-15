---
sldb:
  by: agent
  at: '2026-11-15T16:02:41Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e@sha256:655c45a83438eb9cea228914cf89453ead19bd06ff78575c4f5d527fd45c63ac
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261115-160116/context-review/task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e/preflight/27cb49a77accc1532bb9b8b0225ae367b1a28fb566686c67de0e4d14b4b45ddc/attempt-1
input_sha256: 27cb49a77accc1532bb9b8b0225ae367b1a28fb566686c67de0e4d14b4b45ddc
output_sha256: 1406f3d3f0774c3d2485f8e7250967b786a54691aac1e387714481783c932cc2
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coordinador wA:p1, revisable).
  (1) Log de señales: JSONL de solo agregado en <store>/.sldb_cache/signals.jsonl,
  una línea por señal con at, tool, arguments, signal_class, suggestions y actor.
  Es caché, no estado del store, el mismo criterio que .sldb_cache/composed de H11,
  así que funciona en nivel 0 y la comprobación de que leer no escribe excluye .sldb_cache.
  Escritura con O_APPEND de una línea por llamada; sin rotación en esta tarea. (2)
  Sugerencias: las de sldb.api.matching con sus parámetros por defecto, las 5 primeras
  en su orden, en la clave suggestions de la respuesta. (3) Extensión: si IR ya tiene
  un punto de extensión, se migra tal cual. Si no, build_server(store, level, actor,
  extensions=[callable(server, context)]) y el flag repetible --extension modulo:funcion
  en sldb mcp, con un test que registra una tool de prueba. (4) Matriz de niveles:
  la de IR (mutability.py), que se migra. Nivel 0 es lectura más list_signals, nivel
  1 suma propose_changes y nivel 2 suma apply_changes. (5) Tests: se portan los de
  IR tal cual, cambiando solo imports y nombres de paquete; sin literales nuevos que
  repitan la respuesta. (6) Deshacer pendiente: undo_changes no se registra; llamarla
  devuelve la señal no implementada y queda en el log; un test lo fija. (7) La validación
  final es la del brief: suite de sldb completa de a un archivo, tools/check.sh y
  sldb stores build --check; los corre el coordinador.'
# ISO 8601 timestamp
created_at: '2026-11-15T16:01:29.243964+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-15T16:02:24.400194+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261115-160116/context-review/task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e/preflight/27cb49a77accc1532bb9b8b0225ae367b1a28fb566686c67de0e4d14b4b45ddc/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coordinador wA:p1, revisable). (1) Log de señales: JSONL de solo agregado en <store>/.sldb_cache/signals.jsonl, una línea por señal con at, tool, arguments, signal_class, suggestions y actor. Es caché, no estado del store, el mismo criterio que .sldb_cache/composed de H11, así que funciona en nivel 0 y la comprobación de que leer no escribe excluye .sldb_cache. Escritura con O_APPEND de una línea por llamada; sin rotación en esta tarea. (2) Sugerencias: las de sldb.api.matching con sus parámetros por defecto, las 5 primeras en su orden, en la clave suggestions de la respuesta. (3) Extensión: si IR ya tiene un punto de extensión, se migra tal cual. Si no, build_server(store, level, actor, extensions=[callable(server, context)]) y el flag repetible --extension modulo:funcion en sldb mcp, con un test que registra una tool de prueba. (4) Matriz de niveles: la de IR (mutability.py), que se migra. Nivel 0 es lectura más list_signals, nivel 1 suma propose_changes y nivel 2 suma apply_changes. (5) Tests: se portan los de IR tal cual, cambiando solo imports y nombres de paquete; sin literales nuevos que repitan la respuesta. (6) Deshacer pendiente: undo_changes no se registra; llamarla devuelve la señal no implementada y queda en el log; un test lo fija. (7) La validación final es la del brief: suite de sldb completa de a un archivo, tools/check.sh y sldb stores build --check; los corre el coordinador.
