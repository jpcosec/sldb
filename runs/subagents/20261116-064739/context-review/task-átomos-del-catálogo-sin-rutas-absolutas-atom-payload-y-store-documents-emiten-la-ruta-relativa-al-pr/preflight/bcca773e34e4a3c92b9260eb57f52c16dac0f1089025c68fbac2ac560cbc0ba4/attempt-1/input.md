FILE:desk/tasks/task-átomos-del-catálogo-sin-rutas-absolutas-atom-payload-y-store-documents-emiten-la-ruta-relativa-al-pr.md
---
sldb:
  by: agent
  at: '2026-11-16T06:19:24Z'
  authority: generated
  via: create_document
id: task-átomos-del-catálogo-sin-rutas-absolutas-atom-payload-y-store-documents-emiten-la-ruta-relativa-al-pr
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-004703-suggestion-sldb-matching-el-payload-de-tomos-del-cat-logo-incrusta-rutas-absolutas-path-y-store-en-atoms-db.md
depends_on: []
pills: []
files:
- src/sldb/api/matching/atom_payload.py
- src/sldb/api/matching/store_documents.py
- tests/matching/test_matching_explicit.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Átomos del catálogo sin rutas absolutas: atom_payload y store_documents emiten la ruta relativa al proyecto y no la del store

## Rationale

_Explain why this task exists or the business driver behind it._

sldb.api.matching.atom_payload (src/sldb/api/matching/atom_payload.py, la línea que arma entry["atoms"][question]) emite "path": str(doc_path) y "store": str(store_path) absolutos por átomo, y _document de src/sldb/api/matching/store_documents.py hace lo mismo con "store" y "path" (str(root / doc.path)). specir catalog build los vuelca en window.ATOMS_DB del HTML, así que un catálogo commiteado queda atado a la máquina y a la ubicación de cada repo (visto en MEPU en rendered/catalogo.html). Heredado de spec2viz, que se retira. Origen: desk/inbox/20261116-004703-suggestion-sldb-matching-el-payload-de-tomos-del-cat-logo-incrusta-rutas-absolutas-path-y-store-en-atoms-db.md.

## Goal

_Describe the concrete result this task must produce._

El payload de átomos y las filas de store_documents traen "path" relativo a la raíz del proyecto del store que tiene el documento (con "/" como separador) y ya no traen la ruta absoluta del store; un catálogo construido con ellos no contiene "/mnt/" ni "/home/".

## Scope

_State what is in scope and what is out of scope._

Entra: en atom_payload.py, "path" pasa a ser la ruta del documento relativa a la raíz del proyecto de su store (project_root del store, en formato posix) y se quita la clave "store"; en store_documents.py, "path" pasa a doc.path (ya relativo) en formato posix y "store" se reemplaza por "store_name" (que ya está) sin la ruta absoluta; revisar con grep -rn '"store"\]\|\["path"\]\|get("store")\|get("path")' src/sldb/api/matching src/sldb/api/notations los lectores de esas claves dentro de sldb y adaptarlos (si alguno necesita la ruta absoluta, la recompone con project_root). Tests en tests/matching/test_matching_explicit.py: el payload de un store en tmp_path no contiene str(tmp_path) en ningún valor y "path" es relativo. CHANGELOG.md con nota de cambio de forma para consumidores. No entra: specir (repo IR), que se avisa al cerrar.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer atom_payload.py, store_documents.py y sus usos (grep -rn "atom_payload\|store_documents\|atoms_from_documents" src/sldb). 2) Cambiar las claves. 3) Adaptar los lectores internos. 4) Test. 5) CHANGELOG y aviso a IR.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/matching/
- TMPDIR=/dev/shm pytest -q tests/notations/test_spec_catalog_sync.py

## Done When

_Name the observable condition that makes the task complete._

Los dos comandos pasan con el test nuevo; ningún valor del payload de prueba contiene la ruta de tmp_path; CHANGELOG y commit; aviso a IR con deskops message send --to IR (si el repo no está registrado para el envío, el aviso va como línea "Aviso a IR" en result-summary.md).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-átomos-del-catálogo-sin-rutas-absolutas-atom-payload-y-store-documents-emiten-la-ruta-relativa-al-pr: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

