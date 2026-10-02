from __future__ import annotations
import argparse

def add_basic_commands(s: argparse._SubParsersAction) -> None:
    _extract(s)
    _render(s)
    _validate(s)

def _extract(s):
    p = s.add_parser("extract", help="Extract data from Markdown.")
    p.add_argument("model", help="Model ref: module:Class")
    p.add_argument("input", help="Markdown file")
    p.add_argument("output", help="Output JSON/YAML")
    p.add_argument("--format", choices=("json", "yaml"), default=None)
    p.add_argument("--pythonpath", help="Project path")

def _render(s):
    p = s.add_parser("render", help="Render Markdown from data.")
    p.add_argument("model", help="Model ref: module:Class")
    p.add_argument("input", help="Data file")
    p.add_argument("output", help="Output .md")
    p.add_argument("--pythonpath", help="Project path")
    p.add_argument("--ref-root", default=None, help="Directory a composed field's refs resolve against (default: the working directory).")

def _validate(s):
    p = s.add_parser("validate", help="Validate idempotency.")
    p.add_argument("model", help="Model ref: module:Class")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--input", help="Markdown file")
    g.add_argument("--data", help="Data file")
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    p.add_argument("--pythonpath", help="Project path")
