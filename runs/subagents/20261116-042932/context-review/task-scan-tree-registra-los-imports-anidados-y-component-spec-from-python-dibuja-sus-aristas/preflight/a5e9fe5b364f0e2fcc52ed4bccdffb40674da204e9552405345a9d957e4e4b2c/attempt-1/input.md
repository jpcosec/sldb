FILE:desk/tasks/task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas.md
---
sldb:
  by: agent
  at: '2026-11-16T04:02:32Z'
  authority: generated
  via: create_document
id: task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-203456-suggestion-code-scan-tree-nested-imports-component-spec-from-python-no-ve-los-from-imports-anidados.md
depends_on: []
pills: []
files:
- src/sldb/code/imports.py
- src/sldb/code/scan.py
- src/sldb/api/notations/component_spec_python.py
- tests/notations/test_component_spec_python.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-inventario-de-código-de-sldb-se-publica-como-hechos-de-fuente-y-cada-consumidor-los-proyecta
---

# scan_tree registra los imports anidados y component_spec_from_python dibuja sus aristas

## Rationale

_Explain why this task exists or the business driver behind it._

component_spec_from_python (src/sldb/api/notations/component_spec_python.py) arma las aristas imports del spec de componentes con attrs.imports de sldb.code.scan_tree, que solo trae las sentencias del nivel superior del módulo (py_imports en src/sldb/code/imports.py recorre root.named_children). spec2viz recorría todo el árbol y veía los imports dentro de funciones, if o try (imports perezosos, TYPE_CHECKING). En IR, specir/visual/commands.py importa compilers y lint_mermaid dentro de funciones y esas aristas faltan: el diagrama pierde dependencias reales. Origen: desk/inbox/20261115-203456-suggestion-code-scan-tree-nested-imports-component-spec-from-python-no-ve-los-from-imports-anidados.md.

## Goal

_Describe the concrete result this task must produce._

El spec de componentes generado desde Python incluye una arista imports por cada import anidado (dentro de def, class, if, try o with) además de los de nivel superior, sin cambiar los hechos de código (facts.rels) que ya consumen attrs.imports.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/code/imports.py una función que recorre el árbol completo y devuelve los imports anidados; en src/sldb/code/scan.py (líneas 58-61, donde se guarda attrs.imports) guardar esos imports en un attr aparte attrs.nested_imports, para no cambiar attrs.imports ni los facts que lo usan; en src/sldb/api/notations/component_spec_python.py (_module_elements línea 55, _imports línea 72) emitir aristas imports también desde nested_imports, deduplicadas contra las de nivel superior. Tests en tests/notations/test_component_spec_python.py (un módulo con import dentro de una función y otro bajo if TYPE_CHECKING producen la arista) y en tests/selfdoc/test_treesitter_symbols.py (attrs.imports no cambia; nested_imports aparece). CHANGELOG.md. No entra: marcar las aristas con estilo distinto en los renderers, cambiar facts.rels, ni el oráculo de paridad con spec2viz (tarea aparte del golden).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/code/imports.py (py_imports, línea 18) y src/sldb/code/scan.py 50-70. 2) Agregar py_nested_imports(root) que hace un recorrido completo y excluye los nodos hijos directos del módulo. 3) Guardar attrs["nested_imports"] en scan.py. 4) En component_spec_python.py unir imports y nested_imports al construir las aristas, sin duplicados. 5) Tests y CHANGELOG. Requiere el extra [code] (tree-sitter-python) instalado.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm pytest -q tests/selfdoc/test_treesitter_symbols.py

## Done When

_Name the observable condition that makes the task complete._

Los dos archivos de test pasan con los casos nuevos (import en función e import bajo TYPE_CHECKING generan arista imports; attrs.imports igual que antes); CHANGELOG con la entrada; commit con los archivos de Files.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

