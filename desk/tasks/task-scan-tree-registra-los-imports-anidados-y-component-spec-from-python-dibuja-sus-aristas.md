---
sldb:
  by: agent
  at: '2026-11-16T07:36:21Z'
  authority: generated
  via: save_document_payload
id: task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-203456-suggestion-code-scan-tree-nested-imports-component-spec-from-python-no-ve-los-from-imports-anidados.md
depends_on: []
pills:
- desk/contexts/pill-pill-imports-anidados-en-scan-tree.md
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

Precisiones (preflight-1): una sola arista imports por par (módulo fuente, módulo destino), aunque el destino se importe en varias funciones o también en el nivel superior; "anidado" es toda sentencia import o from-import que no es hijo directo del nodo module del árbol de tree-sitter, incluidas las que están dentro de if TYPE_CHECKING, try, def, class o with en el nivel del módulo. Test nuevo en tests/notations/test_component_spec_python.py: agregar al dict TREE un módulo "pkg/lazy.py" con "def f():\n    from pkg.sub import b\nif False:\n    import json\n" y comprobar que ("module_pkg_lazy", "module_pkg_sub_b") y ("module_pkg_lazy", "module_json") están en las aristas imports.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

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
