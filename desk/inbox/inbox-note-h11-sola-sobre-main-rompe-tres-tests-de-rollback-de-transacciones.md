---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: mepu
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-14T02:19:01'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:28:20'
---

# H11 (wt/h11) sola sobre main rompe tres tests de rollback de transacciones; no se integró

_Describe the incoming message with enough evidence to triage._

Escrita a mano desde mepu (14-11) por pedido de JP, que pidió integrar en main las ramas pendientes de sldb.

- **Integrado en main (`b51e9667`):** wt/h1-check, wt/pending-desk-h11b-y-fila (= el worktree sldb-desk-tmp) y wt/h47; CHANGELOG.md resuelto conservando las entradas de ambos lados. Suite completa: 2420 passed, 0 failed, 25 skipped (igual que main antes).
- **No integrado: wt/h11.** Sola sobre main (`b965c62d`) da 3 failed en tests/api/test_replace_text.py, test_tags.py, test_transaction.py y test_transaction_rules_dirty.py (en main: 67 passed). Junto con H47 suben a 6, incluidos los dos tests nuevos de H47 en tests/api/test_on_write_entering.py (`test_apply_batch_inherits_the_refusal_and_leaves_the_tree_as_it_was`, `test_transaction_create_inherits_the_refusal_and_restores_the_tree`). Todos son de rollback: una escritura rechazada dentro de una transacción no deja el árbol como estaba.
- **Las otras 21 ramas wt/*** ya estaban en main por squash (sus conflictos al mezclarlas son solo porque main siguió cambiando ese código); se pueden borrar tras revisarlas.
