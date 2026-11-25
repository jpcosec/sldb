FILE:desk/tasks/task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e.md
---
sldb:
  by: agent
  at: '2026-11-15T15:50:32Z'
  authority: generated
  via: create_document
id: task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb mcp: servidor MCP genérico (niveles 0/1/2, propose/apply, log de señales) migrado desde specIR, con extra opcional mcp

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: nunca reimplementar en un consumidor lo que es de sldb. El servidor MCP de specIR no tiene nada de dominio: lee y escribe un store solo por sldb.api. Debe vivir en sldb y specIR montar encima sus tools de dominio.

## Goal

_Describe the concrete result this task must produce._

Comando 'sldb mcp --store <dir> --level 0|1|2 --actor <quien>' servido por stdio, instalable como extra opcional 'mcp' del paquete sldb, con las tools de lectura y de escritura de specIR migradas (no reescritas), el log de señales y un punto de extensión para tools de consumidores.

## Scope

_State what is in scope and what is out of scope._

SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE. Origen: el paquete mcp de specIR (repo IR, main 82c79d6 para escritura IR04 y 14f6f24 para lectura IR03; módulos server, read_tools, write_tools, changes, mutability, addresses, paging) y sus tests (test_read_tools, test_no_writes, test_dry_run, test_mutability, test_write_tools, writing, más las fixtures de conftest que usan). Leerlos antes de escribir nada. Tools de lectura (nivel 0, todas read-only e idempotentes): list_models, describe_model, list_relation_types, describe_relation_type, read_document, select_documents, neighbors, neighborhood, list_views, resolve_view, check_integrity; JSON estructurado, dirección estable sldb://document/<export_id>, conjuntos paginados {items,total,offset,limit,truncated,next_offset}. Tools de escritura (nivel 1 contenido, nivel 2 reglas como dato; el nivel lo fija el operador al arrancar, nunca un argumento de tool; los modelos como código nunca se sirven): propose_changes (ejecución en seco con las guardas expected_source_hash puestas por el servidor, no escribe) y apply_changes (la propuesta tal cual; todo o nada, rechazo con causa stale o rules) sobre sldb.api.apply_batch; --actor firma la procedencia. Adaptación: quitar de lo migrado todo lo específico de specIR (nombres, tests que dependen de la federación spec2viz o de tareas concretas del board de IR: reescribir la fuente de verdad de esos tests contra el propio store de sldb, sin literales que repitan la respuesta). Extra opcional 'mcp' en pyproject (dependencia mcp>=2.2), importación perezosa para que sldb sin el extra siga funcionando y 'sldb mcp' diga cómo instalarlo; subcomando registrado en la CLI respetando contracts/layers.toml. LOG DE SEÑALES (decisión de JP, punto 3): cada consulta que pide algo que no existe o que se llama distinto se registra, y no es un error: tool desconocida, modelo, documento, campo, tipo de relación o vista inexistente, argumento no reconocido. La respuesta dice 'no implementado / no existe, registrado como señal' y sugiere nombres cercanos con sldb.api.matching (no un matcher nuevo). Cada entrada lleva momento, tool, argumentos, clase de señal, sugerencias y actor si lo hay. Se lee con una tool del MCP (por ejemplo list_signals, paginada como las demás). Funciona también en nivel 0: el log no es una escritura del store ni de los almacenados, así que no rompe la prueba de que leer no escribe. El worker decide dónde vive (runtime o caché del store, fuera de los documentos trackeados) y lo justifica en el informe de cierre. PUNTO DE EXTENSIÓN: una función pública (por ejemplo build_server con un registro de extensiones) para que un consumidor, specIR, registre tools de dominio encima del servidor de sldb sin copiarlo, heredando niveles, actor, paginación y log de señales; con un test que registra una tool de ejemplo. DESHACER: conecta con el pedido de sldb en el inbox 20261115-123855 (apply_batch devuelve el lote inverso con guardas, deshacer es de sldb por decisión de JP). Esta tarea no implementa el inverso en sldb.api; cuando ese pedido se resuelva, el MCP expone una tool undo_changes que reaplica el inverso; dejar el punto preparado y declarado como pendiente. Tests portados: cliente MCP real por stdio contra el servidor real, sobre copia aislada del store, comprobación de que leer no escribe (digest del store y de los enlazados antes y después), niveles, rechazo stale, reglas, aristas contra su tipo de relación. Sin mocks. Documentar en docs y CHANGELOG.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer el origen en IR y listar qué importa de specir (debería ser solo sldb.api y mcp). 2) Copiar los módulos al paquete sldb con el mínimo cambio y portar los tests. 3) Registrar 'sldb mcp' en la CLI y el extra mcp. 4) Añadir el log de señales y list_signals con sugerencias de sldb.api.matching. 5) Añadir el punto de extensión con su test. 6) Documentar el pedido de deshacer como pendiente conectado al inbox 20261115-123855. 7) Suite completa de a un archivo, tools/check.sh y stores build --check.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de cada archivo de tests tocado y después de cada tests/*.py de a uno
- tools/check.sh
- sldb stores build --check
- deskops graph missing sin referencias nuevas

## Done When

_Name the observable condition that makes the task complete._

Existe 'sldb mcp --store --level --actor' que sirve por stdio las once tools de lectura, propose_changes y apply_changes según el nivel, y list_signals; el código viene migrado del servidor de specIR y no reescrito; los tests portados pasan con cliente MCP real; leer (incluido registrar señales) no escribe en el store; el punto de extensión lo prueba una tool de ejemplo; el informe justifica dónde vive el log de señales. La suite de sldb completa pasa (pytest de a un archivo con TMPDIR=/dev/shm, tools/check.sh, sldb stores build --check).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

