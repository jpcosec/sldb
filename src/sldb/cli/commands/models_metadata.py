"""`sldb models metadata edit`: thin CLI adapter over `sldb.api` metadata drafts."""

from __future__ import annotations

import contextlib
import json
from pathlib import Path
from typing import Any
import yaml

from sldb.api.model_drafts.metadata_drafts import edit_model_metadata


class ModelsMetadataCLI:
    """`sldb models metadata edit`: thin CLI adapter over `sldb.api` metadata drafts."""

    def metadata(self, args: Any) -> int:
        if args.metadata_command == "edit":
            return self.edit_metadata(args)
        raise SystemExit(f"Unknown models metadata command: {args.metadata_command}")

    def edit_metadata(self, args: Any) -> int:
        meta = {k: self._parse_json_or_yaml(getattr(args, k, None)) for k in ("containment", "references", "compositions", "semantics")}
        draft = edit_model_metadata(args.store, args.model, authority=getattr(args, "authority", None), pythonpath=getattr(args, "pythonpath", None), **meta)
        print(f"Updated metadata draft for '{args.model}' in {draft.draft_path}")
        return 0

    @staticmethod
    def _parse_json_or_yaml(value: str | None) -> Any:
        if not value:
            return None
        text = value.strip()
        if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
            with contextlib.suppress(Exception):
                return json.loads(text)
        p = Path(text)
        return yaml.safe_load(p.read_text(encoding="utf-8") if p.is_file() else text)
