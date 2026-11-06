from __future__ import annotations
from sldb.cli.output_format import add_format

def _add_docs_part3(sub):
    _select(sub); _replace(sub)

def _replace(s):
    r = s.add_parser("replace", help="Replace exactly N occurrences of a literal text in a tracked document (validated and tracked again) or in a plain file under the project root.",
                     epilog="Nothing is written when the count differs, the document no longer validates or an on_write rule refuses it.\n"
                            "Examples:\n  sldb docs replace roadmap --old 'Q3' --new 'Q4'\n"
                            "  sldb --envelope docs replace notes/outline.txt --old foo --new bar --count 2 --format json")
    r.add_argument("ref", help="Doc name, Model/DocName or tracked path; else a path relative to the project root")
    r.add_argument("--old", required=True, help="The literal text to replace (not a regex)")
    r.add_argument("--new", required=True, help="Its replacement")
    _replace_options(r)

def _replace_options(r):
    r.add_argument("--count", type=int, default=1, help="Exactly how many non-overlapping occurrences there must be (default 1)")
    r.add_argument("--store", help="Store path")
    r.add_argument("--pythonpath", help="Project path")
    add_format(r)

def _select(s):
    e = s.add_parser("select", help="Which tracked documents a selector names (keys combined by conjunction).",
                     epilog="Exit codes: 0 ok; with --one, 1 when no document matches or several do (the candidates are listed).\n"
                            "Examples:\n  sldb docs select --prefix task-a --one --format json\n"
                            "  sldb docs select --model BaseDoc --path-glob 'sub/**/*.md' --where 'status = \"open\"'")
    _selector_keys(e)
    e.add_argument("--one", action="store_true", help="Expect exactly one document: error when none or several match")
    e.add_argument("--include-linked", dest="include_linked", action="store_true", help="Also read the stores linked directly to this one")
    e.add_argument("--store", help="Store path")
    add_format(e)

def _selector_keys(e):
    e.add_argument("--ref", help="Doc name, Model/DocName, Model:DocName or tracked path; 'alias:ref' reaches a directly linked store")
    e.add_argument("--prefix", help="Name prefix; with --one an exact name wins over the prefix matches")
    e.add_argument("--path-glob", dest="path_glob", help="Shell pattern over the path relative to the project root ('**' crosses directories)")
    e.add_argument("--model", help="A model name: it and every model extending it")
    e.add_argument("--where", help="A predicate of the rules language over the indexed payload")
