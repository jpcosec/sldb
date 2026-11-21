---
sldb:
  by: agent
  at: '2026-11-21T06:56:05Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent-preflight-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent@sha256:a4938ff58f997cb0c085a0bb66ce7726dfe83113a14cbc85be0582bee14cd451
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-065328/context-review/task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent/preflight/f1dd0049d0e950ad6ada2b0e7036afa509466b43dffef49cd768dc7d4d138264/attempt-1
input_sha256: f1dd0049d0e950ad6ada2b0e7036afa509466b43dffef49cd768dc7d4d138264
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 8abb5c6c9ba98bed096ac8491c7b01c043672fe9f363b1e80dea0f5146a3e48a
output_sha256: 6fc0d10b446417c3c962f341ea946d422808e132b56cb933b1cad558c4a4a571
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones (código en origin/main, src/sldb/store/documents_dirty.py):
  1) _DIRTY ya se indexa por (str(s_path), modelo, namespace) con namespaces semantic/sections/edges;
  la carga perezosa es por s_path: un set interno de stores ya cargados; la primera
  llamada a names(s_path, ...) para un s_path no cargado lee el archivo de ese store
  y vuelca sus entries en _DIRTY. 2) Las firmas actuales no cambian: mark(s_path,
  model_name, name) agrega a los tres namespaces conocidos; clear(s_path, model_name,
  namespace) deja esa clave en set() (una entrada); invalidate(s_path, model_name)
  quita las tres claves del modelo; después de cada una se reescribe el archivo entero
  del s_path con todas sus claves. clear_all() solo vacía la memoria (y el set de
  cargados), no borra archivos. 3) names() ya devuelve None cuando no hay base (contrato
  vigente que usa documents_hash.py:117); no es contrato nuevo y test_edges_follow_the_contract.py
  no cambia. 4) Firma distinta a la de runtime_cache_signature.signature(s_path):
  se descarta el contenido (no se carga nada, names() devuelve None) y el archivo
  se reescribe en la próxima escritura con la firma nueva. 5) El borrado del archivo
  corrupto se hace dentro de store_lock(s_path, wait=True) (src/sldb/store/io/__init__.py:12)
  y no carga nada en _DIRTY para ese store. 6) Ruta: sldb.store.layout.cache_dir(s_path)
  / ''documents_dirty.json'' (layout.py:19, que da el directorio de caché junto al
  store); no user_cache.py (ese es el caché XDG). 7) CHANGELOG.md: una viñeta en español
  bajo ''## 0.1.13 — not released yet'', con el estilo de las existentes (qué cambia,
  archivos y tests). Commit en el worktree que dispatch le da al ejecutor con trailer
  ''Task-Id: task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent''
  en el cuerpo; la puerta identidad de tools/check.sh --fast falla por workbench_demo
  (excepción autorizada f055723d).'
# ISO 8601 timestamp
created_at: '2026-11-21T06:53:47.554976+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T06:55:36.157738+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-065328/context-review/task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent/preflight/f1dd0049d0e950ad6ada2b0e7036afa509466b43dffef49cd768dc7d4d138264/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones (código en origin/main, src/sldb/store/documents_dirty.py): 1) _DIRTY ya se indexa por (str(s_path), modelo, namespace) con namespaces semantic/sections/edges; la carga perezosa es por s_path: un set interno de stores ya cargados; la primera llamada a names(s_path, ...) para un s_path no cargado lee el archivo de ese store y vuelca sus entries en _DIRTY. 2) Las firmas actuales no cambian: mark(s_path, model_name, name) agrega a los tres namespaces conocidos; clear(s_path, model_name, namespace) deja esa clave en set() (una entrada); invalidate(s_path, model_name) quita las tres claves del modelo; después de cada una se reescribe el archivo entero del s_path con todas sus claves. clear_all() solo vacía la memoria (y el set de cargados), no borra archivos. 3) names() ya devuelve None cuando no hay base (contrato vigente que usa documents_hash.py:117); no es contrato nuevo y test_edges_follow_the_contract.py no cambia. 4) Firma distinta a la de runtime_cache_signature.signature(s_path): se descarta el contenido (no se carga nada, names() devuelve None) y el archivo se reescribe en la próxima escritura con la firma nueva. 5) El borrado del archivo corrupto se hace dentro de store_lock(s_path, wait=True) (src/sldb/store/io/__init__.py:12) y no carga nada en _DIRTY para ese store. 6) Ruta: sldb.store.layout.cache_dir(s_path) / 'documents_dirty.json' (layout.py:19, que da el directorio de caché junto al store); no user_cache.py (ese es el caché XDG). 7) CHANGELOG.md: una viñeta en español bajo '## 0.1.13 — not released yet', con el estilo de las existentes (qué cambia, archivos y tests). Commit en el worktree que dispatch le da al ejecutor con trailer 'Task-Id: task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent' en el cuerpo; la puerta identidad de tools/check.sh --fast falla por workbench_demo (excepción autorizada f055723d).
