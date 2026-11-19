from __future__ import annotations
import argparse

def add_fields_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("fields", help="Field CRUD, append, clean, and query.")
    sub = p.add_subparsers(dest="fields_command", required=True)
    _show(sub); _query(sub); _cruds(sub); _clean(sub)

def _show(s):
    sh = s.add_parser("show", help="Show model field schema or document field value.")
    sh.add_argument("target", help="models/<Model>[/field] or docs/<Doc>/<field>")
    sh.add_argument("--store", help="Store path")
    sh.add_argument("--pythonpath", help="Project path")
    sh.add_argument("--format", choices=("json", "yaml"), default="json")

def _query(s):
    q = s.add_parser("query", help="Query a field path across tracked docs.")
    q.add_argument("field", help="Field path, eg status or tasks.status")
    q.add_argument("--store", help="Store path")
    q.add_argument("--pythonpath", help="Project path")
    q.add_argument("--global", dest="global_scope", action="store_true")
    q.add_argument("--format", choices=("json", "yaml"), default="json")

def _cruds(s):
    cmds = [("create", "Create"), ("update", "Update"), ("remove", "Remove"), ("append", "Append")]
    for n, h in cmds:
        cmd = s.add_parser(n, help=h)
        cmd.add_argument("target", help="docs/<Doc>/<field> or docs/<Model>/<Doc>/<field>")
        cmd.add_argument("value", help="Inline YAML/JSON value")
        cmd.add_argument("--store", help="Store path")
        cmd.add_argument("--pythonpath", help="Project path")
        if n in ("update", "append"):
            cmd.add_argument("--string", action="store_true", help="Take the value as literal text, without JSON/YAML parsing")
            cmd.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _clean(s):
    c = s.add_parser("clean", help="Clean a list field.")
    c.add_argument("target", help="docs/<Doc>/<field> or docs/<Model>/<Doc>/<field>")
    c.add_argument("--store", help="Store path")
    c.add_argument("--pythonpath", help="Project path")
    c.add_argument("--dedupe", action="store_true")
    c.add_argument("--drop-empty", action="store_true")
