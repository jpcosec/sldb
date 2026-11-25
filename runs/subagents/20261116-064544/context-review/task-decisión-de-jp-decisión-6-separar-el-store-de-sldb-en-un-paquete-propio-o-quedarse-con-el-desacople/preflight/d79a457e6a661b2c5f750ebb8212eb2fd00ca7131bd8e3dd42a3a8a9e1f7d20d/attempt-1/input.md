FILE:desk/tasks/task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio-o-quedarse-con-el-desacople.md
---
sldb:
  by: agent
  at: '2026-11-16T06:23:07Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio-o-quedarse-con-el-desacople
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- docs/architecture/store-extraction-proposal.md
- desk/STANDARDS.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-separar-el-store-en-un-paquete-propio-espera-la-decisi-n-6.md
---

# Decisión de JP (decisión 6): separar el store de sldb en un paquete propio o quedarse con el desacople interno

## Rationale

_Explain why this task exists or the business driver behind it._

El desacople del store dentro de sldb está hecho (beb8a99c): el store depende del resto de sldb solo por tres costuras (src/sldb/store/exceptions.py, src/sldb/store/runtime_codec.py, src/sldb/store/model_contract.py) y tests/test_store_seams.py lo hace cumplir. Separarlo en un paquete propio solo tiene sentido si el dueño decide que el store sea un motor genérico de documentos tipados para sldb, deskops, knowledge y repopackage. Esa es la decisión 6, pendiente según desk/STANDARDS.md:19. Spec: docs/architecture/store-extraction-proposal.md. Origen: drawer desk/drawer/tasks/task-separar-el-store-en-un-paquete-propio-espera-la-decisi-n-6.md.

## Goal

_Describe the concrete result this task must produce._

JP toma la decisión 6: (a) separar: se crea la tarea de refactor que inyecta las tres costuras y crea el paquete con su pyproject y su suite; o (b) quedarse con el desacople interno. La decisión queda escrita en docs/architecture/store-extraction-proposal.md, sección "Decisión 6", con fecha, y desk/STANDARDS.md:19 deja de decir que está pendiente (vía la CLI que corresponda o en el commit del doc si STANDARDS.md no es un documento modelado).

## Scope

_State what is in scope and what is out of scope._

Entra: presentar la decisión con el estado (costuras listas, test verde) y la recomendación del coordinador: (b) hasta que un segundo consumidor necesite el store sin sldb. Registrar el recibo owner (dispose accepted de JP), escribir la sección y crear la tarea si es (a). No entra: mover código.

Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.
Precisiones (preflight-1): desk/STANDARDS.md no es un documento modelado por deskops (no está en el store), así que se edita en el mismo commit que el doc: la línea que dice que la decisión 6 está pendiente pasa a decir "Decisión 6 (AAAA-MM-DD, JP): <opción>; ver docs/architecture/store-extraction-proposal.md". La recomendación es insumo para JP, no decisión por defecto.

Referencia kimun (solo lectura, github jpcosec/kimun main b14a30f): kimun es un solo producto (doc v2 de kimun 08-distribucion.md:11, "kernel SLDB v2 y modelos", un binario y un jar; deps.edn con un solo :paths) desacoplado por anillos que un script hace cumplir (doc v2 de kimun 03-estandares-de-codigo.md:10-17, bb lint / scripts/check_rings.clj). La separación que kimun planea no es "el store como motor genérico de documentos", sino base frente a grafo: "el grafo es un paquete aparte de la base" (05-estado.md:120, decisión 43). Y "kimun no tiene consumidores en código" (12-ecosistema-y-pendientes.md:71). Recomendación para que JP confirme: (b), quedarse con el desacople interno, que sldb ya hace cumplir con tests/test_store_seams.py y contracts/layers.toml. Se reabre si aparece un segundo consumidor que necesite el store sin sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer docs/architecture/store-extraction-proposal.md y desk/STANDARDS.md. 2) Pedir la decisión. 3) Escribir la sección y actualizar STANDARDS.md. 4) Crear la tarea de refactor si es (a).

## Validation

_List the checks required before this task can close._

- grep -n 'Decisión 6' docs/architecture/store-extraction-proposal.md
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la decisión y la fecha; STANDARDS.md ya no la da por pendiente; recibo owner aceptado por JP; tarea de refactor creada si es (a); commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio-o-quedarse-con-el-desacople: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

