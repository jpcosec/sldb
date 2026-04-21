import argparse
import json
import sys
from importlib import import_module
from importlib.resources import files
from pathlib import Path
from typing import Any, Dict, Type

import yaml

from sldb.structuredNLDoc import StructuredNLDoc
from sldb.validation import (
    extract_model_data,
    render_model_markdown,
    validate_model_data_roundtrip,
    validate_model_input_roundtrip,
)


def _read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def _read_mapping(path: str) -> Dict[str, Any]:
    raw = _read_text(path)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise SystemExit(f"Failed to parse data file: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("Data input must be a JSON/YAML object at the top level.")

    return data


def _write_text(path: str, content: str) -> None:
    if path == "-":
        sys.stdout.write(content)
        return
    Path(path).write_text(content, encoding="utf-8")


def _serialize_structured_output(data: Dict[str, Any], output_format: str) -> str:
    if output_format == "yaml":
        return yaml.safe_dump(data, sort_keys=False)
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def _skills_markdown() -> str:
    return files("sldb.templates").joinpath("sldb.md").read_text(encoding="utf-8")


def _resolve_model_ref(
    model_ref: str, pythonpath: str | None = None
) -> Type[StructuredNLDoc]:
    if ":" not in model_ref:
        raise SystemExit("Model reference must use the form 'module:ClassName'.")

    search_paths = []
    if pythonpath:
        search_paths.append(str(Path(pythonpath).resolve()))
    search_paths.append(str(Path.cwd().resolve()))

    for path in reversed(search_paths):
        if path not in sys.path:
            sys.path.insert(0, path)

    module_name, attr_path = model_ref.split(":", 1)

    try:
        module = import_module(module_name)
    except ImportError as exc:
        raise SystemExit(
            f"Failed to import module '{module_name}' for model '{model_ref}'."
        ) from exc

    obj: Any = module
    try:
        for attr in attr_path.split("."):
            obj = getattr(obj, attr)
    except AttributeError as exc:
        raise SystemExit(
            f"Failed to resolve model attribute '{attr_path}' in module '{module_name}'."
        ) from exc

    if not isinstance(obj, type) or not issubclass(obj, StructuredNLDoc):
        raise SystemExit(
            f"Resolved object '{model_ref}' is not a StructuredNLDoc subclass."
        )

    return obj


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sldb",
        description=(
            "SLDB treats Markdown documents as structured, typed, reversible data. "
            "It exists so a document can be parsed into a StructuredNLDoc/Pydantic model "
            "and rendered back to Markdown while preserving its intended structure.\n\n"
            "Benefits: human-readable source of truth, machine-extractable typed data, "
            "one artifact for both writing and parsing, easier validation/automation/diffing, "
            "and safer roundtrips.\n\n"
            "Basics: define a StructuredNLDoc model, put the Markdown contract in __template__, "
            "and mark variable regions with markers such as ⸢rev•title⸥, ⸢optrev•subtitle⸥, ⸢rev,list•items⸥, "
            "⸢rev,dict•meta⸥, ⸢render•slug⸥, ⸢py•title.upper()⸥, or Jinja2 expressions like {{ title }}. rev markers "
            "are reversible and required, optrev markers are reversible but optional, rev,list markers map repeated "
            "Markdown list items, rev/optrev dict markers map YAML-like mapping blocks, table cells can use reversible "
            "markers inside the template row, and render/py/Jinja2 are non-reversible render-only paths. Python markers "
            "stay literal in safe mode and only evaluate in unsafe mode. The stable "
            "Markdown stays literal; only the "
            "changing spans become markers. "
            "sldb then parses Markdown structurally, extracts values into model fields, renders the model back "
            "to Markdown, and validates idempotent roundtrips.\n\n"
            "To create a good StructuredNLDoc model: start from a real document shape, keep stable prose fixed, "
            "mark only variable parts, use clear field names, let headings and sections anchor the structure, "
            "choose field types that match the block shape, and validate roundtrips early."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract model data from a Markdown document.",
    )
    extract_parser.add_argument(
        "model", help="Model reference, like package.module:DocModel."
    )
    extract_parser.add_argument("input", help="Markdown document file path.")
    extract_parser.add_argument(
        "output", help="Output JSON/YAML file path, or '-' for stdout."
    )
    extract_parser.add_argument(
        "--format",
        choices=("json", "yaml"),
        default=None,
        help="Output format.",
    )
    extract_parser.add_argument(
        "--pythonpath",
        help="Optional project path to prepend when importing the model.",
    )

    render_parser = subparsers.add_parser(
        "render",
        help="Render Markdown from model data.",
    )
    render_parser.add_argument(
        "model", help="Model reference, like package.module:DocModel."
    )
    render_parser.add_argument("input", help="Input JSON/YAML data file path.")
    render_parser.add_argument(
        "output", help="Rendered Markdown output file path, or '-' for stdout."
    )
    render_parser.add_argument(
        "--pythonpath",
        help="Optional project path to prepend when importing the model.",
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate idempotency for a StructuredNLDoc model.",
    )
    validate_parser.add_argument(
        "model", help="Model reference, like package.module:DocModel."
    )
    validate_mode = validate_parser.add_mutually_exclusive_group(required=True)
    validate_mode.add_argument(
        "--input",
        help="Markdown document file path to validate extract-render-extract.",
    )
    validate_mode.add_argument(
        "--data", help="JSON/YAML data file path to validate render-extract."
    )
    validate_parser.add_argument(
        "--format",
        choices=("text", "json", "yaml"),
        default="text",
        help="Validation output format.",
    )
    validate_parser.add_argument(
        "--pythonpath",
        help="Optional project path to prepend when importing the model.",
    )

    init_parser = subparsers.add_parser(
        "init",
        help="Write a minimal SLDB skill file into .skills/sldb/SKILL.md.",
    )
    init_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Target project directory. Defaults to current directory.",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing .skills/sldb/SKILL.md file.",
    )

    example_parser = subparsers.add_parser(
        "example",
        help="Create a comprehensive sldb example in an sldb_example folder.",
    )
    example_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory where the example folder will be created. Defaults to current directory.",
    )

    return parser


