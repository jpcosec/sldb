---
sldb:
  by: agent
  at: '2026-11-16T08:49:57Z'
  authority: generated
  via: save_document_payload
id: task-r6-el-tokenizer-y-el-parser-del-lenguaje-de-reglas-bajan-a-core-para-cerrar-la-arista-de-capas-model
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
pills:
- desk/contexts/pill-pill-alcance-real-del-traslado-del-parser-a-core.md
files:
- src/sldb/store/graph/language/predicate_tokens.py
- src/sldb/store/graph/language/predicate_cursor.py
- src/sldb/store/graph/language/predicate_parser.py
- src/sldb/store/graph/language/predicate_ast.py
- src/sldb/models/rule_doc.py
- contracts/layers.toml
- CHANGELOG.md
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-store-depende-del-resto-de-sldb-solo-por-costuras-y-un-test-lo-hace-cumplir
from_drawer: drawer task-r6-bajar-el-parser-del-lenguaje-de-reglas-a-la-capa-0-para-cerrar-la-arista-models-a-store
  (retirado en el triaje 2026-11-16; contenido en git antes del commit del triaje)
---

# R6: el tokenizer y el parser del lenguaje de reglas bajan a core para cerrar la arista de capas models -> store

## Rationale

_Explain why this task exists or the business driver behind it._

RuleDoc valida en pydantic que condition, where y subject parseen (src/sldb/models/rule_doc.py:61-64, _parse), con un import diferido de sldb.store.graph.language.predicate_parser. Eso es una arista hacia arriba de models a store, declarada como excepción en contracts/layers.toml: [allow].upward ["models", "store"] con comentario R6 (línea 89) y [[pending]] id="R6" (línea 164). WherePredicateError ya está en la capa 0 (src/sldb/core/exceptions/where_predicate_error.py). Hallazgo de GO06 (622da0b5). Origen: drawer desk/drawer/tasks/task-r6-bajar-el-parser-del-lenguaje-de-reglas-a-la-capa-0-para-cerrar-la-arista-models-a-store.md.

## Goal

_Describe the concrete result this task must produce._

predicate_tokens, predicate_cursor, predicate_parser y predicate_ast viven en un paquete de core (sldb.core.rules_language), sldb.store.graph.language los reexporta con los mismos nombres, rule_doc._parse importa de core, y contracts/layers.toml ya no tiene la excepción upward [models, store] ni el pending R6; python tools/check_layers.py pasa.

## Scope

_State what is in scope and what is out of scope._

Entra: mover los cuatro módulos de src/sldb/store/graph/language/ (predicate_tokens.py, predicate_cursor.py, predicate_parser.py, predicate_ast.py) y solo lo que ellos importen sin evaluación ni vistas, a un paquete nuevo sldb.core.rules_language; dejar en src/sldb/store/graph/language/ módulos con el mismo nombre que reexportan desde core, para que sigan funcionando los importadores actuales (api/search.py, api/rules/rule_writes.py, api/rules/dirty_set.py, api/rules/fixpoint.py, api/rules/rule_reach.py, cli/commands/find.py, models/notation/view_doc_checks.py, store/edge_index/validation.py, store/query_engine/rules.py); cambiar el import de rule_doc._parse a core y hacerlo de módulo (ya no diferido); borrar la línea upward R6 y el bloque [[pending]] R6 de contracts/layers.toml. Si alguno de los cuatro módulos necesita algo de store que no es parseo, la tarea se detiene y el informe dice qué. CHANGELOG.md. No entra: cambiar la gramática, el evaluador ni los mensajes de error; actualizar los importadores para que apunten a core (pueden seguir por el reexport).

Precisiones (preflight-1): se mueven los ocho módulos del parser: predicate_tokens, predicate_cursor, predicate_parser, predicate_ast, predicate_atoms, predicate_paths, predicate_terms y predicate_reach (los cuatro primeros importan a los demás). WherePredicateError se importa de sldb.core.exceptions (ya existe ahí). unquote, de sldb.store.query_engine.where_literal, se mueve a sldb.core.rules_language si es una función pura de texto, y where_literal la reimporta; si no es pura, la tarea se detiene. Si aparece cualquier otra dependencia de sldb.store, la tarea se detiene y el informe la lista. Cada módulo viejo queda como shim: from sldb.core.rules_language.<módulo> import * con el mismo __all__. Los importadores se verifican con grep -rn "store.graph.language" src/ tests/ y todos deben seguir funcionando por el shim. "Los tests" son los cinco comandos de Validation.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer contracts/layers.toml (líneas 80-170), rule_doc.py 55-70 y los cuatro módulos con sus imports. 2) git mv a src/sldb/core/rules_language/ y crear los reexports. 3) Cambiar rule_doc. 4) Editar layers.toml. 5) python tools/check_layers.py y los tests.

## Validation

_List the checks required before this task can close._

- python tools/check_layers.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rules.py
- TMPDIR=/dev/shm pytest -q tests/test_rules_language_spec.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rules_evaluation.py
- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los cinco comandos pasan; grep -n "R6" contracts/layers.toml no devuelve nada; rule_doc.py importa de sldb.core.rules_language; CHANGELOG y commit.
