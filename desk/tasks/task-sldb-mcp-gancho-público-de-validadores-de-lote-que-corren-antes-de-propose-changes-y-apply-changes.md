---
sldb:
  by: agent
  at: '2026-11-16T07:43:46Z'
  authority: generated
  via: save_document_payload
id: task-sldb-mcp-gancho-público-de-validadores-de-lote-que-corren-antes-de-propose-changes-y-apply-changes
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-182013-suggestion-sldb-mcp-gancho-p-blico-de-comprobaciones-de-dominio-antes-de-propose-changes.md
depends_on: []
pills:
- desk/contexts/pill-pill-forma-del-rechazo-de-dominio-en-sldb-mcp.md
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

Precisiones (preflight-1): diseño elegido: build_server pasa el ServerContext a WriteTools (parámetro context), y WriteTools lee context.batch_validators en cada llamada. En propose_changes los validadores corren después de self._require y _check_path y antes de construir el lote; en apply_changes corren después de require y sealer.check, sobre proposal.changes. Se corren todos los validadores siempre (no se corta en el primer error). Si hay algún error, la respuesta es apply.rejected("domain", "<n> domain check(s) failed", findings=<todos los findings, errores y alertas>) y no se escribe. Si solo hay alertas, la respuesta normal gana una clave "domain_alerts" con la lista. El contrato se documenta en docs/architecture/mcp.md.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

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
