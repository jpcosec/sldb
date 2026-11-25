FILE:desk/tasks/task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre.md
---
sldb:
  by: agent
  at: '2026-11-17T07:38:22Z'
  authority: generated
  via: save_document_payload
id: task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md
depends_on: []
pills: []
files:
- src/sldb/code/scan.py
- src/sldb/code/readers.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb.code publica facts genéricos de Python: bases de clase, decoradores con argumentos, llamadas entre símbolos y asignaciones de clase con llamada (C3 de IR, parte genérica)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR necesita derivar de un proyecto Django/DRF las rutas (path(), router.register()), las acciones (@action(detail, methods)), las bases de clase (models.Model, ModelViewSet, ModelSerializer), los campos de modelo con tipo, choices, ForeignKey y Meta.db_table, Meta.model y Meta.fields de serializers, y las llamadas entre símbolos (handler -> Post.publish -> can_publish). Hoy sldb.code solo da módulos, clases, funciones y métodos. Decisión del coordinador (reversible, alineada con el pill keep-sldb-generic y con el alcance de B2, donde mapear a conceptos de dominio es de specIR): sldb publica los hechos sintácticos genéricos y specIR los interpreta como Django/DRF. Origen: desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md.

## Goal

_Describe the concrete result this task must produce._

Los facts de Python llevan, sin conocer ningún framework: las bases de cada clase, los decoradores de cada definición con sus argumentos, las llamadas que hace cada función o método a otros nombres, y las asignaciones a nivel de módulo o de clase cuyo valor es una llamada (nombre, función llamada y argumentos), incluidas las de una clase anidada como Meta; con eso specIR reconstruye rutas, campos, serializers y cadenas de llamadas de un proyecto Django/DRF.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) relación extends desde la clase hacia cada base escrita (texto calificado tal cual, p. ej. models.Model). (2) attrs.decorators: lista de {name, args, kwargs} con los argumentos como texto normalizado. (3) relación calls desde cada función o método hacia cada nombre llamado (texto calificado tal cual: self.publish, Post.objects.create, can_publish), sin resolver tipos; attrs.calls con línea de cada llamada. (4) un kind nuevo assignment para asignaciones de nivel de módulo o de clase (incluida una clase anidada como Meta) cuyo valor es una llamada o un literal simple: name, attrs.call {func, args, kwargs} o attrs.value, contenido en su clase o módulo; así salen urlpatterns = [path(...)], router.register(...) como llamada de módulo (kind call, con func y args), title = models.CharField(max_length=200, choices=...), model = Post y fields = [...]. (5) NORMALIZATION: si cambia la forma de los facts existentes, se sube y se dice en el CHANGELOG. Fixture de Django/DRF mínimo en tests/fixtures/treesitter/ con models, serializers, views con @action, urls con path() y router.register(), y tests. CHANGELOG. No entra: interpretar Django o DRF (es specIR), resolver tipos o imports de las llamadas, TS/JS (otra tarea).

Precisiones (intento 2): (a) Una sentencia de módulo o de clase que es solo una llamada (router.register(...)) es un hecho kind call con attrs.call {func, args, kwargs}. Una asignación (nombre = valor) es kind assignment: si el valor es una llamada, attrs.call; si es una lista o tupla, attrs.items con un elemento por ítem, cada uno {func, args, kwargs} si es llamada o {value} si no (así urlpatterns = [path(...), path(...)] da dos ítems); si es un literal simple, attrs.value. (b) Literal simple: str, bytes, int, float, bool, None, un nombre o atributo con puntos (model = Post) y listas o tuplas de esos (fields = ["id", "title"]). Lo que no sea llamada, lista/tupla ni literal simple da attrs.value con su texto. (c) Todo texto de bases, func, args, kwargs y value se normaliza con py_norm, la misma función que usa signature; kwargs es un dict nombre -> texto. (d) El hecho call de módulo se nombra por su func con sufijo ~N si se repite.

Precisiones (corrección 2, tras dos testers): (1) Los facts nuevos (assignment, call) toman su id después de todos los existentes (Ids.take_late y flush), en scan_tree, scan_file y code_facts; los facts que ya existían conservan el id de HEAD. (2) Una asignación aumentada (nombre += valor y los demás operadores) también es kind assignment, con attrs.op igual al operador ('+=') y el valor leído igual que en '=' (call, items o value); así urlpatterns += [path(...)] da sus ítems. (3) Una asignación encadenada (a = b = valor) da un fact por cada nombre, con el mismo valor. (4) Lo que siga fuera queda documentado en el docstring de py_statements.py. El diff de los intentos anteriores está guardado en runs/subagents/20261116-exec-k3-c1/executor-diff-c3py-c1.patch y es el punto de partida.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/code/readers.py, scan.py, facts.py y fingerprints.py. 2) Escribir los readers nuevos en módulos nuevos del paquete sldb.code (por la regla de 80 líneas). 3) Integrarlos en scan_file para .py. 4) Fixture y tests en tests/selfdoc/test_treesitter_symbols.py. 5) Comprobar que tests/selfdoc/test_treesitter_agreement.py y tests/notations/test_component_spec_python.py siguen pasando. 6) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_agreement.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; sobre el fixture de Django/DRF salen las bases, los decoradores @action con sus argumentos, las llamadas handler -> método -> función, los campos de modelo como assignment con su llamada y argumentos, Meta.db_table, Meta.model y Meta.fields, y las llamadas path() y router.register() de urls; las anclas existentes no cambian de estado; CHANGELOG y commit; aviso a IR.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

