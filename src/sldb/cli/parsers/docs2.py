from __future__ import annotations
import argparse

def _add_docs_part2(sub):
    _recover(sub); _list(sub); _compose(sub); _explore(sub)

def _recover(s):
    r = s.add_parser("recover", help="Resolve [[links]] and report their targets.", epilog="Example:\n  sldb docs recover roadmap --store .sldb")
    r.add_argument("doc", help="Doc name or path")
    r.add_argument("--store", help="Store path")
    r.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    r.add_argument("--depth", type=int, default=1)
    r.add_argument("--links-only", action="store_true")
    r.add_argument("--include-transclusions", action="store_true")

def _list(s):
    l = s.add_parser("list", help="List tracked documents.")
    l.add_argument("--store", help="Store path")
    l.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _compose(s):
    c = s.add_parser("compose", help="Expand ![[transclusions]] into composed Markdown.")
    c.add_argument("doc", help="Doc name or path")
    c.add_argument("--store", help="Store path")
    c.add_argument("-o", "--output", default="-", help="Output path or - for stdout")
    c.add_argument("--format", choices=("markdown", "json", "yaml"), default="markdown")

def _explore(s):
    e = s.add_parser("explore", help="Search tracked docs, repo docs, and docstrings.")
    e.add_argument("term", help="Search term or regex")
    e.add_argument("--source", choices=("all", "docs", "docstrings"), default="all")
    e.add_argument("--regex", action="store_true")
    e.add_argument("--docs-root", default="docs", help="Docs directory to scan")
    e.add_argument("--code-root", default="src", help="Python source directory to scan")
    e.add_argument("--max-results", type=int, default=20)
    e.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    e.add_argument("--store", help="Store used to anchor relative source roots")
