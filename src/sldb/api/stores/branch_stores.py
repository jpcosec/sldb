"""Other local branches of the same repository that already have a store at this path: the
alert `sldb stores init` gives before a second store is born on a branch (one store per repo:
two stores in two branches only meet again in a merge, MEPU 20261115-195033)."""

from __future__ import annotations

from pathlib import Path

from sldb.ports.git import git_output


def branches_with_store(root: Path) -> list[str]:
    """Local branches other than the current one whose tree has a store at `<root>/.sldb/`
    (its `store.yaml`, or the `core/store_index.yaml` of a store never declared); empty outside git."""
    rel = git_output(root, "rev-parse", "--show-prefix")
    if rel is None:
        return []
    current = (git_output(root, "branch", "--show-current") or "").strip()
    heads = (git_output(root, "for-each-ref", "--format=%(refname:short)", "refs/heads") or "").split()
    targets = [f"{rel.strip()}.sldb/{name}" for name in ("store.yaml", "core/store_index.yaml")]
    return [b for b in heads if b != current and (git_output(root, "ls-tree", "--full-tree", "--name-only", b, "--", *targets) or "").strip()]
