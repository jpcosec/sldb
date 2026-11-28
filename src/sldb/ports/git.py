"""The port to git: the one place that runs the `git` binary.

`run_git` is the base; the other functions are the questions sldb asks git today, each
with the way it fails (`None`, `False` or an exception) that its callers already relied on.
Nothing here knows nodes, documents or stores.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def run_git(*args: str, cwd: Path | str | None = None, text: bool = True,
            timeout: float | None = None, check: bool = False) -> subprocess.CompletedProcess:
    """`git <args>` with its output captured; `OSError` (no git) and the timeout propagate."""
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=text, timeout=timeout, check=check)


def git_output(cwd: Path, *args: str) -> str | None:
    """Stdout of `git <args>` in `cwd`; None when git fails or is missing."""
    try:
        done = run_git(*args, cwd=cwd)
    except OSError:
        return None
    return done.stdout if done.returncode == 0 else None


def git_ok(cwd: Path, *args: str) -> bool:
    """Whether `git <args>` in `cwd` exits 0; False when git is missing."""
    try:
        return run_git(*args, cwd=cwd, text=False).returncode == 0
    except OSError:
        return False


def git_stdout(cwd: Path, *args: str, check: bool = True) -> str:
    """Stdout of `git <args>` in `cwd`; with `check`, a failure raises `RuntimeError` with git's stderr."""
    done = run_git(*args, cwd=cwd)
    if check and done.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: {done.stderr.strip()}")
    return done.stdout


def toplevel(path: Path) -> Path | None:
    """The root of the work tree that holds `path` (or its parent when it is a file); None outside git."""
    cwd = path.parent if path.parent.is_dir() else path
    out = git_output(cwd, "rev-parse", "--show-toplevel")
    return Path(out.strip()) if out and out.strip() else None


def describe_checkout(directory: Path) -> str | None:
    """`git describe --tags --always --dirty` of `directory`; None if git fails, is missing or takes over 2 s."""
    try:
        done = run_git("-C", str(directory), "describe", "--tags", "--always", "--dirty", timeout=2)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    described = done.stdout.strip()
    return described if done.returncode == 0 and described else None


def head_sha(path: Path) -> str:
    """The commit `HEAD` of the repository at `path`; empty when there is none."""
    return run_git("-C", str(path), "rev-parse", "HEAD").stdout.strip()


def dirty_paths(path: Path) -> list[str]:
    """`git status --porcelain` lines of the repository at `path`."""
    return run_git("-C", str(path), "status", "--porcelain").stdout.splitlines()


def committed_file(path: Path) -> str | None:
    """The text of `path` as `HEAD` has it; None when `HEAD` has no such version."""
    done = run_git("show", f"HEAD:./{path.name}", cwd=path.parent)
    return done.stdout if done.returncode == 0 else None


def unignored_files(root: Path, check: bool = False) -> bytes | None:
    """`git ls-files --cached --others --exclude-standard -z` of `root`, raw.

    With `check`, a failure raises. Without it, None outside a repository or without git.
    """
    args = ("ls-files", "--cached", "--others", "--exclude-standard", "-z")
    if check:
        return run_git(*args, cwd=root, text=False, check=True).stdout
    try:
        done = run_git(*args, cwd=root, text=False)
    except OSError:
        return None
    return done.stdout if done.returncode == 0 else None
