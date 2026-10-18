"""Whether a document's indexed text is some version of the file git has seen.

`stores check` said FAIL for an index that only fell behind and for one that matches nothing,
alike (inbox 20260924-010929). Git can tell them apart: an indexed text that is an earlier
committed version of the file is `stale` (`stores update`); one that no committed version has
is `unmatched` (an edit indexed and never committed, or damage: worth a look); a file gone
from disk is `orphan`. Outside a git work tree everything is `undetermined`.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from sldb.store.hashing import hash_text

MEANINGS = {
    "stale": "the index holds an earlier committed version of this file: it fell behind",
    "unmatched": "no committed version of this file has the indexed text: an edit indexed and never committed, or damage",
    "orphan": "the file is gone from disk",
    "undetermined": "not a git work tree: cannot tell stale from damaged",
}
_DEPTH = 200  # commits of a file's history searched; older indexes read as unmatched


def text_history(root: Path, rel_path: str, indexed_hash: str | None, exists: bool) -> dict[str, str]:
    """`{verdict, commit?, command}` for a document whose text disagrees with its index."""
    command = f"git log --follow -p -- {rel_path}"
    commits = _commits(root, rel_path)
    if commits is None:
        return {"verdict": "undetermined", "command": command}
    if not exists:
        return {"verdict": "orphan", **({"commit": commits[0][:10]} if commits else {}), "command": command}
    found = next((c for c in commits if indexed_hash and _hash_at(root, c, rel_path) == indexed_hash), None)
    return {"verdict": "stale", "commit": found[:10], "command": command} if found else {"verdict": "unmatched", "command": command}


def _commits(root: Path, rel_path: str) -> list[str] | None:
    out = _git(root, "log", "--follow", f"-n{_DEPTH}", "--format=%H", "--", rel_path)
    return None if out is None else out.split()


def _hash_at(root: Path, commit: str, rel_path: str) -> str | None:
    text = _git(root, "show", f"{commit}:{rel_path}")
    return hash_text(text) if text is not None else None


def _git(root: Path, *argv: str) -> str | None:
    try:
        done = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True, check=False)
    except OSError:
        return None
    return done.stdout if done.returncode == 0 else None


def with_history(doc, root: Path):
    """The diagnosis, with `history` when its text disagrees with the index (or it is gone)."""
    if not doc.content_ok:
        doc.history = text_history(root, doc.path, doc.content_in_index, doc.path_exists)
    return doc
