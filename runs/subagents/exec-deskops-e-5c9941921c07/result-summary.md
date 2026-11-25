# Result
run_id: exec-deskops-e-5c9941921c07
session: n/a (claude executor)  session_sha256: n/a

Added predicate `model_tag("T")`: true when the document's model declares T, a tag descending from T (semantic_parent edges) or an equivalent of either (semantic_equivalent, both ways). Parent query matches children, not the reverse. Reuses the edge index's DAG edges (no second hierarchy).
Writing a RuleDoc whose where/condition names a tag absent from the DAG raises SLDBStoreError "Unknown semantic tag 'T'" (rule_writes.py).

Commit (branch deskops/deskops-e-5c9941921c07), no Task-Id trailer per the clarification. Files:
docs/architecture/rules-language.md, docs/architecture/rules.md, src/sldb/api/rules/rule_writes.py,
src/sldb/store/graph/backend/index_view.py, index_semantics.py (new),
src/sldb/store/graph/language/predicate_{ast,atoms,leaves,view}.py, semantic_scope.py (new),
tests/test_rules_semantic_tag_predicate.py (new)

Validation: see validation.log. Review: the commit has no Task-Id trailer on purpose (the task prompt's
Entrega section asks for one, but its clarifications say not to put it on code commits); decide at closeout.

Code commit: 23750bc31 on deskops/deskops-e-5c9941921c07.
Advance: BLOCKED. `deskops advance task` leaves the task at ritual-execution: rule rule-activation-task-code, the bundle review ReviewDoc:review-...-bundle-1 has anchor_state "changed" and there is no intact accepted preflight. A supervisor must re-review it. I did not touch review documents.
