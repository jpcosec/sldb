---
sldb:
  by: agent
  at: '2026-11-11T16:53:06Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-seguridad-resto-2-las-lecturas-y-escrituras-de-documentos-trackeados-que-quedan-edges-records-views-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-seguridad-resto-2-las-lecturas-y-escrituras-de-documentos-trackeados-que-quedan-edges-records-views@sha256:cff2bef2342b18d118724bd0ac2a44bd1629c2ea4f21f2c4566c8f184a89d1f9
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261111-165204/context-review/task-seguridad-resto-2-las-lecturas-y-escrituras-de-documentos-trackeados-que-quedan-edges-records-views/bundle/68f03ed88ba1b52e2666d256e9bcff45feb013c7e0b8a6d98e9e9becdd96e877/attempt-2
input_sha256: 68f03ed88ba1b52e2666d256e9bcff45feb013c7e0b8a6d98e9e9becdd96e877
output_sha256: 40fbc699e34547e06bf3412d8c96b37272274e5b6dacf51a55a367edde962c8e
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Inventario:
  la lista del implementation_path es el piso. El worker confirma cada línea en su
  base y suma lo que encuentre el grep: read_text, read_bytes, open y os.open sobre
  una ruta derivada de doc.path, runtime_doc[''absolute_path''], node.semantics[''path'']
  o el destino de un enlace resuelto, bajo src/sldb. Excepciones: las de SEGURIDAD
  resto (store.yaml, store_index, shards yaml, pyproject, .gitignore) y archivos que
  no son documentos, cada una nombrada en el informe. (2) Objetivo único: un comando
  cuyo argumento nombra UN documento (sections show, docs compose de ese documento,
  serve /document/ir, records de un documento) sale con SLDBDocumentTargetError, exit
  1 y un mensaje con el código (store/path-outside-root o store/symlink-not-read).
  Las superficies agregadas (edges rebuild/rewrite, project graph, list_views, iter_records_docs,
  segments, model_registry) nombran el hallazgo como warning y siguen. Un enlace a
  un destino no legible queda como estaba escrito, sin abrirlo ni emitir la ruta.
  (3) Canónico: las lecturas, por read_source_text; las escrituras, por os.open con
  O_NOFOLLOW (un helper en sldb.store.source_read si se repite). (4) Archivo nuevo:
  en una carpeta con eje, no hace nada; un helper en src/sldb/store/ usa lectura_de_fuentes;
  si no, me pregunta. (5) Grados: en los comentarios de contracts/layers.toml, como
  hizo SEGURIDAD resto, con los valores que mide tools/check.sh --fast y fecha. (6)
  Matriz de tests: un archivo por superficie; edges en un archivo con tres casos (rebuild,
  rewrite, project graph). (7) Los 7 pasos los corre el coordinador; las excepciones
  del grep las decide él al verificar.'
# ISO 8601 timestamp
created_at: '2026-11-11T16:52:25.700721+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-11T16:53:06.416655+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-seguridad-resto-2-las-lecturas-y-escrituras-de-documentos-trackeados-que-quedan-edges-records-views

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261111-165204/context-review/task-seguridad-resto-2-las-lecturas-y-escrituras-de-documentos-trackeados-que-quedan-edges-records-views/bundle/68f03ed88ba1b52e2666d256e9bcff45feb013c7e0b8a6d98e9e9becdd96e877/attempt-2.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Inventario: la lista del implementation_path es el piso. El worker confirma cada línea en su base y suma lo que encuentre el grep: read_text, read_bytes, open y os.open sobre una ruta derivada de doc.path, runtime_doc['absolute_path'], node.semantics['path'] o el destino de un enlace resuelto, bajo src/sldb. Excepciones: las de SEGURIDAD resto (store.yaml, store_index, shards yaml, pyproject, .gitignore) y archivos que no son documentos, cada una nombrada en el informe. (2) Objetivo único: un comando cuyo argumento nombra UN documento (sections show, docs compose de ese documento, serve /document/ir, records de un documento) sale con SLDBDocumentTargetError, exit 1 y un mensaje con el código (store/path-outside-root o store/symlink-not-read). Las superficies agregadas (edges rebuild/rewrite, project graph, list_views, iter_records_docs, segments, model_registry) nombran el hallazgo como warning y siguen. Un enlace a un destino no legible queda como estaba escrito, sin abrirlo ni emitir la ruta. (3) Canónico: las lecturas, por read_source_text; las escrituras, por os.open con O_NOFOLLOW (un helper en sldb.store.source_read si se repite). (4) Archivo nuevo: en una carpeta con eje, no hace nada; un helper en src/sldb/store/ usa lectura_de_fuentes; si no, me pregunta. (5) Grados: en los comentarios de contracts/layers.toml, como hizo SEGURIDAD resto, con los valores que mide tools/check.sh --fast y fecha. (6) Matriz de tests: un archivo por superficie; edges en un archivo con tres casos (rebuild, rewrite, project graph). (7) Los 7 pasos los corre el coordinador; las excepciones del grep las decide él al verificar.
