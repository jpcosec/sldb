---
sldb:
  by: agent
  at: '2026-11-23T17:53:46Z'
  authority: generated
  via: save_document_payload
id: task-sldb-serve-tolera-documentos-invalidos-ve-altas-de-otros-procesos-y-resuelve-tipo-nombre-en-document
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261121-220138-unclear-sldb-serve-no-deja-leer-ni-reparar-nada-cuando-un-documento-del-store-es-invalido.md
- desk/inbox/20261122-232536-unclear-sldb-serve-no-ve-altas-hechas-por-otro-proceso-hasta-su-pr-ximo-guardado.md
- desk/inbox/20261122-233451-unclear-sldb-serve-document-y-save-no-resuelven-tipo-nombre-hom-nimos-entre-modelos.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb serve tolera documentos invalidos, ve altas de otros procesos y resuelve Tipo/nombre en document y save

## Rationale

_Explain why this task exists or the business driver behind it._

Notas 20261121-220138-unclear-sldb-serve-no-deja-leer-ni-reparar-nada-cuando-un-documento-del-store-es-invalido, 20261122-232536-unclear-sldb-serve-no-ve-altas-hechas-por-otro-proceso-hasta-su-pr-ximo-guardado y 20261122-233451-unclear-sldb-serve-document-y-save-no-resuelven-tipo-nombre-hom-nimos-entre-modelos (sesion de minegocio, 21 y 22-nov): (1) un documento invalido en el store deja /graph en 500, /document/segments de otro documento sano en 422 y POST /save en 500 (cli/serve/save_routes.py:33-42); (2) serve no ve lo que otro proceso crea con create_document hasta su proximo guardado (404 Unknown doc); (3) /document, /document/ir, /document/segments y POST /save update/delete no aceptan Tipo/nombre: con homonimos entre modelos ninguno se abre ni se guarda (tracked_docs.is_tracked y batch_prevalidate._existing/find_doc). El lector de surface depende de esto.

## Goal

_Describe the concrete result this task must produce._

sldb serve entrega los documentos sanos y nombra aparte los rechazados (como load_runtime_documents(on_invalid='skip')), deja abrir y reparar un documento rechazado; refleja altas, cambios y bajas hechos por otro proceso sin reiniciar ni guardar; acepta Tipo/nombre en /document, /document/ir, /document/segments y POST /save; el 422 de /save devuelve exc.errors() como details.

## Scope

_State what is in scope and what is out of scope._

src/sldb/cli/serve/ (rutas de graph, document, segments y save), tracked_docs, batch_prevalidate y el cache del servidor, con tests de serve. Fuera: la superficie.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Tests que reproducen los tres casos (documento invalido en el store, alta por la API de Python con serve arriba, dos homonimos en modelos distintos; minegocio tiene la prueba xfail test_dos_paginas_con_el_mismo_nombre_se_abren_y_se_guardan_cada_una como guia). 2) Lectura tolerante con lista de rechazados. 3) Invalidacion del cache de serve por firma del store (mtime/hash de shards). 4) Resolucion Tipo/nombre en las rutas que faltan. 5) details del 422.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/ -k serve

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan y los de serve existentes siguen verdes; los tres casos de las notas quedan cubiertos.
