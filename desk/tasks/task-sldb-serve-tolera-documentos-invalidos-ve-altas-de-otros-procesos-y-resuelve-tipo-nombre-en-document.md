---
sldb:
  by: agent
  at: '2026-11-25T01:14:23Z'
  authority: generated
  via: save_document_payload
id: task-sldb-serve-tolera-documentos-invalidos-ve-altas-de-otros-procesos-y-resuelve-tipo-nombre-en-document
status: draft
summary: ''
tags: []
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

sldb serve entrega los documentos sanos y nombra aparte los rechazados (como load_runtime_documents(on_invalid='skip')), y deja abrir un documento rechazado para repararlo.

## Scope

_State what is in scope and what is out of scope._

src/sldb/cli/serve/ (lectura del store y rutas graph/document) y un test de serve nuevo. Fuera: cache, Tipo/nombre, 422, surface.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test: store con un documento invalido; serve arranca, /graph lista los sanos y trae la lista de rechazados; /document del rechazado lo abre con su error. 2) Lectura tolerante. Correr solo el test nuevo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_serve_tolerante.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa: un documento invalido no tumba serve, se lista como rechazado y se puede abrir.
