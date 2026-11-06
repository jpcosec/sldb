from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml

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
        family = getattr(args, "family", None) if args else None
        if family is None:
            family = spec.get("family")
        if family is not None:
            body.append(f"    __family__ = {family!r}")

        authority = getattr(args, "authority", None) if args else None
        if authority is None:
            authority = spec.get("authority")
        if authority is not None:
            body.append(f"    __authority__ = {authority!r}")

        semantics = getattr(args, "semantics", None) if args else None
        if semantics is None:
            semantics = spec.get("semantics")
        elif isinstance(semantics, str):
            import json, yaml
            semantics = json.loads(semantics) if (semantics.startswith("{") or semantics.startswith("[")) else yaml.safe_load(semantics)
        if semantics is not None:
            body.append(f"    __semantics__ = {semantics!r}")

        body.append(f"    __template__ = {template!r}")

        containment = getattr(args, "containment", None) if args else None
        if containment is None:
            containment = spec.get("containment")
        elif isinstance(containment, str):
            import json, yaml
            containment = json.loads(containment) if (containment.startswith("{") or containment.startswith("[")) else yaml.safe_load(containment)
        if containment is not None:
            body.append(f"    __containment__ = {containment!r}")

        references = getattr(args, "references", None) if args else None
        if references is None:
            references = spec.get("references")
        elif isinstance(references, str):
            import json, yaml
            references = json.loads(references) if (references.startswith("{") or references.startswith("[")) else yaml.safe_load(references)
        if references is not None:
            body.append(f"    __references__ = {references!r}")

        compositions = getattr(args, "compositions", None) if args else None
        if compositions is None:
            compositions = spec.get("compositions")
        elif isinstance(compositions, str):
            import json, yaml
            compositions = json.loads(compositions) if (compositions.startswith("{") or compositions.startswith("[")) else yaml.safe_load(compositions)
        if compositions is not None:
            body.append(f"    __compositions__ = {compositions!r}")

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
