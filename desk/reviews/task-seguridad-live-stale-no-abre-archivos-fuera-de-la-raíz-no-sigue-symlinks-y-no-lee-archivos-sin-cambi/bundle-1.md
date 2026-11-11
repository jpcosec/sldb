---
sldb:
  by: agent
  at: '2026-11-11T07:38:22Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-seguridad-live-stale-no-abre-archivos-fuera-de-la-raíz-no-sigue-symlinks-y-no-lee-archivos-sin-cambi-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-seguridad-live-stale-no-abre-archivos-fuera-de-la-raíz-no-sigue-symlinks-y-no-lee-archivos-sin-cambi@sha256:67e39022d2823b7975bc07c63958db5949cd424f99acc51658e2e24de20c8af7
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261111-073745/context-review/task-seguridad-live-stale-no-abre-archivos-fuera-de-la-raíz-no-sigue-symlinks-y-no-lee-archivos-sin-cambi/bundle/70d208b5f6fa23b83d09c9bf3fed6aa7627c06ad538d010f624ee36801007767/attempt-1
input_sha256: 70d208b5f6fa23b83d09c9bf3fed6aa7627c06ad538d010f624ee36801007767
output_sha256: 43a6885b60b32d3dac4821e2df0f0724eacf02dbc7b1a7b2be709df01e4374d7
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Fijado por el coordinador, sin cambiar el contrato:

  - Raíz: project_root(store_path), la que ya usa live_stale (el directorio que contiene
  .sldb).

  - Hallazgos: ''store/path-outside-root'' (s1) y ''store/symlink-not-read'' (s2),
  severidad alert, publicados por la misma vía que los demás códigos de documento
  (store_findings._DOC_CODES y stores check).

  - stale sigue siendo list[str] de ids (contrato sin cambio); el motivo va en el
  hallazgo, no en la lista.

  - s2 revisable: si rompe un caso real, el worker para y avisa al coordinador con
  la propuesta antes de cambiar el criterio.

  - Stat en el shard: campo opcional source_stat [mtime_ns, size] en DocEdges, por
  defecto None. Un shard sin él se hashea como hoy (compatible, sin migración de formato);
  el próximo build lo completa.

  - Informe: runs/subagents/livestale-worker-report.md, con una sección ''Servidores''
  para s5.

  - Archivo protegido en el test: un archivo trackeado dentro de la raíz que el test
  afirma, con el audit hook, que no se abre mientras no cambió desde el build.

  Sin ambigüedad abierta.'
# ISO 8601 timestamp
created_at: '2026-11-11T07:37:57.603022+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-11T07:38:21.794259+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-seguridad-live-stale-no-abre-archivos-fuera-de-la-raíz-no-sigue-symlinks-y-no-lee-archivos-sin-cambi

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261111-073745/context-review/task-seguridad-live-stale-no-abre-archivos-fuera-de-la-raíz-no-sigue-symlinks-y-no-lee-archivos-sin-cambi/bundle/70d208b5f6fa23b83d09c9bf3fed6aa7627c06ad538d010f624ee36801007767/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Fijado por el coordinador, sin cambiar el contrato:
- Raíz: project_root(store_path), la que ya usa live_stale (el directorio que contiene .sldb).
- Hallazgos: 'store/path-outside-root' (s1) y 'store/symlink-not-read' (s2), severidad alert, publicados por la misma vía que los demás códigos de documento (store_findings._DOC_CODES y stores check).
- stale sigue siendo list[str] de ids (contrato sin cambio); el motivo va en el hallazgo, no en la lista.
- s2 revisable: si rompe un caso real, el worker para y avisa al coordinador con la propuesta antes de cambiar el criterio.
- Stat en el shard: campo opcional source_stat [mtime_ns, size] en DocEdges, por defecto None. Un shard sin él se hashea como hoy (compatible, sin migración de formato); el próximo build lo completa.
- Informe: runs/subagents/livestale-worker-report.md, con una sección 'Servidores' para s5.
- Archivo protegido en el test: un archivo trackeado dentro de la raíz que el test afirma, con el audit hook, que no se abre mientras no cambió desde el build.
Sin ambigüedad abierta.
