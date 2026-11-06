"""Rules (GO06): the RuleDoc documents of a store, evaluated with the predicate language.

`rules_check` turns the failures into core `Finding`s; `rules_explain` returns one eval finding;
`refuse_unknown_family` is what writing a RuleDoc checks against the store. GO08 evaluates
them when they are due: `on_write` in `save_document_payload`, `on_transition` in
`edges_holding`/`edges_blocked` (`transition_findings`) and `on_check` in `stores check`
(`on_check_findings`, incremental over `.sldb_cache/rules`) (docs/architecture/rules.md).
"""

from sldb.api.rules.rule_writes import refuse_unknown_family
from sldb.api.rules.rules_check import rules_check
from sldb.api.rules.rules_explain import explain_exit, rules_explain
from sldb.api.rules.rules_on_check import on_check_findings, rules_on_check
from sldb.api.rules.rules_on_transition import transition_findings

__all__ = ["explain_exit", "on_check_findings", "refuse_unknown_family", "rules_check", "rules_explain", "rules_on_check", "transition_findings"]
