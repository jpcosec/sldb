"""Code facts as a public API: what `sldb.code` reads from Python, TS, TSX, JS, JSX and SQL.

`code_facts(root, paths=None)` returns `{"facts": [...], "skipped": [...]}`. `paths` (relative to
`root`, files or directories; `None` is the whole tree) is checked before anything is scanned: an
absolute path, one outside `root` or one that does not exist raises `ValueError` naming it, and a
repeated path counts once. A directory expands like `sldb.code.files.find_files` (no
`node_modules`, no `__pycache__`). Each fact has the shape of `sldb.code.facts.fact`: `path`
relative to `root` with `/`, `span` `{"start_line", "end_line"}` (1-based, inclusive) and
`source_hash` `"sha256:<hex>"` of the file's bytes, both as the readers give them; a fact without
them is a reader bug and raises `RuntimeError`. Facts come by path, then by position in the file,
with the ids of `scan_tree`. A file that parses with errors keeps its facts (`has_error` or
`parse_errors`, as its reader says); `skipped` lists, sorted, only the files without an installed
grammar (or with no grammar at all).
"""

from sldb.api.code.code_facts import code_facts

__all__ = ["code_facts"]
