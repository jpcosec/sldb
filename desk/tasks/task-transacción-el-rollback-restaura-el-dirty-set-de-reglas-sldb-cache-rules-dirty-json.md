---
sldb:
  by: agent
  at: '2026-11-09T16:53:13Z'
  authority: generated
  via: save_document_payload
id: task-transacción-el-rollback-restaura-el-dirty-set-de-reglas-sldb-cache-rules-dirty-json
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/api/documents/transaction_state.py
- src/sldb/api/documents/transaction_ops.py
- src/sldb/api/documents/transaction_paths.py
- src/sldb/api/rules/dirty_set.py
- src/sldb/api/rules/rules_on_write.py
- tests/api/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-transacci-n-rollback-falla-con-ruledoc-por-sldb-cache-rules-dirty-json-sin-snapshot.md
---

# transacción: el rollback restaura el dirty set de reglas (.sldb_cache/rules/dirty.json)

## Rationale

_Explain why this task exists or the business driver behind it._

Hallazgo de deskops CC32 (gates de activación como RuleDoc), sobre la transacción de GD24 y el dirty set de GO08. Nota de deskops promovida a este drawer (d72db524). En un store con RuleDoc y un dirty set (.sldb_cache/rules/dirty.json), toda transacción que falla sale como RollbackError en lugar del error original. Esto bloquea la integración de CC32 en deskops: dos tests de test_transaction de deskops en wt/cc32 c9af867e.

## Goal

_Describe the concrete result this task must produce._

El rollback de sldb.api.transaction deja .sldb_cache/rules/dirty.json como estaba antes de la transacción y relanza el error original (o ConflictError), no RollbackError, también en un store con RuleDoc y dirty set. Un test de sldb lo fija.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/documents/transaction_state.py, transaction_ops.py y transaction_paths.py (lo mínimo para que la transacción snapshotee el dirty set), y si hace falta src/sldb/api/rules/dirty_set.py y rules_on_write.py (sin cambiar qué marca el dirty set); un test nuevo en tests/api/ y CHANGELOG.md. Fuera: la semántica de on_write y del dirty set, otros archivos de .sldb_cache, replace_text fuera de transacción y el resto de la API.

## Implementation Path

_Outline the expected implementation route or affected surface._

SUPERFICIE (sldb origin/main 758772c0):
- src/sldb/api/documents/transaction_state.py (78 líneas). Al abrir, signatures = store_signatures(store_path) (:28): el (mtime, size) de cada archivo del store y de su cache (.sldb_cache), sin los locks. remember(paths, model) (:38) snapshotea antes de cada escritura (transaction_ops.py :50, :74, :83, :93). rollback(original) (:56) llama restore_all(saved), luego unsnapshotted_drift(signatures, store_path, saved) (transaction_paths.py:60). Los archivos nuevos sin snapshot se borran; los cambiados sin snapshot cuentan como failed y producen RollbackError.
- src/sldb/api/rules/rules_on_write.py:29 check_on_write: un paso de save_document_payload que evalúa on_write y llama a dirty_set.mark_dirty(store_path, graph.index, node) (:37). mark_dirty (dirty_set.py:36) reescribe <cache>/rules/dirty.json bajo el lock del store si el archivo existe; si no existe, no lo crea («absent stays absent»).
- Por eso, en una transacción sobre un store con RuleDoc y dirty.json presente, la primera escritura cambia dirty.json sin snapshot. Si después la transacción falla, rollback lanza RollbackError('Rollback incomplete; not restored: .sldb_cache/rules/dirty.json') encadenado al original.

