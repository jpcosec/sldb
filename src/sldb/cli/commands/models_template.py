from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_drafts.template_drafts import write_template_draft
from sldb.api.model_drafts.template_literals import read_template_literal, replace_template_literal, template_assign_node, template_literal
from sldb.cli.utils import read_text
from sldb.core.exceptions import SLDBModelDraftError
from sldb.cli.commands.models_utils import registered_model_source, draft_path as get_draft_path

class ModelsTemplateCLI:
    """`sldb models template show|edit`: thin CLI adapters over `sldb.api` template drafts."""

    def template(self, args: Any) -> int:
        if args.template_command == "show":
            return self._show_template(args)
        if args.template_command == "edit":
            return self.edit_template(args)
        raise SystemExit(f"Unknown models template command: {args.template_command}")

    def _show_template(self, args: Any) -> int:
        path, _mod, attr = registered_model_source(args)
        src_path = get_draft_path(path) if args.draft else path
        if args.draft and not src_path.exists():
            raise SLDBModelDraftError(f"No draft template for '{args.model}'.")
        template = self._read_template_literal(src_path, attr.split(".")[-1])
        print(template)
        return 0

    def edit_template(self, args: Any) -> int:
        path, module_name, attr = registered_model_source(args)
        template = read_text(args.input)
        d_path = write_template_draft(ModelSource(path=path, module_name=module_name, attr_path=attr), template)
        print(f"Wrote draft template for '{args.model}' to {d_path}")
        return 0

    def _replace_template_literal(self, path: Path, class_name: str, template: str) -> str:
        return replace_template_literal(path, class_name, template)

    def _get_template_assign_node(self, class_node: ast.ClassDef, class_name: str) -> ast.Assign:
        return template_assign_node(class_node, class_name)

    def _template_literal(self, template: str) -> str:
        return template_literal(template)

    def _read_template_literal(self, path: Path, class_name: str) -> str:
        return read_template_literal(path, class_name)
