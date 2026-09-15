from __future__ import annotations
import argparse

def add_misc_commands(s: argparse._SubParsersAction) -> None:
    _help(s); _faq(s); _inbox(s); _explore(s); _ast(s); _lint(s)

def _help(s):
    p = s.add_parser("help", help="Curated CLI help.")
    p.add_argument("topic", nargs="?", help="stores, models, predicates, docs, fields, sections, ast, find, faq, inbox, explore, selfdoc, legacy")

def _faq(s):
    p = s.add_parser("faq", help="Browse the first-use FAQ by question.")
    p.add_argument("question", nargs="?", help="Question index, slug, or text fragment.")
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    p.add_argument("--faq-path", default="docs/faq.md", help="FAQ markdown path")
    p.add_argument("--store", help="Store used to anchor a relative FAQ path")

def _inbox(s):
    p = s.add_parser("inbox", help="Log unclear points or suggestions into the repo desk.")
    p.add_argument("message", nargs="?", help="Inbox note body")
    p.add_argument("--kind", choices=("unclear", "suggestion"), default="unclear", help="Type of desk note to write")
    p.add_argument("--title", help="Short title for the note")
    p.add_argument("--desk-root", help="Desk root directory override")
    p.add_argument("--store", help="Store path used to resolve the target project root")
    p.add_argument("--pythonpath", help="Project path used when auto-tracking inbox notes")
    p.add_argument("--author", default="cli", help="Source label for the inbox note")
    _add_inbox_part2(p)

def _add_inbox_part2(p):
    p.add_argument("--list", action="store_true", help="List desk inbox notes")
    p.add_argument("--show", help="Show one inbox note")
    p.add_argument("--limit", type=int, default=20, help="Limit listed notes")
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _explore(s):
    p = s.add_parser("explore", help="Search markdown docs and Python docstrings.")
    p.add_argument("term", help="Search term or regex")
    p.add_argument("--source", choices=("all", "docs", "docstrings"), default="all")
    p.add_argument("--regex", action="store_true")
    p.add_argument("--docs-root", default="docs", help="Docs directory to scan")
    p.add_argument("--code-root", default="src", help="Python source directory to scan")
    p.add_argument("--max-results", type=int, default=20)
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    p.add_argument("--store", help="Store used to anchor relative source roots")

def _ast(s):
    p = s.add_parser("ast", help="Inspect the normalized SLDB graph.")
    sub = p.add_subparsers(dest="ast_command", required=True)
    sh = sub.add_parser("show", help="Show AST for a target.")
    sh.add_argument("target", nargs="?", default="store")
    sh.add_argument("--store", help="Store path")
    sh.add_argument("--pythonpath", help="Project path")
    sh.add_argument("--format", choices=("json", "yaml", "text"), default="json")
    sch = sub.add_parser("schema", help="Show node and edge schema.")
    sch.add_argument("--format", choices=("json", "yaml", "text"), default="json")

def _lint(s):
    p = s.add_parser("lint", help="Lint knowledge references for canonical paths.")
    p.add_argument("target", nargs="?", help="File or directory to lint (default: recursive scan of repo)")
    p.add_argument("--repo-root", help="Repository root path (default: auto-detect from cwd)")
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")
