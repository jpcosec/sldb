---
sldb:
  by: agent
  at: '2026-11-16T06:18:23Z'
  authority: generated
  via: save_document_payload
id: task-el-oráculo-de-paridad-de-d2-deja-de-importar-spec2viz-golden-congelado-en-tests-notations
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-224828-suggestion-ir13-pide-migrar-lo-que-queda-de-sldb-sobre-spec2viz-or-culo-de-d2-vistas-yml-identity-toml.md
depends_on: []
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

Precisiones (preflight-1): la entrada es el árbol TREE y la fixture tree de tests/notations/test_component_spec_python.py, y la comparación viva es test_matches_spec2viz_on_modules_classes_and_defines, que compara _defined(spec) con _defined(python_ast.generate_python_ast_spec(tree)). El golden es un JSON con tres claves: "modules" y "classes" (los dos dicts de _defined) y "defines" (la lista ordenada de pares [from, to]), más "_source": la salida de `git -C /mnt/ssd/proyectos/SLDB_1/spec2viz rev-parse HEAD`. Se genera una vez con `PYTHONPATH=/mnt/ssd/proyectos/SLDB_1/spec2viz` sobre una copia de TREE escrita en un directorio temporal; la carpeta goldens se crea dentro de tests/notations. El test pasa a leer el golden y comparar contra _defined(spec) convertido a la misma forma. La comprobación "sin spec2viz" es: `python -c "import spec2viz"` falla en el entorno de la suite, o bien correr el test con PYTHONPATH=src y sin el checkout de spec2viz en sys.path. Solo se compara lo que hoy compara el test (módulos, clases, defines), no imports.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

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
