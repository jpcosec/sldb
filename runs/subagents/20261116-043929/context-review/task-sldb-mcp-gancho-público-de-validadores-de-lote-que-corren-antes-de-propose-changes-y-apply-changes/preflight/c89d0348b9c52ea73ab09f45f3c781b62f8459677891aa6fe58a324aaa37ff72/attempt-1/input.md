FILE:desk/tasks/task-sldb-mcp-gancho-público-de-validadores-de-lote-que-corren-antes-de-propose-changes-y-apply-changes.md
---
sldb:
  by: agent
  at: '2026-11-16T04:07:14Z'
  authority: generated
  via: create_document
id: task-sldb-mcp-gancho-público-de-validadores-de-lote-que-corren-antes-de-propose-changes-y-apply-changes
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-182013-suggestion-sldb-mcp-gancho-p-blico-de-comprobaciones-de-dominio-antes-de-propose-changes.md
depends_on: []
pills: []
files:
- src/sldb/mcp/context.py
- src/sldb/mcp/extension.py
- src/sldb/mcp/server.py
- src/sldb/mcp/write/tools.py
- tests/mcp/test_extension.py
- tests/mcp/example_extension.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb mcp: gancho público de validadores de lote que corren antes de propose_changes y apply_changes

## Rationale

_Explain why this task exists or the business driver behind it._

IR03b monta specir.mcp_extension:register sobre sldb mcp y necesita una regla de dominio antes de proponer cambios (claims_verified, IR05 D2-E: un agente no escribe verificacion: verificado por el MCP). Hoy la extensión quita propose_changes/apply_changes y los vuelve a registrar desde WriteTools con su comprobación, importando internos de sldb.mcp (changes, paging, registry, write). build_server (src/sldb/mcp/server.py:38) solo acepta extensiones Callable[[server, context], None] (src/sldb/mcp/extension.py) y no hay forma de enganchar un validador. Origen: desk/inbox/20261115-182013-suggestion-sldb-mcp-gancho-p-blico-de-comprobaciones-de-dominio-antes-de-propose-changes.md.

## Goal

_Describe the concrete result this task must produce._

Una extensión registra validadores con context.add_batch_validator(fn), donde fn(changes, context) -> list[dict] devuelve findings; propose_changes y apply_changes de WriteTools llaman a todos los validadores antes de su trabajo y, si algún finding tiene level "error", responden rechazado con esos findings y no escriben; los de level "alert" se devuelven en la respuesta sin bloquear.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/mcp/context.py (ServerContext) una lista batch_validators y el método add_batch_validator(fn); BatchValidator = Callable[[list, ServerContext], list[dict]] definido en src/sldb/mcp/extension.py junto a Extension; en src/sldb/mcp/server.py build_server pasa el context a WriteTools (o WriteTools recibe la lista de validadores) y las extensiones se aplican antes de que se sirva la primera llamada; en src/sldb/mcp/write/tools.py propose_changes y apply_changes corren los validadores sobre los changes (en apply, sobre proposal.changes) antes de sellar o aplicar. Un finding es {"code", "level", "what", "subject"} con level en {"error", "alert"}; un rechazo usa apply.rejected("domain", ...) con los findings en detail. Documentar el contrato estable de extensión (Extension, BatchValidator, ServerContext.add_batch_validator) en docs/architecture/ en el doc donde ya se describe sldb mcp. Tests en tests/mcp/test_extension.py: un validador que devuelve error bloquea propose y apply sin escribir; uno con alert deja pasar y aparece en la respuesta; sin validadores el comportamiento es el de hoy. Actualizar tests/mcp/example_extension.py con un validador de ejemplo. CHANGELOG.md. No entra: mover sldb.mcp a sldb.api, cambiar el sellado de propuestas, ni tocar el repo IR.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/mcp/server.py, extension.py, context.py, write/tools.py, write/apply.py y tests/mcp/test_extension.py, tests/mcp/example_extension.py. 2) Agregar BatchValidator y add_batch_validator. 3) Conectar WriteTools con el context. 4) Correr validadores en propose y apply. 5) Tests y doc. 6) grep "mcp" docs/architecture para elegir el doc donde va el contrato.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/mcp/test_extension.py
- TMPDIR=/dev/shm pytest -q tests/mcp/test_write_tools.py

## Done When

_Name the observable condition that makes the task complete._

Los dos archivos de test pasan con los tres casos nuevos; el contrato de extensión está documentado; CHANGELOG y commit; mensaje a IR con deskops message send --to IR (si ese repo no está registrado para el envío, el aviso va como línea "Aviso a IR" en el informe de cierre) avisando el gancho.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-mcp-gancho-público-de-validadores-de-lote-que-corren-antes-de-propose-changes-y-apply-changes: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

