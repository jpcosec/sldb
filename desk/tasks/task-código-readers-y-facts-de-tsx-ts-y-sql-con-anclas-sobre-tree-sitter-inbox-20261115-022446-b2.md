---
sldb:
  by: agent
  at: '2026-11-16T20:37:24Z'
  authority: generated
  via: save_document_payload
id: task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- pyproject.toml
- uv.lock
- src/sldb/code/runtime.py
- src/sldb/code/scan.py
- src/sldb/models/code_ref.py
- src/sldb/api/anchors/record_anchor.py
- tests/api/test_anchors.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb.code lee el frontend: TS, TSX, JS y JSX con un mismo reader sobre tree-sitter-typescript como extra (B2, parte TS; SQL va aparte)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR ancla cada nodo extraído a su fuente con las anclas de código de sldb y debe leer Django (Python, cubierto), SQL y React TSX/TS. Decisión de JP 2026-11-15: lo genérico va a sldb y specIR solo mapea al dominio (IR08 e IR09 quedan como mapeo sobre estos extractores).

## Goal

_Describe the concrete result this task must produce._

El paquete sldb.code lee TypeScript y JavaScript (.ts, .tsx, .js, .jsx) con un mismo reader, publica sus hechos de fuente con la misma forma que los de Python y soporta anclas code:<ruta>.<ext>::<símbolo>, con tree-sitter-typescript como parte del extra code; SQL lo hace la tarea hermana.

## Scope

_State what is in scope and what is out of scope._

Amplía el pedido parcial del inbox sldb 20261115-022446, que solo pedía anclas: aquí entran readers y facts, no solo anclas. Hoy el escáner recorre solo .py con tree-sitter-python (extra code); sldb.code tiene readers, facts, fingerprints, ids (src/sldb/code/ids.py), imports y scan.

Alcance (JP, 2026-11-16: el foco es el frontend): TypeScript y JavaScript, es decir .ts, .tsx, .js y .jsx, con un mismo reader en un módulo nuevo lang_ts.py del paquete sldb.code; solo cambia la gramática según la extensión (typescript para .ts; tsx para .tsx, .js y .jsx, porque la gramática tsx también parsea JavaScript). Hechos en la misma forma que los de Python (ver el atom del inventario de código como hechos de fuente). record_anchor y check_anchors usan la misma referencia code:<ruta>::<qualified_name>, con fingerprints por nodo, estados y reconexión. tree-sitter-typescript entra en el extra code. Se reutiliza la maquinaria existente de Python, sin duplicarla. Fuera de alcance: SQL (lo hace la tarea hermana que depende de esta), mapear a conceptos de dominio (eso es specIR) y cualquier cambio fuera del paquete sldb.code, salvo el registro de extensiones en code_ref y record_anchor que nombra Implementation Path.

Reglas de los hechos:
- kind component: declaración de función (function X, export function X, export default function X) o const/let con arrow function o function expression (const X = () => ..., const X = memo(() => ...), const X = forwardRef(...)), cuyo nombre empieza por mayúscula y cuyo cuerpo contiene al menos un nodo JSX en cualquier punto. Los reexports (export { X } from ...) no crean hechos.
- kind hook: misma forma que component, con nombre que empieza por use seguido de mayúscula; tiene prioridad sobre component.
- kind type: type alias o interface, solo en .ts y .tsx.
- kind function: cualquier otra declaración de función o const con arrow function del nivel superior del módulo.
- kind module: el archivo.
- Solo se leen las declaraciones del nivel superior del módulo, incluidas las exportadas; las funciones anidadas no crean hechos.
- docstring: el comentario /** ... */ cuyo final está en la línea inmediatamente anterior a la declaración, o a su export. No se admiten líneas en blanco en medio; los decoradores no cuentan como separación. El texto va sin los delimitadores ni los asteriscos de cada línea.
- qualified_name del módulo: la ruta sin extensión con '.' como separador, igual que py_module_name; el de un símbolo es módulo.nombre. Si dos archivos de la misma carpeta dan el mismo qualified_name de módulo (a.ts y a.js), se ordenan por ruta completa y del segundo en adelante llevan el sufijo ~2, ~3..., con la misma función de ids.py que ya desambigua nombres repetidos.
- NORMALIZATION no cambia si la salida de .py es la misma.

Lock: después de agregar tree-sitter-typescript a pyproject.toml, se corre uv lock (sin --frozen) una vez. Los comandos de Validation con --frozen se corren después, ya con el lock nuevo. Si uv.lock tiene cambios ajenos sin commitear, se anota y lo decide el coordinador.

La lista files nombra los archivos existentes que cambian. Los módulos nuevos (lang_ts.py) y los fixtures nuevos están autorizados por Implementation Path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) pyproject.toml: agregar tree-sitter-typescript>=0.23 al extra code (la versión 0.23.2 está en PyPI) y correr `uv lock` (único cambio de uv.lock: el paquete nuevo; si uv.lock tiene cambios ajenos sin commitear, el ejecutor lo anota y deja al coordinador decidir cómo commitear el lock). 2) src/sldb/code/runtime.py: un runtime por lenguaje elegido por extensión (.py con la gramática de Python; .ts con la gramática typescript; .tsx, .js y .jsx con la gramática tsx del mismo paquete, que también parsea JavaScript) en lugar del Language de Python fijo; si falta la gramática, TreeSitterUnavailable nombra el extra. 3) Un módulo nuevo lang_ts.py en el paquete sldb.code con la query, los readers (JSDoc /** */ como docstring) y los imports de TS/TSX; scan_file (src/sldb/code/scan.py, 78 líneas efectivas: la dispatch por extensión saca código a módulos nuevos) despacha por extensión y find_files incluye .ts/.tsx/.js/.jsx solo si la gramática está. 4) src/sldb/models/code_ref.py (parse_code_ref) acepta .ts, .tsx, .js y .jsx; src/sldb/api/anchors/record_anchor.py (recorded_with) informa la gramática del archivo. 5) Fixtures en tests/fixtures/treesitter/ con un componente .tsx, un hook y un tipo, más un .js con una función y un componente .jsx; tests de intact/changed/lost/reconnected que se saltan sin la gramática.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_agreement.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; un ancla code:<ruta>.tsx::<Componente> se registra y check_anchors la informa intact, changed al cambiar el cuerpo, lost al borrarla y reconnected al moverla; un ancla code:<ruta>.js::<función> del fixture JS se registra y queda intact; sldb sin tree-sitter-typescript sigue escaneando .py; la salida de los .py no cambia (NORMALIZATION igual); CHANGELOG y commit; aviso a IR por deskops message send --desk-root a su desk. La tarea hermana de SQL depende de esta.
