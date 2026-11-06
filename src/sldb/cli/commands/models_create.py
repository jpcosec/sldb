from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml

from sldb.cli.commands.models_create_attrs import class_attr_lines
from sldb.cli.utils import write_text

class ModelsCreateCLI:
    def create(self, args: Any) -> int:
        spec, fields = self._parse_fields_spec(args.fields)
        content = "\n".join(self._build_create_body(args, spec, fields)) + "\n"
        return self._output_create(args, content)

    def _parse_fields_spec(self, fields_path: str) -> tuple[dict[str, Any], list[Any]]:
        spec = yaml.safe_load(Path(fields_path).read_text(encoding="utf-8")) or {}
        fields = spec.get("fields", spec if isinstance(spec, list) else [])
        if not isinstance(fields, list) or not fields:
            raise SystemExit("Field spec must define a non-empty 'fields' list.")
        return spec, fields

    def _output_create(self, args: Any, content: str) -> int:
        if args.stdout:
            print(content, end="")
            return 0
        write_text(args.output, content)
        print(f"Wrote {args.output}")
        return 0

    def _build_create_body(self, args: Any, spec: dict[str, Any], fields: list[Any]) -> list[str]:
        template = Path(args.template).read_text(encoding="utf-8")
        class_name = spec.get("name", args.name)
        base = spec.get("base", "StructuredNLDoc")
        body = ["from pydantic import Field", "", f"from sldb import {base}", ""]
        body.append(f"class {class_name}({base}):")
        self._add_create_class_attrs(body, spec, template, args)
        self._add_create_fields(body, fields)
        return body

    def _add_create_class_attrs(self, body: list[str], spec: dict[str, Any], template: str, args: Any = None) -> None:
        body.extend(class_attr_lines(spec, template, args))

    def _add_create_fields(self, body: list[str], fields: list[Any]) -> None:
        for field in fields:
            self._add_single_create_field(body, field)

    def _add_single_create_field(self, body: list[str], field: dict[str, Any]) -> None:
        f_name, desc = field.get("name"), field.get("description")
        f_type = field.get("type", "str")
        if not f_name or not desc:
            raise SystemExit("Every generated field needs a name and description.")
        if field.get("required", True) and "default" not in field:
            body.append(f"    {f_name}: {f_type} = Field(description={desc!r})")
        else:
            body.append(f"    {f_name}: {f_type} = Field(default={field.get('default')!r}, description={desc!r})")
