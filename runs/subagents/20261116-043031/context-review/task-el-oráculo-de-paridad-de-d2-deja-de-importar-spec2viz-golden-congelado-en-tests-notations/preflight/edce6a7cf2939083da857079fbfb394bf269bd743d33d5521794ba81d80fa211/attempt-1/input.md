FILE:desk/tasks/task-el-oráculo-de-paridad-de-d2-deja-de-importar-spec2viz-golden-congelado-en-tests-notations.md
---
sldb:
  by: agent
  at: '2026-11-16T04:22:25Z'
  authority: generated
  via: save_document_payload
id: task-el-oráculo-de-paridad-de-d2-deja-de-importar-spec2viz-golden-congelado-en-tests-notations
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-224828-suggestion-ir13-pide-migrar-lo-que-queda-de-sldb-sobre-spec2viz-or-culo-de-d2-vistas-yml-identity-toml.md
depends_on:
- task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas
pills: []
files:
- tests/notations/test_component_spec_python.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El oráculo de paridad de D2 deja de importar spec2viz: golden congelado en tests/notations

## Rationale

_Explain why this task exists or the business driver behind it._

IR13 (gate de retiro de spec2viz) pide migrar lo que queda de sldb sobre spec2viz. Los puntos 2 y 3 (vistas.yml e identity.toml) ya los cubre la tarea task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con. Queda el punto 1: tests/notations/test_component_spec_python.py:43 hace pytest.importorskip("spec2viz.generators.python_ast") y compara en vivo con spec2viz; sin spec2viz instalado el test se salta y la paridad deja de comprobarse. Origen: desk/inbox/20261115-224828-suggestion-ir13-pide-migrar-lo-que-queda-de-sldb-sobre-spec2viz-or-culo-de-d2-vistas-yml-identity-toml.md.

## Goal

_Describe the concrete result this task must produce._

La comparación de paridad corre siempre contra un golden versionado en tests/ y el archivo de test no importa spec2viz en ninguna rama.

## Scope

_State what is in scope and what is out of scope._

Entra: generar una sola vez, con spec2viz instalado, la salida de spec2viz.generators.python_ast para la entrada que hoy usa el test y guardarla como golden en el golden nuevo component_spec_python_spec2viz.json en la carpeta goldens de tests/notations (JSON con sort_keys=True e indent=2), con la clave "_source" que dice el commit de spec2viz del que salió; cambiar el test para comparar con ese golden; quitar el importorskip. Si spec2viz no está instalado en la máquina, generar el golden desde el checkout /mnt/ssd/proyectos/SLDB_1/spec2viz con PYTHONPATH, sin instalarlo. CHANGELOG.md. No entra: vistas.yml, identity.toml ni otros usos de spec2viz (tarea task-los-specs-de-docs-architecture-...), y cambiar component_spec_from_python (si la paridad falla con el golden, se reporta, no se ajusta el golden a mano).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/notations/test_component_spec_python.py, en especial la línea 43 y la función que compara. 2) Correr una vez el generador de spec2viz sobre la misma entrada y guardar su salida normalizada como golden. 3) Reemplazar la comparación viva por la lectura del golden. 4) grep -n spec2viz tests/notations/test_component_spec_python.py no devuelve imports. 5) CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_python.py
- ! grep -n 'import.*spec2viz\|importorskip("spec2viz' tests/notations/test_component_spec_python.py

## Done When

_Name the observable condition that makes the task complete._

El test pasa sin spec2viz importable (comprobado con python -c "import spec2viz" fallando o con PYTHONPATH sin spec2viz) y el grep de Validation no encuentra imports de spec2viz; golden y CHANGELOG commiteados.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-oráculo-de-paridad-de-d2-deja-de-importar-spec2viz-golden-congelado-en-tests-notations: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

