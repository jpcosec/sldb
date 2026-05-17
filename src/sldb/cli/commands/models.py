from __future__ import annotations

import ast
import importlib.util
import json
from importlib.machinery import SourceFileLoader
from pathlib import Path
import sys
from typing import Any

import yaml

from sldb.cli.commands.model import ModelCLI
from sldb.cli.graph import ast_for_target
from sldb.cli.utils import (
    get_store_context,
    parse_data_value,
    read_text,
    resolve_model_ref,
    write_text,
)
from sldb.core.exceptions import (
    SLDBModelDraftError,
    SLDBModelEditError,
    SLDBModelError,
    SLDBValidationError,
)
from sldb.runtime.validation import Validator, validate_model_input_roundtrip
from sldb.store.io import load_documents_index, load_models_index, load_store_index


class ModelsCLI:
    """Plural model surface for the redesigned CLI."""

    def __init__(self) -> None:
        self._model = ModelCLI()

    def run(self, args: Any) -> int:
        command = args.models_command
        if command in {"add", "update"}:
            args.model_command = command
            return self._model.run(args)
        if command == "show":
            payload = ast_for_target(
                args.store, args.pythonpath, f"models/{args.model}"
            )
            print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
            return 0
        if command == "create":
            return self.create(args)
        if command == "validate":
            return self.validate(args)
        if command == "template":
            return self.template(args)
        if command == "fields":
            return self.fields(args)
        raise SystemExit(f"Unknown models command: {command}")

    def fields(self, args: Any) -> int:
        if args.fields_command == "add":
            return self.add_field(args)
        if args.fields_command == "remove":
            return self.remove_field(args)
        raise SystemExit(f"Unknown models fields command: {args.fields_command}")

    def template(self, args: Any) -> int:
        if args.template_command == "show":
            path, module_name, attr_path = self._registered_model_source(args)
            source_path = self._draft_path(path) if args.draft else path
            if args.draft and not source_path.exists():
                raise SLDBModelDraftError(f"No draft template for '{args.model}'.")
            template = self._read_template_literal(
                source_path, attr_path.split(".")[-1]
            )
            print(template)
            return 0
        if args.template_command == "edit":
            return self.edit_template(args)
        raise SystemExit(f"Unknown models template command: {args.template_command}")

    def edit_template(self, args: Any) -> int:
        path, module_name, attr_path = self._registered_model_source(args)
        class_name = attr_path.split(".")[-1]
        template = read_text(args.input).rstrip("\n")
        draft_path = self._draft_path(path)
        source_path = draft_path if draft_path.exists() else path
        updated = self._replace_template_literal(source_path, class_name, template)
        draft_path.write_text(updated, encoding="utf-8")
        print(f"Wrote draft template for '{args.model}' to {draft_path}")
        return 0

    def validate(self, args: Any) -> int:
        path, module_name, attr_path = self._registered_model_source(args)
        draft_path = self._draft_path(path)
        model_path = draft_path if draft_path.exists() else path
        model_type = self._load_model_from_path(
            model_path, module_name, attr_path, args.pythonpath
        )
        details: dict[str, Any] = {
            "model": args.model,
            "draft": draft_path.exists(),
            "path": str(model_path),
            "documents": [],
        }
        try:
            self._validate_template_contract(model_type)
            for doc_name, doc_path in self._tracked_docs_for_model(args):
                valid, doc_details = validate_model_input_roundtrip(
                    model_type, Path(doc_path).read_text(encoding="utf-8")
                )
                details["documents"].append(
                    {"name": doc_name, "path": doc_path, "valid": valid}
                )
                if not valid:
                    raise SLDBValidationError(
                        f"Draft for '{args.model}' failed validation on '{doc_name}'.",
                        doc_details,
                    )
        except (SLDBValidationError, SLDBModelError):
            raise
        except Exception as exc:
            raise SLDBModelEditError(
                f"Draft for '{args.model}' is invalid: {exc}"
            ) from exc

        if args.promote:
            if not draft_path.exists():
                raise SLDBModelDraftError(
                    f"No draft template for '{args.model}' to promote."
                )
            path.write_text(draft_path.read_text(encoding="utf-8"), encoding="utf-8")
            draft_path.unlink()
            args.model_command = "update"
            args.bump_version = True
            self._model.update(args)
            details["promoted"] = True
        else:
            details["promoted"] = False

        if args.format == "text":
            status = (
                "PASS"
                if not details["documents"]
                or all(d["valid"] for d in details["documents"])
                else "FAIL"
            )
            draft_label = "draft" if details["draft"] else "active model"
            print(f"{status}: validated {draft_label} for '{args.model}'")
        elif args.format == "json":
            print(json.dumps({"valid": True, **details}, indent=2))
        else:
            print(
                yaml.safe_dump(
                    {"valid": True, **details}, sort_keys=False, allow_unicode=True
                )
            )
        return 0

    def create(self, args: Any) -> int:
        template = Path(args.template).read_text(encoding="utf-8")
        spec = yaml.safe_load(Path(args.fields).read_text(encoding="utf-8")) or {}
        fields = spec.get("fields", spec if isinstance(spec, list) else [])
        if not isinstance(fields, list) or not fields:
            raise SystemExit("Field spec must define a non-empty 'fields' list.")

        class_name = spec.get("name", args.name)
        base = spec.get("base", "StructuredNLDoc")
        family = spec.get("family")
        semantics = spec.get("semantics")
        body = ["from pydantic import Field", "", f"from sldb import {base}", ""]
        body.append(f"class {class_name}({base}):")
        if family is not None:
            body.append(f"    __family__ = {family!r}")
        if semantics is not None:
            body.append(f"    __semantics__ = {semantics!r}")
        body.append(f"    __template__ = {template!r}")
        for field in fields:
            field_name = field.get("name")
            field_type = field.get("type", "str")
            description = field.get("description")
            if not field_name or not description:
                raise SystemExit("Every generated field needs a name and description.")
            required = field.get("required", True)
            default = field.get("default")
            if required and "default" not in field:
                body.append(
                    f"    {field_name}: {field_type} = Field(description={description!r})"
                )
            else:
                body.append(
                    f"    {field_name}: {field_type} = Field(default={default!r}, description={description!r})"
                )
        content = "\n".join(body) + "\n"
        if args.stdout:
            print(content, end="")
            return 0
        write_text(args.output, content)
        print(f"Wrote {args.output}")
        return 0

    def add_field(self, args: Any) -> int:
        path, _module_name, attr_path = self._registered_model_source(args)
        class_name = attr_path.split(".")[-1]
        source_path = (
            self._draft_path(path) if self._draft_path(path).exists() else path
        )
        default_supplied = args.default is not None
        default_value = parse_data_value(args.default) if default_supplied else None
        field_block = self._field_block(
            args.field,
            args.field_type,
            args.description,
            default_supplied,
            default_value,
        )
        updated = self._insert_field_block(
            source_path, class_name, args.field, field_block
        )
        draft_path = self._draft_path(path)
        draft_path.write_text(updated, encoding="utf-8")
        print(f"Added field draft '{args.field}' for '{args.model}' in {draft_path}")
        return 0

    def remove_field(self, args: Any) -> int:
        path, _module_name, attr_path = self._registered_model_source(args)
        class_name = attr_path.split(".")[-1]
        source_path = (
            self._draft_path(path) if self._draft_path(path).exists() else path
        )
        updated = self._remove_field_block(source_path, class_name, args.field)
        draft_path = self._draft_path(path)
        draft_path.write_text(updated, encoding="utf-8")
        print(f"Removed field draft '{args.field}' for '{args.model}' in {draft_path}")
        return 0

    def _registered_model_source(self, args: Any) -> tuple[Path, str, str]:
        sp, root = get_store_context(args.store)
        idx = load_store_index(sp)
        m_entry = next((m for m in idx.models if m.name == args.model), None)
        if not m_entry:
            raise SLDBModelError(f"Model '{args.model}' not found.")
        model_path = Path(m_entry.path)
        if not model_path.is_absolute():
            model_path = root / model_path
        module_name, attr_path = m_entry.model_ref.split(":", 1)
        return model_path.resolve(), module_name, attr_path

    def _draft_path(self, path: Path) -> Path:
        return path.with_name(path.name + ".temp")

    def _field_block(
        self,
        field_name: str,
        field_type: str,
        description: str,
        default_supplied: bool,
        default_value: Any,
    ) -> str:
        if default_supplied:
            return (
                f"    {field_name}: {field_type} = Field(default={default_value!r}, "
                f"description={description!r})\n"
            )
        return f"    {field_name}: {field_type} = Field(description={description!r})\n"

    def _insert_field_block(
        self, path: Path, class_name: str, field_name: str, field_block: str
    ) -> str:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        class_node = self._find_class_node(tree, class_name, path)
        if any(
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == field_name
            for node in class_node.body
        ):
            raise SLDBModelEditError(
                f"Field '{field_name}' already exists in '{class_name}'."
            )
        anchor = class_node.body[-1]
        lines = source.splitlines(keepends=True)
        insert_at = anchor.end_lineno
        lines.insert(insert_at, field_block)
        return "".join(lines)

    def _remove_field_block(self, path: Path, class_name: str, field_name: str) -> str:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        class_node = self._find_class_node(tree, class_name, path)
        field_node = next(
            (
                node
                for node in class_node.body
                if isinstance(node, ast.AnnAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id == field_name
            ),
            None,
        )
        if field_node is None:
            raise SLDBModelEditError(
                f"Field '{field_name}' does not exist in '{class_name}'."
            )
        return self._remove_node_block(source, field_node)

    def _find_class_node(
        self, tree: ast.AST, class_name: str, path: Path
    ) -> ast.ClassDef:
        class_node = next(
            (
                node
                for node in tree.body
                if isinstance(node, ast.ClassDef) and node.name == class_name
            ),
            None,
        )
        if class_node is None:
            raise SLDBModelEditError(f"Class '{class_name}' not found in {path}.")
        return class_node

    def _replace_template_literal(
        self, path: Path, class_name: str, template: str
    ) -> str:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        class_node = next(
            (
                node
                for node in tree.body
                if isinstance(node, ast.ClassDef) and node.name == class_name
            ),
            None,
        )
        if class_node is None:
            raise SLDBModelEditError(f"Class '{class_name}' not found in {path}.")
        assign_node = next(
            (
                node
                for node in class_node.body
                if isinstance(node, ast.Assign)
                and any(
                    isinstance(target, ast.Name) and target.id == "__template__"
                    for target in node.targets
                )
            ),
            None,
        )
        if assign_node is None:
            raise SLDBModelEditError(
                f"Class '{class_name}' has no __template__ assignment."
            )
        return self._replace_rhs_expression(
            source, assign_node.value, self._template_literal(template)
        )

    def _template_literal(self, template: str) -> str:
        escaped = template.replace('"""', '\\"\\"\\"')
        return f'"""{escaped}""".strip()'

    def _read_template_literal(self, path: Path, class_name: str) -> str:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        class_node = next(
            (
                node
                for node in tree.body
                if isinstance(node, ast.ClassDef) and node.name == class_name
            ),
            None,
        )
        if class_node is None:
            raise SLDBModelEditError(f"Class '{class_name}' not found in {path}.")
        assign_node = next(
            (
                node
                for node in class_node.body
                if isinstance(node, ast.Assign)
                and any(
                    isinstance(target, ast.Name) and target.id == "__template__"
                    for target in node.targets
                )
            ),
            None,
        )
        if assign_node is None:
            raise SLDBModelEditError(
                f"Class '{class_name}' has no __template__ assignment."
            )
        value_node = assign_node.value
        if isinstance(value_node, ast.Call):
            return ast.literal_eval(value_node.func.value)
        return ast.literal_eval(value_node)

    def _load_model_from_path(
        self, path: Path, module_name: str, attr_path: str, pythonpath: str | None
    ):
        search_paths = [str(Path.cwd().resolve())]
        if pythonpath:
            search_paths.insert(0, str(Path(pythonpath).resolve()))
        for candidate in reversed(search_paths):
            if candidate not in sys.path:
                sys.path.insert(0, candidate)
        loader = SourceFileLoader(f"{module_name}__draft__", str(path))
        spec = importlib.util.spec_from_loader(f"{module_name}__draft__", loader)
        if spec is None or spec.loader is None:
            raise SLDBModelDraftError(f"Could not load model draft from {path}.")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        obj: Any = module
        for attr in attr_path.split("."):
            obj = getattr(obj, attr)
        return obj

    def _validate_template_contract(self, model_type: Any) -> None:
        recipes = Validator(model_type)._get_recipes()
        field_names = set(model_type.model_fields)
        referenced: set[str] = set()
        for recipe in recipes:
            markers = list(recipe.get("props_info", []))
            if "marker" in recipe:
                markers.append(recipe["marker"])
            if "col_markers" in recipe:
                for marker_info in recipe["col_markers"].values():
                    markers.append(marker_info["marker"])
            for marker in markers:
                name = getattr(marker, "name", None)
                if isinstance(marker, dict):
                    name = marker.get("name")
                if name:
                    referenced.add(name)
        unknown = sorted(name for name in referenced if name not in field_names)
        if unknown:
            raise SLDBModelEditError(
                f"Draft for '{model_type.__name__}' references unknown fields: {', '.join(unknown)}"
            )

    def _replace_rhs_expression(
        self, source: str, node: ast.AST, replacement: str
    ) -> str:
        lines = source.splitlines(keepends=True)
        start_line = node.lineno - 1
        end_line = node.end_lineno - 1
        start_col = node.col_offset
        end_col = node.end_col_offset
        if start_line == end_line:
            line = lines[start_line]
            lines[start_line] = line[:start_col] + replacement + line[end_col:]
            return "".join(lines)
        prefix = lines[start_line][:start_col]
        suffix = lines[end_line][end_col:]
        lines[start_line : end_line + 1] = [prefix + replacement + suffix]
        return "".join(lines)

    def _remove_node_block(self, source: str, node: ast.AST) -> str:
        lines = source.splitlines(keepends=True)
        start_line = node.lineno - 1
        end_line = node.end_lineno
        del lines[start_line:end_line]
        return "".join(lines)

    def _tracked_docs_for_model(self, args: Any) -> list[tuple[str, str]]:
        sp, root = get_store_context(args.store)
        idx = load_store_index(sp)
        m_entry = next((m for m in idx.models if m.name == args.model), None)
        if not m_entry:
            raise SLDBModelError(f"Model '{args.model}' not found.")
        m_idx = load_models_index(root / m_entry.models_index)
        d_idx = load_documents_index(root / m_idx.documents_index)
        docs: list[tuple[str, str]] = []
        for doc in d_idx.documents:
            doc_path = Path(doc.path)
            if not doc_path.is_absolute():
                doc_path = root / doc_path
            docs.append((doc.name, str(doc_path)))
        return docs
