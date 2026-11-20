from __future__ import annotations
import argparse

def add_project_commands(s: argparse._SubParsersAction) -> None:
    _init(s)
    _example(s)
    _move(s)

def _init(s):
    p = s.add_parser("init", help="Create a repository-local SLDB skill file.")
    p.add_argument("path", nargs="?", default=".")
    p.add_argument("--force", action="store_true")

def _example(s):
    p = s.add_parser("example", help="Unpack the bundled SLDB reference example.")
    p.add_argument("path", nargs="?", default=".")

def _move(s):
    p = s.add_parser("move", help="Move a file or directory with git mv and fix the store's fields and Markdown links that name it.")
    p.add_argument("source", help="File or directory to move")
    p.add_argument("destination", help="Where it goes; must not exist and must stay inside the project")
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Project path")
    p.add_argument("--dry-run", action="store_true", help="List what would move and be rewritten; touch nothing")
    p.add_argument("--format", choices=("text", "json"), default="text")
