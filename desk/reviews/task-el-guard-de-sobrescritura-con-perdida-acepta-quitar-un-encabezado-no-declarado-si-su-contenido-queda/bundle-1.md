---
sldb:
  by: agent
  at: '2026-11-22T11:17:51Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda@sha256:5415285cb289ab6dad1073200b942dfb7c98c48f4588c9f2e1cbb542110dca2d
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261122-111538/context-review/task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda/bundle/dbec87b96930553ebb9ef4de5bb323bc1bacc89f7d142ed8776b14959f09b86e/attempt-1
input_sha256: dbec87b96930553ebb9ef4de5bb323bc1bacc89f7d142ed8776b14959f09b86e
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: adcbc35b6673767fcfe45fbb10bb7a57ea65ff6a13c8b313ba05b7aedeabb5a1
output_sha256: f47cd88ec33775f9a04846e6dbf6ee45df2d891cc7ffb0ba2319cbae2db1d42f
# pending | accepted | rejected | incomplete
verdict: accepted
reason: "Aceptado. Resoluciones del coordinador, con el código actual.\n\nP1, P2,\
  \ P3 y B1) Contrato preciso. Hoy _lost_headings (src/sldb/api/documents/lossy_overwrite.py,\
  \ alrededor de la línea 38) devuelve las líneas de encabezado no declarado que el\
  \ texto renderizado no conserva. El cambio va después de calcular esas líneas: un\
  \ encabezado perdido deja de contar como pérdida si su contenido sobrevive.\n- **Contenido\
  \ de un encabezado:** el texto del archivo actual entre esa línea de encabezado\
  \ y el siguiente encabezado de nivel igual o superior (o el fin del documento),\
  \ sin la línea del encabezado.\n- **Normalización:** igual en ambos lados.\n  1.\
  \ quitar marcas Markdown de énfasis (* y _) y los prefijos de viñeta ('- ', '* ',\
  \ '1. ');\n  2. colapsar todo espacio en blanco, saltos incluidos, en un solo espacio;\n\
  \  3. recortar extremos;\n  4. pasar a minúsculas (casefold);\n  5. aplicar NFC\
  \ de Unicode.\n- **Criterio:** el contenido normalizado está como subcadena del\
  \ texto renderizado completo normalizado. No hace falta localizar campos ni párrafos.\n\
  - **Contenido vacío:** un encabezado sin contenido se considera conservado.\n\n\
  P4 y B2) Son dos tests con estos nombres:\n- test_dropping_an_undeclared_heading_whose_content_survives_is_accepted\n\
  - test_dropping_an_undeclared_heading_whose_content_is_lost_is_refused\nVan en tests/api/test_lossy_overwrite.py\
  \ (nuevo). El fixture es un documento con '## Tags' y su lista bajo él: en el primero\
  \ el texto nuevo trae esa lista dentro de un campo, en el segundo no.\n\nP5) El\
  \ criterio de CLI se comprueba con sldb fields set sobre un documento temporal en\
  \ el test, o llamando a la API de escritura de campo que usa ese comando. deskops\
  \ edit atom no se toca: es de otro repo.\n\nP6 y B5) El worktree es el que dispatch\
  \ le da al ejecutor (rama deskops/<agente> desde main). El trailer es 'Task-Id:\
  \ <id de esta tarea>' en el cuerpo.\n\nP7 y B4) bash tools/check.sh --fast se corre\
  \ antes del commit. La única roja aceptada es la puerta 'identidad' por el directorio\
  \ workbench_demo (decisión f055723d, vigente hasta que JP la resuelva). Cualquier\
  \ otra puerta en rojo bloquea.\n\nB3) Regresión: tests/api completo con -n 4, más\
  \ tests/test_extraction_segments.py, que es el único test existente que usa el guard\
  \ (grep -rln lossy tests/).\n\nB6) El fixture es el del punto P4, un documento temporal.\n\
  \nB7) El CHANGELOG es exigible: una viñeta en la sección superior sin publicar."
# ISO 8601 timestamp
created_at: '2026-11-22T11:15:56.692756+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T11:17:27.314435+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261122-111538/context-review/task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda/bundle/dbec87b96930553ebb9ef4de5bb323bc1bacc89f7d142ed8776b14959f09b86e/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador, con el código actual.

P1, P2, P3 y B1) Contrato preciso. Hoy _lost_headings (src/sldb/api/documents/lossy_overwrite.py, alrededor de la línea 38) devuelve las líneas de encabezado no declarado que el texto renderizado no conserva. El cambio va después de calcular esas líneas: un encabezado perdido deja de contar como pérdida si su contenido sobrevive.
- **Contenido de un encabezado:** el texto del archivo actual entre esa línea de encabezado y el siguiente encabezado de nivel igual o superior (o el fin del documento), sin la línea del encabezado.
- **Normalización:** igual en ambos lados.
  1. quitar marcas Markdown de énfasis (* y _) y los prefijos de viñeta ('- ', '* ', '1. ');
  2. colapsar todo espacio en blanco, saltos incluidos, en un solo espacio;
  3. recortar extremos;
  4. pasar a minúsculas (casefold);
  5. aplicar NFC de Unicode.
- **Criterio:** el contenido normalizado está como subcadena del texto renderizado completo normalizado. No hace falta localizar campos ni párrafos.
- **Contenido vacío:** un encabezado sin contenido se considera conservado.

P4 y B2) Son dos tests con estos nombres:
- test_dropping_an_undeclared_heading_whose_content_survives_is_accepted
- test_dropping_an_undeclared_heading_whose_content_is_lost_is_refused
Van en tests/api/test_lossy_overwrite.py (nuevo). El fixture es un documento con '## Tags' y su lista bajo él: en el primero el texto nuevo trae esa lista dentro de un campo, en el segundo no.

P5) El criterio de CLI se comprueba con sldb fields set sobre un documento temporal en el test, o llamando a la API de escritura de campo que usa ese comando. deskops edit atom no se toca: es de otro repo.

P6 y B5) El worktree es el que dispatch le da al ejecutor (rama deskops/<agente> desde main). El trailer es 'Task-Id: <id de esta tarea>' en el cuerpo.

P7 y B4) bash tools/check.sh --fast se corre antes del commit. La única roja aceptada es la puerta 'identidad' por el directorio workbench_demo (decisión f055723d, vigente hasta que JP la resuelva). Cualquier otra puerta en rojo bloquea.

B3) Regresión: tests/api completo con -n 4, más tests/test_extraction_segments.py, que es el único test existente que usa el guard (grep -rln lossy tests/).

B6) El fixture es el del punto P4, un documento temporal.

B7) El CHANGELOG es exigible: una viñeta en la sección superior sin publicar.
