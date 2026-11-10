"""---
id: sldb.selfdoc.python_doc_ids
kind: core
tags: [system:sldb, workspace:knowledge, topic:selfdoc]

---
Name the documents of Python symbols: `python-<system>-<module>-<qualname>`, lowercased.

Python tells `transaction` from `Transaction`; the lowercased id does not, and two symbols of
one module that differ only by case got the same document. Only the ids that fold together
carry the AST kind as a suffix (`--function`, `--class`): every other id stays as it was.
"""
from __future__ import annotations

import re
from collections import Counter

from .python_symbol import PythonSymbol


def symbol_slug(record: PythonSymbol) -> str:
    """`<module>-<qualname>` lowercased, with every run of other characters as one `-`."""
    return re.sub(r"[^a-z0-9_]+", "-", f"{record.module}-{record.qualname}".lower()).strip("-")


def document_ids(records: list[PythonSymbol], system: str) -> list[str]:
    """The document id of each record, in order; ids that collide carry `--<kind>`."""
    slugs = [symbol_slug(record) for record in records]
    count = Counter(slugs)
    return [f"python-{system}-{slug}" + (f"--{kind_suffix(record)}" if count[slug] > 1 else "")
            for record, slug in zip(records, slugs)]


def kind_suffix(record: PythonSymbol) -> str:
    """The AST kind without `Def`, lowercased: `FunctionDef` is `function`, `ClassDef` `class`."""
    return re.sub(r"def$", "", record.kind.lower())
