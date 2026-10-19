"""The directory an owner's model imports from, read off the path the owner registers.

An owner with a `src/` layout registers `src/pron/models/anchor.py` for `pron.models:AnchorDoc`:
the package starts at `src/`, not at the project root, so putting only the root on `sys.path`
leaves the inherited model unimportable. The root is the path up to the module's top package.
"""

from __future__ import annotations

from pathlib import Path


def import_root(owner_root: Path, model_ref: str, registered_path: str) -> Path:
    """`owner_root` joined with what precedes the top package of `model_ref` in `registered_path`;
    `owner_root` itself when the path is empty, absolute or does not contain that package."""
    top = model_ref.split(":", 1)[0].split(".", 1)[0]
    parts = Path(registered_path).parts if registered_path else ()
    if not parts or Path(registered_path).is_absolute() or top not in parts[:-1]:
        return owner_root
    return owner_root.joinpath(*parts[: parts.index(top)])
