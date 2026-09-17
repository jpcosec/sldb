from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from sldb.api.model_drafts.field_blocks import check_field_absent, field_block, field_node, insert_field_block, remove_field_block
from sldb.api.model_drafts.field_drafts import add_model_field, remove_model_field
from sldb.cli.utils import parse_data_value

class ModelsFieldsCLI:
    """`sldb models fields add|remove`: thin CLI adapters over `sldb.api` draft field edits."""

    def fields(self, args: Any) -> int:
        if args.fields_command == "add":
            return self.add_field(args)
        if args.fields_command == "remove":
            return self.remove_field(args)
        raise SystemExit(f"Unknown models fields command: {args.fields_command}")

    def add_field(self, args: Any) -> int:
        draft = add_model_field(args.store, args.model, args.field, args.field_type, args.description, args.default, getattr(args, "pythonpath", None))
        print(f"Added field draft '{args.field}' for '{args.model}' in {draft.draft_path}")
        return 0

    def _get_new_field_block(self, args: Any) -> str:
        d_supplied = args.default is not None
        d_val = parse_data_value(args.default) if d_supplied else None
        return self._field_block(args.field, args.field_type, args.description, d_supplied, d_val)

    def _field_block(self, field_name: str, field_type: str, description: str, default_supplied: bool, default_value: Any) -> str:
        return field_block(field_name, field_type, description, default_supplied, default_value)

    def _insert_field_block(self, path: Path, cls_name: str, f_name: str, f_block: str) -> str:
        return insert_field_block(path, cls_name, f_name, f_block)

    def _check_field_not_exists(self, class_node: ast.ClassDef, cls_name: str, f_name: str) -> None:
        check_field_absent(class_node, cls_name, f_name)

    def remove_field(self, args: Any) -> int:
        draft = remove_model_field(args.store, args.model, args.field, getattr(args, "pythonpath", None))
        print(f"Removed field draft '{args.field}' for '{args.model}' in {draft.draft_path}")
        return 0

    def _remove_field_block(self, path: Path, class_name: str, field_name: str) -> str:
        return remove_field_block(path, class_name, field_name)

    def _get_field_node(self, class_node: ast.ClassDef, class_name: str, field_name: str) -> ast.AST:
        return field_node(class_node, class_name, field_name)
