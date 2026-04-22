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
            "Model rule: every StructuredNLDoc field must define a non-empty Pydantic description "
            "so humans and LLMs can read the model as a guided document contract.\n\n"
            "Benefits: human-readable source of truth, machine-extractable typed data, "
            "one artifact for both writing and parsing, easier validation/automation/diffing, "
            "and safer roundtrips.\n\n"
            "Basics: define a StructuredNLDoc model, put the Markdown contract in __template__, "
            "declare fields with Field(description=...), "
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
            "choose field types that match the block shape, write meaningful field descriptions, and validate "
            "roundtrips early."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract model data from a Markdown document.",
        description="Load a StructuredNLDoc model with described fields and extract typed data from Markdown.",
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
        description="Load a StructuredNLDoc model with described fields and render Markdown from JSON or YAML data.",
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
        description="Validate that a described StructuredNLDoc model roundtrips cleanly between Markdown and typed data.",
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
        description="Write a reusable SLDB skill file that reminds agents to keep StructuredNLDoc fields documented and validated.",
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
        description="Create a working example bundle with Field(description=...) usage, Markdown input, YAML data, and docs.",
    )
    example_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory where the example folder will be created. Defaults to current directory.",
    )

    store_parser = subparsers.add_parser(
        "store",
        help="Manage the SLDB store.",
        description="Initialize stores, register models and documents, and check integrity.",
    )
    store_sub = store_parser.add_subparsers(dest="store_command", required=True)

    _store_init = store_sub.add_parser("init", help="Initialize an SLDB store.")
    _store_init.add_argument("--path", default=".", help="Project root directory.")
    _store_init.add_argument("--force", action="store_true", help="Overwrite existing store.")

    _store_add = store_sub.add_parser("add", help="Register a model in the store.")
    _store_add.add_argument("model", help="Model reference, e.g. myapp.models:Book.")
    _store_add.add_argument("--store", default=None, help="Path to .sldb directory.")
    _store_add.add_argument("--pythonpath", default=None)

    _store_track = store_sub.add_parser("track", help="Register a document instance.")
    _store_track.add_argument("model", help="Model reference.")
    _store_track.add_argument("document", help="Path to the .md document.")
    _store_track.add_argument("--name", default=None, help="Logical name. Defaults to file stem.")
    _store_track.add_argument("--store", default=None, help="Path to .sldb directory.")
    _store_track.add_argument("--pythonpath", default=None)

    _store_check = store_sub.add_parser("check", help="Run integrity diagnostics.")
    _store_check.add_argument("--store", default=None, help="Path to .sldb directory.")
    _store_check.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    _store_check.add_argument("--pythonpath", default=None)

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
        sys.stdout.write(
            "  Review `guide_model.py` for the required Field(description=...) pattern.\n"
        )
        sys.stdout.write(f"  (from within the {target_root} directory)\n")
        return 0

    if args.command == "store":
        import dataclasses
        import inspect
        from sldb.store.io import (
            load_store_index, save_store_index,
            load_models_index, save_models_index,
            load_documents_index, save_documents_index,
        )
        from sldb.store.models import StoreIndex, ModelEntry, ModelsIndex, DocumentsIndex, DocumentEntry
        from sldb.store.hashing import hash_documents_index, hash_models_layer, hash_text, hash_fields
        from sldb.store.resolver import find_local_store

        def _resolve_store(store_arg: str | None) -> Path:
            if store_arg:
                return Path(store_arg).resolve()
            found = find_local_store()
            if not found:
                raise SystemExit("No .sldb store found. Run 'sldb store init' first.")
            return found

        if args.store_command == "init":
            project_root = Path(args.path).resolve()
            store_path = project_root / ".sldb"
            if (store_path / "store_index.yaml").exists() and not args.force:
                raise SystemExit(f"Store already exists at {store_path}. Use --force to overwrite.")
            save_store_index(store_path, StoreIndex())
            sys.stdout.write(f"Initialized store at {store_path}\n")
            return 0

        if args.store_command == "add":
            store_path = _resolve_store(args.store)
            project_root = store_path.parent
            model_type = _resolve_model_ref(args.model, args.pythonpath)
            store_index = load_store_index(store_path)

            if any(m.name == model_type.__name__ for m in store_index.models):
                raise SystemExit(f"Model '{model_type.__name__}' is already registered.")

            model_file = Path(inspect.getfile(model_type))
            try:
                model_path = str(model_file.relative_to(project_root))
            except ValueError:
                model_path = str(model_file)

            models_index_rel = f".sldb/models/{model_type.__name__}.yaml"
            docs_index_rel = f".sldb/documents/{model_type.__name__}.yaml"

            docs_index = DocumentsIndex()
            save_documents_index(project_root / docs_index_rel, docs_index)

            models_idx = ModelsIndex(
                name=model_type.__name__,
                model_ref=args.model,
                path=model_path,
                documents_index=docs_index_rel,
                hash_b=hash_documents_index(docs_index),
            )
            save_models_index(project_root / models_index_rel, models_idx)

            store_index.models.append(ModelEntry(
                name=model_type.__name__,
                model_ref=args.model,
                path=model_path,
                models_index=models_index_rel,
            ))
            all_indices = [load_models_index(project_root / m.models_index) for m in store_index.models]
            store_index.hash_a = hash_models_layer(all_indices)
            save_store_index(store_path, store_index)

            sys.stdout.write(f"Registered model '{model_type.__name__}' in {store_path}\n")
            return 0

        if args.store_command == "track":
            store_path = _resolve_store(args.store)
            project_root = store_path.parent
            model_type = _resolve_model_ref(args.model, args.pythonpath)
            store_index = load_store_index(store_path)

            model_entry = next((m for m in store_index.models if m.name == model_type.__name__), None)
            if model_entry is None:
                raise SystemExit(f"Model '{model_type.__name__}' is not registered. Run 'sldb store add' first.")

            doc_path = Path(args.document).resolve()
            try:
                doc_rel = str(doc_path.relative_to(project_root))
            except ValueError:
                doc_rel = str(doc_path)

            doc_name = args.name or doc_path.stem
            models_idx = load_models_index(project_root / model_entry.models_index)
            docs_idx = load_documents_index(project_root / models_idx.documents_index)

            if any(d.name == doc_name for d in docs_idx.documents):
                raise SystemExit(f"Document '{doc_name}' is already tracked under '{model_type.__name__}'.")

            text = doc_path.read_text(encoding="utf-8")
            docs_idx.documents.append(DocumentEntry(
                name=doc_name,
                path=doc_rel,
                hash_c=hash_text(text),
                hash_d=hash_fields(model_type, text),
            ))
            save_documents_index(project_root / models_idx.documents_index, docs_idx)

            models_idx.hash_b = hash_documents_index(docs_idx)
            save_models_index(project_root / model_entry.models_index, models_idx)

            all_indices = [load_models_index(project_root / m.models_index) for m in store_index.models]
            store_index.hash_a = hash_models_layer(all_indices)
            save_store_index(store_path, store_index)

            sys.stdout.write(f"Tracked document '{doc_name}' under '{model_type.__name__}'\n")
            return 0

        if args.store_command == "check":
            from sldb.store.diagnostics import diagnose_store, DiagnosisNote

            store_path = _resolve_store(args.store)
            project_root = store_path.parent
            result = diagnose_store(store_path, project_root, pythonpath=args.pythonpath)

            if args.format == "text":
                status = "PASS" if result.is_valid else "FAIL"
                sys.stdout.write(f"{status}: store integrity check\n")
                for m in result.models:
                    b = "ok" if m.hash_b_ok else "FAIL(hash_b)"
                    sys.stdout.write(f"  model {m.name}: {b}\n")
                    for d in m.documents:
                        sys.stdout.write(f"    doc {d.name} [{d.path}]: {d.note.value}\n")
            else:
                def _ser(obj):
                    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
                        return {f.name: _ser(getattr(obj, f.name)) for f in dataclasses.fields(obj)}
                    if isinstance(obj, list):
                        return [_ser(i) for i in obj]
                    if isinstance(obj, DiagnosisNote):
                        return obj.value
                    return obj

                payload = {"valid": result.is_valid, "hash_a_ok": result.hash_a_ok, "models": _ser(result.models)}
                sys.stdout.write(_serialize_structured_output(payload, args.format))

            return 0 if result.is_valid else 1

    parser.error("Unknown command")
    return 2
