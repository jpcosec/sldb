from __future__ import annotations
import argparse
from .models2 import _add_models_part2

def add_models_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("models", help="Model contracts and generation.")
    sub = p.add_subparsers(dest="models_command", required=True)
    _add(sub); _update(sub); _remove(sub); _inherit(sub); _list(sub); _show(sub)
    _add_models_part2(sub)

def _add(s):
    a = s.add_parser("add", help="Register model.")
    a.add_argument("model", help="Model ref")
    a.add_argument("--store", help="Store path")
    a.add_argument("--pythonpath", help="Project path")
    a.add_argument("--canonical", action="store_true")

def _update(s):
    u = s.add_parser("update", help="Update model hashes.")
    u.add_argument("model", help="Model name")
    u.add_argument("--store", help="Store path")
    u.add_argument("--pythonpath", help="Project path")

def _remove(s):
    r = s.add_parser("remove", help="Unregister a model; refused while it tracks documents unless --with-documents.")
    r.add_argument("--with-documents", action="store_true", help="Also untrack its documents (files stay); the class need not import")
    r.add_argument("model", help="Model name")
    r.add_argument("--store", help="Store path")
    r.add_argument("--pythonpath", help="Project path")

def _inherit(s):
    i = s.add_parser("inherit", help="Inherit a model from the linked store that owns it (converts a local copy).")
    i.add_argument("model", help="alias:ModelName, the alias linked with `stores add`")
    i.add_argument("--store", help="Store path")
    i.add_argument("--pythonpath", help="Project path")

def _list(s):
    l = s.add_parser("list", help="List registered models.")
    l.add_argument("--store", help="Store path")
    l.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _show(s):
    sh = s.add_parser("show", help="Show registered model info.")
    sh.add_argument("model", help="Model name")
    sh.add_argument("--store", help="Store path")
    sh.add_argument("--pythonpath", help="Project path")
