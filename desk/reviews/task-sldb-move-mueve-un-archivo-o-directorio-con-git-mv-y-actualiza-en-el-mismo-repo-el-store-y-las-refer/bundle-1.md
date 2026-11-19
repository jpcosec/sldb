---
sldb:
  by: agent
  at: '2026-11-19T18:47:59Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer@sha256:98bbd79d13530ee48b77ff4b1a26fb40cbda1eab3c80233a09614f0d69c47152
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261119-184539/context-review/task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer/bundle/19998ba6e319508990cdcee0a40077c10519d8eb01bffccdbcd7b5c123d41cba/attempt-1
input_sha256: 19998ba6e319508990cdcee0a40077c10519d8eb01bffccdbcd7b5c123d41cba
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 09dbad164544411ff6b85beda9bfc76350914771fc507d8c2a5816bb37c30d73
output_sha256: 6a723f47de1e0696062868cae7f11e9c2d1923e3561c3742997008b7a19cbc04
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador. 1) Rollback: los cambios en disco
  y en el store van dentro de una Transaction, que ya guarda un snapshot de cada archivo
  tocado y lo restaura si algo falla (transaction_state.py, store/io/rollback.py).
  El índice de git se toca recién al final, cuando la transacción ya se confirmó:
  git rm --cached -r -q <viejo> y git add <nuevo> de los archivos que git versionaba
  (git lo detecta como renombre, igual que git mv). Si un fallo ocurre antes, git
  no se tocó. Si falla ese último paso, el comando sale con error y dice los dos comandos
  git que faltan. 2) Versionado: un archivo cuenta como versionado si ''git ls-files
  --error-unmatch'' lo encuentra. Un directorio se mueve entero en disco, ignorados
  incluidos, y en el índice se actualizan solo los archivos que git versionaba. Si
  el destino existe (archivo o directorio), el comando da error y no cambia nada;
  es requisito. 3) Valor de campo: cada string del payload de un documento, recorriendo
  listas y dicts anidados; los campos derivados que no están en el payload no cuentan.
  Se compara normalizado: sin ''./'' al inicio ni ''/'' al final, como ruta POSIX
  relativa a la raíz del proyecto. Una ruta absoluta dentro del proyecto se compara
  en su forma relativa y se reescribe manteniendo la absoluta. Se escribe con save_document_payload.
  4) Links: links inline e imágenes ([x](ruta) y ![x](ruta)) y definiciones de referencia
  ([id]: ruta), resueltos desde el directorio del archivo que los contiene. Se conservan
  #ancla y ?query. No se tocan URLs con esquema ni rutas que empiezan con ''/''. Se
  usa el mismo parser markdown-it del scan de enlaces (04e18217), así que no se tocan
  links dentro de código. Archivos: los .md versionados (git ls-files). Si el .md
  es un documento trackeado por sldb, el link se reescribe dentro del valor del campo
  y se guarda con save_document_payload; si no, se reescribe el texto del archivo,
  también dentro de la Transaction. 5) La referencia de CLI regenerada va en el mismo
  commit que el código, con rutas nombradas y trailer ''Task-Id: <id>''. Bundle: 1)
  ''Nombre'' es el nombre del documento en el store (su id), no el basename: al mover
  un directorio cada documento conserva su nombre y solo cambia su ruta. 5) --format
  es text por defecto; --store elige el store como en los demás comandos (si no se
  da, se descubre), y las rutas son siempre relativas a la raíz del proyecto de ese
  store. 6) Ver 2: destino existente es error, también un directorio sobre otro.'
# ISO 8601 timestamp
created_at: '2026-11-19T18:45:55.811636+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T18:47:37.242329+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-184539/context-review/task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer/bundle/19998ba6e319508990cdcee0a40077c10519d8eb01bffccdbcd7b5c123d41cba/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador. 1) Rollback: los cambios en disco y en el store van dentro de una Transaction, que ya guarda un snapshot de cada archivo tocado y lo restaura si algo falla (transaction_state.py, store/io/rollback.py). El índice de git se toca recién al final, cuando la transacción ya se confirmó: git rm --cached -r -q <viejo> y git add <nuevo> de los archivos que git versionaba (git lo detecta como renombre, igual que git mv). Si un fallo ocurre antes, git no se tocó. Si falla ese último paso, el comando sale con error y dice los dos comandos git que faltan. 2) Versionado: un archivo cuenta como versionado si 'git ls-files --error-unmatch' lo encuentra. Un directorio se mueve entero en disco, ignorados incluidos, y en el índice se actualizan solo los archivos que git versionaba. Si el destino existe (archivo o directorio), el comando da error y no cambia nada; es requisito. 3) Valor de campo: cada string del payload de un documento, recorriendo listas y dicts anidados; los campos derivados que no están en el payload no cuentan. Se compara normalizado: sin './' al inicio ni '/' al final, como ruta POSIX relativa a la raíz del proyecto. Una ruta absoluta dentro del proyecto se compara en su forma relativa y se reescribe manteniendo la absoluta. Se escribe con save_document_payload. 4) Links: links inline e imágenes ([x](ruta) y ![x](ruta)) y definiciones de referencia ([id]: ruta), resueltos desde el directorio del archivo que los contiene. Se conservan #ancla y ?query. No se tocan URLs con esquema ni rutas que empiezan con '/'. Se usa el mismo parser markdown-it del scan de enlaces (04e18217), así que no se tocan links dentro de código. Archivos: los .md versionados (git ls-files). Si el .md es un documento trackeado por sldb, el link se reescribe dentro del valor del campo y se guarda con save_document_payload; si no, se reescribe el texto del archivo, también dentro de la Transaction. 5) La referencia de CLI regenerada va en el mismo commit que el código, con rutas nombradas y trailer 'Task-Id: <id>'. Bundle: 1) 'Nombre' es el nombre del documento en el store (su id), no el basename: al mover un directorio cada documento conserva su nombre y solo cambia su ruta. 5) --format es text por defecto; --store elige el store como en los demás comandos (si no se da, se descubre), y las rutas son siempre relativas a la raíz del proyecto de ese store. 6) Ver 2: destino existente es error, también un directorio sobre otro.
