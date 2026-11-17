---
sldb:
  by: agent
  at: '2026-11-17T13:12:27Z'
  authority: generated
  via: save_document_payload
id: task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam
status: draft
summary: 'BLOQUEADA 2026-11-17 tras 2 ciclos de corrección (tester FALLA en intento
  1, c1 y c2). Resuelto: await, type args, espacios, cadenas en varias líneas, ''()'',
  ''(fn)'', ''[]'', first_arg y handlers; facts existentes idénticos a HEAD. Pendiente:
  cuando el objeto de la cadena es un array, binario, new o literal, el nombre sale
  como texto sin espacios y puede ser erróneo (new Set(xs) -> newSet(xs); (a ?? []).map
  -> a??[].map; ''a b''.split -> ''ab''.split): 123 de unos 2000 nombres en tres frontends
  reales. Propuesta: un ciclo más con marcadores fijos para esas expresiones ([...],
  (expr), (lit)) en ts_callee.py; necesita OK del supervisor. Diff guardado en runs/subagents/20261116-exec-k4-c2/executor-diff-c3ts-c2.patch
  (reaplicable); informes en runs/subagents/20261116-test-k4*/.'
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md
depends_on:
- task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre
pills: []
files:
- src/sldb/code/lang_ts.py
- src/sldb/code/ts_readers.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
---

# sldb.code publica facts genéricos de TS, TSX, JS y JSX: llamadas entre símbolos, llamadas HTTP como llamadas y handlers JSX (C3 de IR para IR09)

## Rationale

_Explain why this task exists or the business driver behind it._

IR09 (frontend) necesita los componentes, sus handlers y sus llamadas HTTP. Los componentes ya salen (B2); faltan las llamadas y los handlers. Misma decisión que la parte de Python: sldb publica hechos sintácticos genéricos y specIR los interpreta. Origen: desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md.

## Goal

_Describe the concrete result this task must produce._

Los facts de TS, TSX, JS y JSX llevan las llamadas que hace cada función, componente o hook (fetch(...), axios.get(...), api.posts.create(...) y llamadas a otros símbolos) con su primer argumento literal si lo hay, y los atributos JSX que ligan un evento a un handler (onClick={handleSave}), sin conocer ningún framework.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) relación calls desde cada función, componente o hook hacia cada nombre llamado (texto calificado tal cual); attrs.calls con {func, line, first_arg} donde first_arg es el texto de un primer argumento literal (string o template sin expresiones) o null. (2) attrs.handlers en componentes: lista de {element, attribute, handler} para atributos JSX que empiezan por on y cuyo valor es un identificador o una llamada; relación calls también hacia ese handler. (3) Mismas convenciones de forma que la tarea de Python (si esa ya cerró, seguir su forma exacta). Fixture con un componente que hace fetch y axios y tiene un botón con onClick; tests. CHANGELOG. No entra: interpretar REST ni frameworks, resolver imports, Python.

Precisiones (intento 2): esta tarea depende de la de facts genéricos de Python y sigue su forma exacta para calls, attrs.calls y kwargs cuando aplique. El destino de una relación calls es el texto completo de la expresión llamada como un solo nombre (api.posts.create, axios.get, fetch), sin partirlo. first_arg es el valor del literal sin comillas ni backticks (/api/posts, no '/api/posts'); un template con expresiones da null. element es el nombre del tag JSX tal como está escrito (button, Button, Form.Item). Los readers nuevos van en módulos nuevos del paquete sldb.code; están autorizados aunque no figuren en files.

Precisiones (corrección 2, tras dos testers): forma canónica del nombre de una llamada (name en attrs.calls y destino de la relación calls). Se arma desde el árbol, no desde el texto: identificadores y nombres de propiedad unidos por '.' (con '?.' y '!' si están escritos), sin espacios ni saltos de línea, sin await y sin argumentos de tipo. Si un tramo de la cadena es a su vez una llamada, se escribe con '()' sin sus argumentos (fetch(url).then(cb).then -> fetch().then().then; (await listDocuments(m)).slice -> listDocuments().slice). Una función anónima o una IIFE como objeto se escribe '(fn)'. Un acceso por índice se escribe '[]'. Los handlers JSX son atributos 'on' seguidos de mayúscula. El diff de los intentos anteriores está en el árbol o en runs/subagents/20261116-exec-k4-c1/ y es el punto de partida.

Decisión del supervisor (2026-11-17, prevalece): no se busca la forma canónica de los nombres cuya cadena empieza en un array, una expresión binaria, un new, un literal u otra expresión que no sea identificador, this, super, llamada, miembro, índice, non-null o función. Esas llamadas se emiten igual en attrs.calls con canonical: false y name igual al texto de la expresión llamada con cada tramo de espacios en blanco colapsado a un solo espacio (no borrado), sin await ni type args; las canónicas llevan canonical: true. La relación calls solo se emite para nombres canónicos, para no poner en el grafo destinos que no son símbolos. Nada se omite en silencio. Canonizarlos queda para una tarea aparte de baja prioridad. El punto de partida es el diff guardado en runs/subagents/20261116-exec-k4-c2/executor-diff-c3ts-c2.patch.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/code/lang_ts.py, ts_readers.py y ts_fingerprints.py, y la forma de calls de la tarea de Python si ya cerró. 2) Readers nuevos en módulos nuevos del paquete sldb.code. 3) Fixture en tests/fixtures/treesitter/frontend/src/ y tests en tests/selfdoc/test_treesitter_symbols.py. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; sobre el fixture salen las llamadas fetch y axios con su URL literal, la llamada del componente a su handler y el handler onClick en attrs.handlers; en los tres frontends reales del workspace (solo lectura) todo name canónico cumple la forma canónica y todo name no canónico lleva canonical: false, sin espacios dobles, sin await y sin type args; ningún destino de la relación calls es no canónico; las anclas TS existentes no cambian de estado; CHANGELOG y commit; aviso a IR.
