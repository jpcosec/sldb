---
sldb:
  by: agent
  at: '2026-11-16T08:47:07Z'
  authority: generated
  via: save_document_payload
id: task-una-sola-forma-de-serializar-un-escalar-al-sustituir-llaves-effects-go09-y-where-subject-usan-la-mis
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
- src/sldb/store/query_engine/where_literal.py
- src/sldb/store/query_engine/where_subject.py
- src/sldb/api/edges/edge_effects.py
- tests/store/test_predicate_language.py
- tests/api/test_edge_effects.py
- CHANGELOG.md
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-evaluates-declared-rules-consumers-author-them
from_drawer: drawer task-dos-formas-de-serializar-un-escalar-al-sustituir-llaves-effects-de-go09-y-where-subject
  (retirado en el triaje 2026-11-16; contenido en git antes del commit del triaje)
---

# Una sola forma de serializar un escalar al sustituir llaves: effects (GO09) y where_subject usan la misma función

## Rationale

_Explain why this task exists or the business driver behind it._

La sustitución {campo} tiene dos serializadores: src/sldb/api/edges/edge_effects.py:38-44 (_written) usa yaml.safe_dump (1e20 da 1.0e+20, booleanos true/false, y hoy una fecha lanza LookupError), mientras src/sldb/store/query_engine/where_literal.py:47-51 (scalar_literal, usado por fill_braces de src/sldb/store/query_engine/where_subject.py:19) usa Decimal sin exponente y devuelve None para booleanos. El mismo valor sale distinto según dónde se sustituya. Hallazgo de GO09 (H3, H4). Origen: drawer desk/drawer/tasks/task-dos-formas-de-serializar-un-escalar-al-sustituir-llaves-effects-de-go09-y-where-subject.md.

## Goal

_Describe the concrete result this task must produce._

Existe una función brace_text(value) -> str en src/sldb/store/query_engine/where_literal.py que usan tanto edge_effects._written como fill_braces, con estas salidas exactas: int y Decimal sin exponente (1e20 -> 100000000000000000000), float con repr más corto sin exponente cuando sea posible (0.5 -> 0.5), bool -> true/false, datetime.date -> ISO 8601 (2026-11-16), str tal cual; cualquier otro tipo lanza TypeError con el tipo.

## Scope

_State what is in scope and what is out of scope._

Entra: escribir brace_text, cambiar _written y scalar_literal/fill_braces para usarla, y tests parametrizados con los cinco casos de Goal en tests/store/test_predicate_language.py y tests/api/test_edge_effects.py (mismo valor, mismo texto por los dos caminos). Si un test existente esperaba 1.0e+20 o None para bool, se actualiza al formato nuevo y el commit lo dice. CHANGELOG.md. No entra: cambiar la gramática del lenguaje de reglas ni los literales que el parser acepta.

Precisiones (preflight-1): orden de despacho: bool antes que int; datetime.datetime -> isoformat() completo antes que date; date -> isoformat(); int -> str(int); Decimal -> format(d, "f") (fraccionarios, negativos y ceros finales tal cual los da "f"; NaN e Infinity lanzan ValueError con el valor); float -> repr(f) si no contiene "e", y si contiene "e" -> format(Decimal(repr(f)), "f"); str -> tal cual. Mensaje de TypeError: "cannot write {type(value).__name__} into braces". scalar_literal se queda y llama a brace_text para los escalares (sigue devolviendo None para los tipos que hoy no maneja, salvo bool, que ahora da true/false).

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer edge_effects.py 30-50, where_literal.py 40-60 y where_subject.py 1-40. 2) Escribir brace_text. 3) Usarla en los dos caminos. 4) Tests. 5) Correr los tres archivos de Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_edge_effects.py
- TMPDIR=/dev/shm pytest -q tests/store/test_predicate_language.py
- TMPDIR=/dev/shm pytest -q tests/store/test_where_empty_and_errors.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan; grep -n "safe_dump" src/sldb/api/edges/edge_effects.py ya no aparece en _written; los cinco casos dan el mismo texto por effects y por where_subject; CHANGELOG y commit.
