---
sldb:
  by: agent
  at: '2026-11-12T00:40:36Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e@sha256:902a1b0afd89d72403dd535f06938cafdd40c783d51ef88b000490ab4d6f1b42
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261112-003955/context-review/task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e/bundle/67444820c34ad67d44fbce739d21b6449d54e6310bf1a9fe2281e6606b22ad37/attempt-1
input_sha256: 67444820c34ad67d44fbce739d21b6449d54e6310bf1a9fe2281e6606b22ad37
output_sha256: 1d8acd06186bf06d32ecad1dfbd0174a7c6605e6dd78109e3c75e9ec49740ed3
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Código:
  store/doc-invalid, una DiagnosisNote nueva (DOC_INVALID) en el mismo mapa _DOC_CODES
  de sldb/api/stores/store_findings.py que store/path-outside-root y store/symlink-not-read,
  severidad error. (2) La causa se confirma antes del arreglo con un test que falla
  en main (stores check sobre un store con un documento inválido da Unexpected) y
  se escribe en el informe, commiteada antes del arreglo. (3) Mensaje: ''invalid:
  <Model> rejects <path>: <N> validation error(s); first: <loc>: <msg>'', la primera
  línea de cada error de pydantic sin la URL de errors.pydantic.dev, como mucho 3
  errores. (4) Una sola vez: el documento que da DOC_INVALID no pasa por las demás
  comprobaciones que extraen con el modelo (campos, contrato movido, secciones, aristas)
  en ese diagnóstico; la clave es (modelo, nombre del documento), y el orden es el
  de hoy (por modelo y por documento). El worker enumera en el informe las rutas de
  stores check que extraen con el modelo. (5) Informe: runs/subagents/h1-worker-report.md.
  Para H2 alcanza con el mecanismo leído en el código (qué cambio hace que untrack
  o la escritura ya no extraigan los demás documentos del modelo, con su commit);
  un git bisect corto sobre la reproducción es opcional si el mecanismo no es claro.
  (6) Los tests de H2/H3 fijan, con dos documentos inválidos en el mismo modelo: (a)
  sldb.api untrack de uno de ellos da éxito, deja intactos el archivo y el índice
  del otro, y su git status muestra solo los índices del untrackeado y del modelo;
  (b) sldb.api.replace_text dentro de transaction sobre un documento válido del mismo
  modelo da éxito y no toca los otros; (c) si una transacción falla a propósito (excepción
  dentro del bloque), el rollback deja el árbol como estaba (H3).'
# ISO 8601 timestamp
created_at: '2026-11-12T00:40:09.884943+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-12T00:40:35.956279+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261112-003955/context-review/task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e/bundle/67444820c34ad67d44fbce739d21b6449d54e6310bf1a9fe2281e6606b22ad37/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Código: store/doc-invalid, una DiagnosisNote nueva (DOC_INVALID) en el mismo mapa _DOC_CODES de sldb/api/stores/store_findings.py que store/path-outside-root y store/symlink-not-read, severidad error. (2) La causa se confirma antes del arreglo con un test que falla en main (stores check sobre un store con un documento inválido da Unexpected) y se escribe en el informe, commiteada antes del arreglo. (3) Mensaje: 'invalid: <Model> rejects <path>: <N> validation error(s); first: <loc>: <msg>', la primera línea de cada error de pydantic sin la URL de errors.pydantic.dev, como mucho 3 errores. (4) Una sola vez: el documento que da DOC_INVALID no pasa por las demás comprobaciones que extraen con el modelo (campos, contrato movido, secciones, aristas) en ese diagnóstico; la clave es (modelo, nombre del documento), y el orden es el de hoy (por modelo y por documento). El worker enumera en el informe las rutas de stores check que extraen con el modelo. (5) Informe: runs/subagents/h1-worker-report.md. Para H2 alcanza con el mecanismo leído en el código (qué cambio hace que untrack o la escritura ya no extraigan los demás documentos del modelo, con su commit); un git bisect corto sobre la reproducción es opcional si el mecanismo no es claro. (6) Los tests de H2/H3 fijan, con dos documentos inválidos en el mismo modelo: (a) sldb.api untrack de uno de ellos da éxito, deja intactos el archivo y el índice del otro, y su git status muestra solo los índices del untrackeado y del modelo; (b) sldb.api.replace_text dentro de transaction sobre un documento válido del mismo modelo da éxito y no toca los otros; (c) si una transacción falla a propósito (excepción dentro del bloque), el rollback deja el árbol como estaba (H3).