def main(argv: Any = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "extract":
        model_type = _resolve_model_ref(args.model, args.pythonpath)
        payload = extract_model_data(model_type, _read_text(args.input))

        output_format = args.format
        if output_format is None:
            output_format = (
                "yaml" if str(args.output).endswith((".yaml", ".yml")) else "json"
            )

        _write_text(args.output, _serialize_structured_output(payload, output_format))
        return 0

    if args.command == "render":
        model_type = _resolve_model_ref(args.model, args.pythonpath)
        output = render_model_markdown(model_type, _read_mapping(args.input))
        _write_text(args.output, output + "\n")
        return 0

    if args.command == "validate":
        model_type = _resolve_model_ref(args.model, args.pythonpath)
        if args.input:
            is_valid, details = validate_model_input_roundtrip(
                model_type, _read_text(args.input)
            )
        else:
            is_valid, details = validate_model_data_roundtrip(
                model_type, _read_mapping(args.data)
            )

        if args.format == "text":
            status = "PASS" if is_valid else "FAIL"
            sys.stdout.write(
                f"{status}: model is idempotent in {details['mode']} mode\n"
            )
        else:
            payload = {"valid": is_valid, **details}
            sys.stdout.write(_serialize_structured_output(payload, args.format))
        return 0 if is_valid else 1

    if args.command == "init":
        target_dir = Path(args.path)
        skills_dir = target_dir / ".skills" / "sldb"
        skills_file = skills_dir / "SKILL.md"

        if skills_file.exists() and not args.force:
            raise SystemExit(
                f"Refusing to overwrite existing file: {skills_file}. Use --force to replace it."
            )

        skills_dir.mkdir(parents=True, exist_ok=True)
        skills_file.write_text(_skills_markdown(), encoding="utf-8")
        sys.stdout.write(f"Wrote {skills_file}\n")
        return 0

    if args.command == "example":
        target_root = Path(args.path) / "sldb_example"
        target_root.mkdir(parents=True, exist_ok=True)

        bundle_path = files("sldb.templates").joinpath("example_bundle")
        for item in bundle_path.iterdir():
            if (
                item.is_file()
                and item.name != "__init__.py"
                and "__pycache__" not in str(item)
            ):
                target_file = target_root / item.name
                target_file.write_text(
                    item.read_text(encoding="utf-8"), encoding="utf-8"
                )
                sys.stdout.write(f"Wrote {target_file}\n")

        sys.stdout.write(f"\nCreated comprehensive example in {target_root}\n")
        sys.stdout.write(f"To test it, run:\n")
        sys.stdout.write(
            f"  sldb validate guide_model:SLDBGuide --input guide.input.md --pythonpath .\n"
        )
        sys.stdout.write(f"  (from within the {target_root} directory)\n")
        return 0

    parser.error("Unknown command")
    return 2
