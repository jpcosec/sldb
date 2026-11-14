---
sldb:
  by: agent
  at: '2026-11-12T02:31:29Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la@sha256:48763804978afbecd704abf78fce171135ca6735c576cc2c6a3014c5dcf088c9
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261112-022741/context-review/task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la/preflight/fb778b76712be91f3ead5c6253e0f37b5bad6f29c90be5a4f0866a2abfa3fe7e/attempt-1
input_sha256: fb778b76712be91f3ead5c6253e0f37b5bad6f29c90be5a4f0866a2abfa3fe7e
output_sha256: 850c7a91353b1ffce2f0ad88f270da5ffcb444483db7d3aa8c905f8d0aa9be33
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) H4 en
  un alta: no hay índice anterior; el sujeto de la regla es el documento con su modelo,
  sus tags y el payload nuevo, y sin aristas previas (las reglas cuya condición depende
  de aristas ven un conjunto vacío). Lo dice la sección de on_write de rules.md. (2)
  H6, decisión: Finding NO gana campos (rules.md lo fija: el nodo en subject y la
  cláusula en what). El dato estructurado se expone aparte, aditivo: una función pública
  en sldb.api.tags que devuelve, por documento local, la evaluación de la familia
  (namespace, tags, lo que falta, la cláusula) calculada en la misma pasada que tag_check,
  y sldb tags check --format json agrega una clave evaluations junto a findings. Los
  nombres exactos los elige el worker y los deja en el informe y en tags.md. El texto
  del hallazgo y la salida de rules explain no cambian (explain ya devuelve node,
  holds, clause y seen). (3) H5: las claves autoradas de StoreDeclaration son las
  que declare_store no deriva del índice (hoy generate, derived, tag_namespaces y
  tag_models); si el worker encuentra otra que declare --write pierda, la suma y la
  lista en el informe; sumarla está en alcance. (4) Los 7 pasos del workflow de sldb
  son: tools/check.sh --fast, pytest, stores build, make world, el store de deskops,
  stores build --check y selfdoc; los corre el coordinador. (5) La suite completa
  de sldb es cada tests/**/test_*.py en su propia invocación de pytest, desde una
  copia en /dev/shm, con wait-pytest antes; nunca pytest tests/ entero. (6) Baja al
  cierre por CLI: deskops drawer remove para el ítem de drawer y deskops retire para
  las dos notas de inbox. (7) El informe es runs/subagents/h47-worker-report.md. (8)
  Orden de ejecución q1 a q5 como está; cada paso con su commit.'
# ISO 8601 timestamp
created_at: '2026-11-12T02:27:53.297647+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-12T02:31:28.783864+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261112-022741/context-review/task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la/preflight/fb778b76712be91f3ead5c6253e0f37b5bad6f29c90be5a4f0866a2abfa3fe7e/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) H4 en un alta: no hay índice anterior; el sujeto de la regla es el documento con su modelo, sus tags y el payload nuevo, y sin aristas previas (las reglas cuya condición depende de aristas ven un conjunto vacío). Lo dice la sección de on_write de rules.md. (2) H6, decisión: Finding NO gana campos (rules.md lo fija: el nodo en subject y la cláusula en what). El dato estructurado se expone aparte, aditivo: una función pública en sldb.api.tags que devuelve, por documento local, la evaluación de la familia (namespace, tags, lo que falta, la cláusula) calculada en la misma pasada que tag_check, y sldb tags check --format json agrega una clave evaluations junto a findings. Los nombres exactos los elige el worker y los deja en el informe y en tags.md. El texto del hallazgo y la salida de rules explain no cambian (explain ya devuelve node, holds, clause y seen). (3) H5: las claves autoradas de StoreDeclaration son las que declare_store no deriva del índice (hoy generate, derived, tag_namespaces y tag_models); si el worker encuentra otra que declare --write pierda, la suma y la lista en el informe; sumarla está en alcance. (4) Los 7 pasos del workflow de sldb son: tools/check.sh --fast, pytest, stores build, make world, el store de deskops, stores build --check y selfdoc; los corre el coordinador. (5) La suite completa de sldb es cada tests/**/test_*.py en su propia invocación de pytest, desde una copia en /dev/shm, con wait-pytest antes; nunca pytest tests/ entero. (6) Baja al cierre por CLI: deskops drawer remove para el ítem de drawer y deskops retire para las dos notas de inbox. (7) El informe es runs/subagents/h47-worker-report.md. (8) Orden de ejecución q1 a q5 como está; cada paso con su commit.
