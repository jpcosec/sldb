---
sldb:
  by: agent
  at: '2026-11-25T06:05:02Z'
  authority: generated
  via: create_document
id: task-sldb-serve-acepta-extension-module-function-y-la-extension-registra-rutas-get-de-solo-lectura-bajo-e
status: draft
summary: ''
tags: []
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

# sldb serve acepta --extension MODULE:FUNCTION y la extension registra rutas GET de solo lectura bajo /ext/<nombre>/

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de IR 20261125-030337-suggestion-sldb-serve-acepta-extension-module-function-como-sldb-mcp-para-que-specir-registre-rutas-http-de-solo-lectura (D8 de JP, plan graph_ui): la UI de specIR lee por HTTP de sldb serve y specIR necesita exponer impacto, reglas y controles sin que sldb lo importe, como ya hace sldb mcp --extension.

## Goal

_Describe the concrete result this task must produce._

Que sldb serve cargue extensiones por nombre y les deje registrar rutas GET bajo un prefijo propio, con acceso al store servido.

## Scope

_State what is in scope and what is out of scope._

src/sldb/cli/parsers/serve.py, el arranque de serve (http_server.py) y routes.dispatch_get, y un test. Fuera: escritura por extensiones, auth nueva, cambios a sldb mcp.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/sldb. Copiar el patron de sldb mcp: src/sldb/cli/parsers/mcp.py:14 declara --extension action=append metavar MODULE:FUNCTION, y src/sldb/mcp/server.py (build_server(..., extensions=...), serve) importa MODULE y llama FUNCTION(server, context). Para serve: --extension repetible en src/sldb/cli/parsers/serve.py; al arrancar, por cada una, importlib.import_module(MODULE) y FUNCTION(registry, context) donde registry.get(name, path, fn) registra una ruta GET '/ext/<name>/<path>' y context da store_path, project_root y pythonpath; fn(query: dict) -> (payload: dict, status: int). dispatch_get (src/sldb/cli/serve/routes.py) consulta el registro antes del 404 para rutas que empiezan con /ext/. Error legible al arrancar si MODULE:FUNCTION no importa o FUNCTION no existe. Un POST a /ext/... da 405. Test nuevo tests/serve/test_serve_extension.py (o junto a los tests de serve existentes): un modulo de extension de prueba en tmp_path (en sys.path) registra /ext/demo/ping que devuelve el nombre del store; build_handler/dispatch con esa extension responde 200 con el payload, una ruta /ext/demo/otra da 404, POST da 405 y una extension inexistente falla al arrancar con mensaje que la nombra.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/serve/test_serve_extension.py

## Done When

_Name the observable condition that makes the task complete._

sldb serve --extension carga la extension, sus GET responden bajo /ext/<nombre>/, POST da 405, y el test nuevo pasa.
