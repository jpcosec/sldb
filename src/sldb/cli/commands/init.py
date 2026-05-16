from __future__ import annotations

from importlib.resources import files
from pathlib import Path
from typing import Any


class InitCLI:
    """Handles project initialization and example generation."""

    def init(self, args: Any) -> int:
        target_dir = Path(args.path)
        skills_dir = target_dir / ".skills" / "sldb"
        skills_file = skills_dir / "SKILL.md"

        if skills_file.exists() and not args.force:
            from sldb.core.exceptions import SLDBError

            raise SLDBError(f"File exists: {skills_file}. Use --force to replace.")

        skills_dir.mkdir(parents=True, exist_ok=True)
        content = (
            files("sldb.assets.skills").joinpath("sldb.md").read_text(encoding="utf-8")
        )
        skills_file.write_text(content, encoding="utf-8")
        print(f"Wrote {skills_file}")
        return 0

    def example(self, args: Any) -> int:
        target_root = Path(args.path) / "sldb_example"
        target_root.mkdir(parents=True, exist_ok=True)

        bundle_path = files("sldb.examples.reference_bundle")
        for item in bundle_path.iterdir():
            if (
                item.is_file()
                and item.name != "__init__.py"
                and "__pycache__" not in str(item)
            ):
                (target_root / item.name).write_text(
                    item.read_text(encoding="utf-8"), encoding="utf-8"
                )
                print(f"Wrote {target_root / item.name}")
        return 0
