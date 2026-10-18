from __future__ import annotations
import argparse
from sldb.cli.output_format import add_format

def _add_models_part2(sub):
    _validate(sub); _template(sub); _fields(sub); _create(sub)

def _validate(s):
    v = s.add_parser("validate", help="Validate a registered model or draft.")
    v.add_argument("model", help="Model name")
    v.add_argument("--store", help="Store path")
    v.add_argument("--pythonpath", help="Project path")
    v.add_argument("--promote", action="store_true", help="Promote a valid draft")
    v.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _template(s):
    t = s.add_parser("template", help="Inspect or edit a registered model template.")
    ts = t.add_subparsers(dest="template_command", required=True)
    _tshow(ts)
    _tedit(ts)

def _tshow(ts):
    tshow = ts.add_parser("show", help="Show the active or draft template.")
    tshow.add_argument("model", help="Model name")
    tshow.add_argument("--store", help="Store path")
    tshow.add_argument("--pythonpath", help="Project path")
    tshow.add_argument("--draft", action="store_true", help="Show the draft template")
    add_format(tshow)

def _tedit(ts):
    tedit = ts.add_parser("edit", help="Write a template draft for a registered model.")
    tedit.add_argument("model", help="Model name")
    tedit.add_argument("--input", required=True, help="Template markdown path")
    tedit.add_argument("--store", help="Store path")
    tedit.add_argument("--pythonpath", help="Project path")

def _fields(s):
    f = s.add_parser("fields", help="Edit registered model fields through drafts.")
    fs = f.add_subparsers(dest="fields_command", required=True)
    _fa(fs)
    _frm(fs)

def _fa(fs):
    fa = fs.add_parser("add", help="Add a field to the model draft.")
    fa.add_argument("model", help="Model name")
    fa.add_argument("field", help="Field name")
    fa.add_argument("--type", dest="field_type", required=True, help="Python type annotation")
    fa.add_argument("--description", required=True, help="Field description")
    fa.add_argument("--default", help="Inline YAML/JSON default value")
    fa.add_argument("--store", help="Store path")
    fa.add_argument("--pythonpath", help="Project path")

def _frm(fs):
    frm = fs.add_parser("remove", help="Remove a field from the model draft.")
    frm.add_argument("model", help="Model name")
    frm.add_argument("field", help="Field name")
    frm.add_argument("--store", help="Store path")
    frm.add_argument("--pythonpath", help="Project path")

def _create(s):
    c = s.add_parser("create", help="Generate a StructuredNLDoc model.")
    c.add_argument("name", help="Class name")
    c.add_argument("--template", required=True, help="Template markdown path")
    c.add_argument("--fields", required=True, help="Field spec YAML path")
    c.add_argument("--output", default="-", help="Output Python file or -")
    c.add_argument("--stdout", action="store_true", help="Print generated code")
