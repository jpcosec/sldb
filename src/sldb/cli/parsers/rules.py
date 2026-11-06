from __future__ import annotations
import argparse

def add_rules_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("rules", help="Evaluate the store's RuleDoc rules (docs/architecture/rules.md).")
    sub = p.add_subparsers(dest="rules_command", required=True)
    _check(sub); _explain(sub)

def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Directory to import models from")
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _check(s):
    c = s.add_parser("check", formatter_class=argparse.RawDescriptionHelpFormatter, help="Report each failing rule as a finding; exit 1 only on an error.",
                     epilog="Without --subject: the on_check rules over every local document of their family.\nExample:\n  sldb rules check --subject TaskDoc:task-a --format json")
    c.add_argument("--subject", help="Only this document (Model:name, store:Model:name or path), every rule of any moment")
    _common(c)

def _explain(s):
    e = s.add_parser("explain", formatter_class=argparse.RawDescriptionHelpFormatter, help="The eval finding of one rule on one document; exit 0 true, 1 false, 2 incomplete, 3 not applicable.",
                     epilog="Example:\n  sldb rules explain RuleDoc:needs-owner TaskDoc:task-a --format json")
    e.add_argument("rule", help="RuleDoc:<name>, <name> or the rule's path")
    e.add_argument("subject", help="Model:name, store:Model:name or the document's path")
    _common(e)
