"""Rules (GO06): the RuleDoc documents of a store, evaluated with the predicate language.

`rules_check` turns the failures into core `Finding`s; `rules_explain` returns one eval finding;
`refuse_unknown_family` is what writing a RuleDoc checks against the store
(docs/architecture/rules.md).
"""

from sldb.api.rules.rule_writes import refuse_unknown_family
from sldb.api.rules.rules_check import rules_check
from sldb.api.rules.rules_explain import explain_exit, rules_explain

__all__ = ["explain_exit", "refuse_unknown_family", "rules_check", "rules_explain"]