DECISIÓN (coordinador del plan de deskops, por recomendación del coordinador de proyecto; REVISABLE):
s1 (snapshotear, no excluir): la transacción snapshotea el dirty set antes de que lo toque cualquier escritura suya, y el rollback lo restaura a su contenido previo (o lo borra si no existía). Así cumple su contrato: todo archivo tocado vuelve a como estaba. No se excluye .sldb_cache/rules de store_signatures ni de unsnapshotted_drift, porque eso esconde estado. Una forma válida es que TransactionState.remember incluya <rules_dir>/dirty.json la primera vez que snapshotea en un store, o que se snapshotee al abrir la transacción. El worker elige la que menos toque y la explica.
s2 (sin cambiar semántica): mark_dirty sigue marcando lo mismo. Tras un commit exitoso, el dirty set queda como hoy. Tras un rollback, queda como antes de la transacción, y es correcto porque los documentos también volvieron.
s3 (test de regresión): un test nuevo en tests/api/ (por ejemplo tests/api/test_transaction_rules_dirty.py, o un caso nuevo en tests/api/test_transaction.py) que arme un store con un RuleDoc on_write y un dirty set existente (rules check o rules_on_check para crearlo), abra transaction(), actualice un documento trackeado y lance un error propio dentro del bloque. El test espera: (a) que salga el error propio, no RollbackError; (b) que dirty.json quede byte a byte igual que antes; (c) que el documento quede igual. Un segundo caso usa expected_source_hash viejo y espera ConflictError, no RollbackError. Un tercero hace commit exitoso y comprueba que dirty.json cambia como hoy.
s4 (validación, de a uno): el test nuevo, tests/api/test_transaction.py, tests/api/test_rules_evaluation.py, tests/api/test_write_paths_validate.py, tests/api/test_replace_text.py y tests/test_clean_code_rules.py. Con deskops wt/cc32 (c9af867e) y PYTHONPATH a esta rama de sldb, tests/test_transaction.py de deskops pasa entero; es la prueba de aceptación del consumidor.
s5 (líneas): wc -l antes y después; los archivos de sldb respetan los límites de test_clean_code_rules.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-09):
b1 (diseño): se snapshotea al abrir la transacción. TransactionState.__init__ (transaction_state.py:28), donde ya se toman las signatures, llama a remember([rules_dir(store_path) / "dirty.json"]). snapshot ya guarda None para un archivo ausente, y restore_all lo borra si apareció. remember y las escrituras no cambian. Si el worker encuentra que esto no alcanza (por ejemplo, un import circular entre api/documents y api/rules), usa en su lugar la ruta como constante en transaction_paths y lo explica en el informe.
b2 (criterio): manda b1; no hay que elegir otra forma.
b3 (test): archivo nuevo tests/api/test_transaction_rules_dirty.py. tests/api/test_transaction.py no se toca.
b4 (setup): se reusa el patrón del fixture world de tests/api/test_rules_evaluation.py (:53-87: World.doc, World.rule y World.save, un store en tmp_path con un RuleDoc). El dirty set se crea con api.rules_on_check(world.store), como en test_a_write_dirties_the_document_and_its_neighbours_only (:204-211). Si el fixture no se puede importar, se copia lo mínimo al archivo nuevo.
b5 (error propio): class Boom(RuntimeError) definida en el test, lanzada con raise Boom("boom") dentro del with api.transaction(...). El test espera pytest.raises(Boom), no RollbackError.
b6 (dirty.json ausente): hay un cuarto caso. Sin dirty.json al abrir (sin rules_on_check previo), la transacción escribe y falla, y después dirty.json sigue ausente; mark_dirty no lo crea, así que no debería aparecer. El commit exitoso (tercer caso de s3) va con dirty.json presente.

## Validation

_List the checks required before this task can close._

- Test de regresión nuevo en tests/api/ (s3): error propio, ConflictError y commit
- TMPDIR=/dev/shm pytest -q, uno a la vez: test nuevo, tests/api/test_transaction.py, test_rules_evaluation, test_write_paths_validate, test_replace_text, tests/test_clean_code_rules.py
- deskops wt/cc32 c9af867e: tests/test_transaction.py pasa con PYTHONPATH a esta rama de sldb
- wc -l antes y después
- CHANGELOG

## Done When

_Name the observable condition that makes the task complete._

En un store con RuleDoc y dirty set, una transacción que falla relanza su error original (o ConflictError) y deja dirty.json y los documentos como estaban; tras un commit, dirty.json se actualiza como hoy. Test nuevo de sldb verde, más test_transaction, test_rules_evaluation, test_write_paths_validate, test_replace_text y test_clean_code_rules de sldb, de a uno. El test_transaction de deskops wt/cc32 pasa entero contra esta rama. CHANGELOG.
