from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from sldb.cli.commands.model import ModelCLI
from sldb.cli.graph import ast_for_target
from sldb.cli.utils import write_text


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
        raise SystemExit(f"Unknown models command: {command}")

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
