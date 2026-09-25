"""Where the process-wide derived caches live: the user's cache dir, never inside a store.

A read must not write into the store (`sldb serve` used to dirty tracked repos because the
extracted-payload and built-model caches sat at `<store>/runtime/cache/`). They now live under
`$XDG_CACHE_HOME/sldb` (fallback `~/.cache/sldb`), one file per store keyed by a hash of the
store path — same keying behavior as before, only the file's location changed. When the cache
dir cannot be resolved or written, callers degrade silently: no cache, extraction still runs.

DECISION ABIERTA (coordinacion, 2026-09-22): existen dos intentos mas del mismo arreglo en
ramas hermanas — `fix/runtime-cache-outside-store` (`41a2979`: deja `built.json` dentro del
store y no atrapa `RuntimeError` de `Path.home()`) y `fix/runtime-cache-detached` (`8da361b`:
crashea con HOME raro). Esta rama es la recomendada a conservar; los otros dos worktrees y
ramas se borran cuando el usuario lo autorice (no borrar aun: dos panes de otras sesiones
tienen ese worktree como cwd). Handoff con la lista completa de pendientes:
`AWS_Infra_worktrees/feature-ui:docs/handoff/handoff-2026-09-22-pendientes.md`.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


def _base() -> Path | None:
    root = os.environ.get("XDG_CACHE_HOME")
    if root:
        return Path(root)
    try:
        return Path.home() / ".cache"
    except RuntimeError:
        return None


def cache_root() -> Path | None:
    base = _base()
    return None if base is None else base / "sldb"


def _store_hash(s_path: Path) -> str:
    return hashlib.sha256(str(Path(s_path).resolve()).encode("utf-8")).hexdigest()


def extracted_cache_file(s_path: Path) -> Path | None:
    root = cache_root()
    return None if root is None else root / "runtime-cache-extracted" / f"{_store_hash(s_path)}.json"


def built_cache_file(s_path: Path) -> Path | None:
    root = cache_root()
    return None if root is None else root / "runtime-cache-built" / f"{_store_hash(s_path)}.json"
