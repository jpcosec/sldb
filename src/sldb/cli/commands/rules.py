"""`sldb rules check|explain`: the store's RuleDoc rules through the CLI (docs/architecture/rules.md).

`check` reports every failing rule as a `Finding` by the one channel (`sldb.cli.alert_sink`) and
exits 1 only when one is an error. `explain` prints the eval finding of one rule on one document
and exits with its value: 0 true, 1 false, 2 incomplete, 3 when the rule does not apply.
"""

from __future__ import annotations

import json
from typing import Any

from sldb.api.rules import explain_exit, rules_check, rules_explain
from sldb.cli import alert_sink
from sldb.cli.output_format import emit
from sldb.core.exceptions import SLDBError


class RulesCLI:
    """Evaluate the rules a store declares as RuleDoc documents."""

    def run(self, args: Any) -> int:
        commands = {"check": self.check, "explain": self.explain}
        if args.rules_command not in commands:
            raise SLDBError(f"Unknown command: {args.rules_command}")
        return commands[args.rules_command](args)

    def check(self, args: Any) -> int:
        findings = rules_check(args.store, args.subject, args.pythonpath)
        text = args.format == "text"
        if not text:
            emit({"findings": [f.as_dict() for f in findings]}, args.format, "")
        alert_sink.report(findings, text=text)
        if text:
            print(f"rules check: {alert_sink.tally(findings) or 'sin hallazgos'}")
        return 1 if any(f.level == "error" for f in findings) else 0

    def explain(self, args: Any) -> int:
        answer = rules_explain(args.store, args.rule, args.subject, args.pythonpath)
        emit(answer, args.format, _text(answer))
        return explain_exit(answer)


def _text(answer: dict[str, Any]) -> str:
    head = f"{answer['rule']} on {answer['subject']}"
    if "finding" not in answer:
        return f"{head}: does not apply ({answer['reason']}: {answer['detail']})"
    found = answer["finding"]
    return f"{head}: {found['holds']}\n  clause: {found['clause']}\n  seen  : {json.dumps(found['seen'], ensure_ascii=False, sort_keys=True)}"
