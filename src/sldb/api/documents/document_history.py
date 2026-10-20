"""`sldb docs history`: a document's past, read from git (docs/architecture/provenance.md §3).

The history lives in git; sldb only puts the wheels on it: for each commit that touched the
file, the provenance block of that version (who signed it, not who committed it: the git
identity is not trusted), its two hashes, and the fields that changed against the version
before. Outside a git work tree, or for a file git never saw, the history is empty.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from sldb.api.documents.document_history_versions import changed_fields, version_facts
from sldb.api.documents.document_payload import runtime_document
from sldb.api.stores.open_store import open_store

_DEPTH = 200
_SEP = "\x1f"


def document_history(store: str | Path | None, doc_ref: str, pythonpath: str | None = None, since: str | None = None) -> list[dict[str, Any]]:
    """Newest first: `{commit, date, by, at, via, authority, declared, source_hash,
    content_hash, changed_fields}` per commit that touched the document, from `since` (ISO date) on."""
    location = open_store(store, mode="readonly")
    doc = runtime_document(location.store_path, pythonpath, doc_ref)
    commits = _commits(location.project_root, doc.path)
    versions = [version_facts(doc.model_type, _show(location.project_root, sha, path)) for sha, _d, path in commits]
    entries = [_entry(meta, versions[i], versions[i + 1] if i + 1 < len(versions) else None) for i, meta in enumerate(commits)]
    return [e for e in entries if since is None or e["date"] >= since]


def _entry(meta: tuple[str, str, str], now: dict[str, Any], before: dict[str, Any] | None) -> dict[str, Any]:
    sha, date, _path = meta
    changed = changed_fields(now["field_hashes"], before["field_hashes"]) if before else []
    return {"commit": sha, "date": date, **now["provenance"], "source_hash": now["source_hash"], "content_hash": now["content_hash"], "changed_fields": changed}


def _commits(root: Path, rel_path: str) -> list[tuple[str, str, str]]:
    """`(sha, iso date, path at that commit)`, newest first; renames followed."""
    out = _git(root, "log", "--follow", f"-n{_DEPTH}", f"--format=%H{_SEP}%cI", "--name-only", "--", rel_path)
    found, pending = [], None
    for line in (out or "").splitlines():
        if _SEP in line:
            pending = tuple(line.split(_SEP))
        elif line.strip() and pending:
            found.append((pending[0], pending[1], line.strip()))
            pending = None
    return found


def _show(root: Path, sha: str, rel_path: str) -> str:
    return _git(root, "show", f"{sha}:{rel_path}") or ""


def _git(root: Path, *argv: str) -> str | None:
    try:
        done = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True, check=False)
    except OSError:
        return None
    return done.stdout if done.returncode == 0 else None
