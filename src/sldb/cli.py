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

    # ── store ────────────────────────────────────────────────────────────────
    store_parser = subparsers.add_parser(
        "store",
        help="Store-level operations: init, federation, integrity check, full reindex.",
        description=(
            "Manages the .sldb/ pointer database. The store is a three-level YAML index cascade "
            "(store_index → models_index → documents_index) that tracks model contracts and "
            "their document instances via a Merkle-style hash chain (hash_a/hash_b/hash_c/hash_d).\n\n"
            "Typical workflow:\n"
            "  sldb store init                   # create .sldb/ in project root\n"
            "  sldb model add myapp.models:Book  # register a model contract\n"
            "  sldb doc add --model Book -o book.md data.yaml  # create + track a document\n"
            "  sldb store check                  # verify integrity\n\n"
            "Scopes: local (.sldb/) takes precedence over global (~/.sldb/)."
        ),
    )
    store_sub = store_parser.add_subparsers(dest="store_command", required=True)

    _si = store_sub.add_parser(
        "init",
        help="Initialize a .sldb/ store in a project directory.",
        description="Creates .sldb/store_index.yaml with empty stores/models arrays.",
    )
    _si.add_argument("--path", default=".", help="Project root. Defaults to current directory.")
    _si.add_argument("--force", action="store_true", help="Overwrite existing store.")

    _sa = store_sub.add_parser(
        "add",
        help="Link a federated store.",
        description=(
            "Adds another store as a federation dependency in the stores: array of store_index.yaml. "
            "The linked store's models become resolvable from the current store at query time."
        ),
    )
    _sa.add_argument("path", help="Path to the other store's .sldb directory.")
    _sa.add_argument("--name", default=None, help="Name for the linked store. Defaults to its parent directory name.")
    _sa.add_argument("--store", default=None, help="Path to the local .sldb directory.")

    _sc = store_sub.add_parser(
        "check",
        help="Run integrity diagnostics on the hash cascade.",
        description=(
            "Walks the hash cascade and reports fractures without modifying anything. "
            "hash_c covers raw text; hash_d covers extracted field values. "
            "If hash_c changes but hash_d is stable the mutation is benign (e.g. a rendered date). "
            "If hash_d changes, field values were edited. If a path is missing, the document was moved or deleted."
        ),
    )
    _sc.add_argument("--store", default=None, help="Path to .sldb directory.")
    _sc.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    _sc.add_argument("--pythonpath", default=None, help="Path to prepend when importing models.")

    _su = store_sub.add_parser(
        "update",
        help="Recompute all hashes from current file states (full reindex).",
        description=(
            "Walks every tracked document, recomputes hash_c and hash_d, "
            "then propagates updated hash_b and hash_a upward. Use after bulk edits or moves."
        ),
    )
    _su.add_argument("--store", default=None, help="Path to .sldb directory.")
    _su.add_argument("--pythonpath", default=None)

    # ── model ────────────────────────────────────────────────────────────────
    model_parser = subparsers.add_parser(
        "model",
        help="Register and manage model contracts in the store.",
        description=(
            "Model contracts are Pydantic StructuredNLDoc subclasses. "
            "Once registered, models are referenced by name in doc commands."
        ),
    )
    model_sub = model_parser.add_subparsers(dest="model_command", required=True)

    _ma = model_sub.add_parser(
        "add",
        help="Register a model contract in the local store.",
        description=(
            "Imports the model class, records its physical path and module reference in the store, "
            "and creates empty models_index and documents_index files for it."
        ),
    )
    _ma.add_argument("model", help="Model reference, e.g. myapp.models:Book.")
    _ma.add_argument("--store", default=None, help="Path to .sldb directory.")
    _ma.add_argument("--pythonpath", default=None)

    _mu = model_sub.add_parser(
        "update",
        help="Re-index a model after its contract (fields or template) changed.",
        description=(
            "Re-imports the model class and recomputes hash_d for every tracked document "
            "under that model, then propagates hash_b and hash_a. "
            "Run this after changing Pydantic fields or __template__."
        ),
    )
    _mu.add_argument("name", help="Registered model name, e.g. Book.")
    _mu.add_argument("--store", default=None, help="Path to .sldb directory.")
    _mu.add_argument("--pythonpath", default=None)

    # ── doc ──────────────────────────────────────────────────────────────────
    doc_parser = subparsers.add_parser(
        "doc",
        help="Create and manage document instances in the store.",
        description=(
            "Documents are .md files that conform to a registered model's template. "
            "Use 'add' to create a new document from data, 'track' to register an existing one."
        ),
    )
    doc_sub = doc_parser.add_subparsers(dest="doc_command", required=True)

    _da = doc_sub.add_parser(
        "add",
        help="Create a new document from a payload and track it in the store.",
        description=(
            "Renders the model template with the provided data, validates idempotency, "
            "writes the result to the output path, and tracks it in the store. "
            "The model must already be registered with 'sldb model add'."
        ),
    )
    _da.add_argument("--model", required=True, help="Registered model name, e.g. Book.")
    _da.add_argument("-o", "--output", required=True, help="Output .md file path.")
    _da.add_argument("payload", help="JSON/YAML data: a file path or an inline JSON/YAML string.")
    _da.add_argument("--name", default=None, help="Logical document name. Defaults to output file stem.")
    _da.add_argument("--store", default=None, help="Path to .sldb directory.")
    _da.add_argument("--pythonpath", default=None)

    _dt = doc_sub.add_parser(
        "track",
        help="Validate and track an existing document in the store.",
        description=(
            "Runs an idempotency check (extract → render → extract) on the document before tracking. "
            "Fails if the document does not roundtrip cleanly. Use --force to track anyway."
        ),
    )
    _dt.add_argument("path", help="Path to the existing .md document.")
    _dt.add_argument("--model", required=True, help="Registered model name.")
    _dt.add_argument("--name", default=None, help="Logical document name. Defaults to file stem.")
    _dt.add_argument("--store", default=None, help="Path to .sldb directory.")
    _dt.add_argument("--pythonpath", default=None)
    _dt.add_argument("--force", action="store_true", help="Track even if idempotency check fails.")

    _dU = doc_sub.add_parser(
        "update",
        help="Re-render a tracked document with new data and update its hashes.",
        description=(
            "Merges the new payload over the tracked document's current field values, "
            "re-renders the markdown, overwrites the file, and recomputes hash_c/hash_d/hash_b/hash_a."
        ),
    )
    _dU.add_argument("name", help="Document name as registered in the store.")
    _dU.add_argument("--model", required=True, help="Registered model name.")
    _dU.add_argument("payload", help="New JSON/YAML data: a file path or an inline JSON/YAML string.")
    _dU.add_argument("--store", default=None, help="Path to .sldb directory.")
    _dU.add_argument("--pythonpath", default=None)

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

    if args.command in ("store", "model", "doc"):
        import dataclasses
        import inspect
        from sldb.store.io import (
            load_store_index, save_store_index,
            load_models_index, save_models_index,
            load_documents_index, save_documents_index,
        )
        from sldb.store.models import StoreIndex, StoreEntry, ModelEntry, ModelsIndex, DocumentsIndex, DocumentEntry
        from sldb.store.hashing import hash_documents_index, hash_models_layer, hash_text, hash_fields
        from sldb.store.resolver import find_local_store

        def _resolve_store(store_arg: str | None) -> Path:
            if store_arg:
                return Path(store_arg).resolve()
            found = find_local_store()
            if not found:
                raise SystemExit("No .sldb store found. Run 'sldb store init' first.")
            return found

        def _parse_payload(payload_arg: str) -> Dict[str, Any]:
            p = Path(payload_arg)
            if p.exists():
                return _read_mapping(str(p))
            try:
                data = yaml.safe_load(payload_arg)
            except yaml.YAMLError as exc:
                raise SystemExit(f"Could not parse payload: {exc}")
            if not isinstance(data, dict):
                raise SystemExit("Payload must be a JSON/YAML object.")
            return data

        def _registered_model(store_path: Path, model_name: str, pythonpath: str | None):
            store_index = load_store_index(store_path)
            entry = next((m for m in store_index.models if m.name == model_name), None)
            if entry is None:
                raise SystemExit(f"Model '{model_name}' not registered. Run 'sldb model add' first.")
            model_type = _resolve_model_ref(entry.model_ref, pythonpath)
            return model_type, entry, store_index

        def _track_document(store_path, project_root, store_index, model_type, model_entry, doc_path, doc_name):
            models_idx = load_models_index(project_root / model_entry.models_index)
            docs_idx = load_documents_index(project_root / models_idx.documents_index)
            if any(d.name == doc_name for d in docs_idx.documents):
                raise SystemExit(f"Document '{doc_name}' is already tracked under '{model_type.__name__}'.")
            try:
                doc_rel = str(doc_path.relative_to(project_root))
            except ValueError:
                doc_rel = str(doc_path)
            text = doc_path.read_text(encoding="utf-8")
            try:
                h_d = hash_fields(model_type, text)
            except Exception:
                h_d = ""
            docs_idx.documents.append(DocumentEntry(
                name=doc_name, path=doc_rel,
                hash_c=hash_text(text),
                hash_d=h_d,
            ))
            save_documents_index(project_root / models_idx.documents_index, docs_idx)
            models_idx.hash_b = hash_documents_index(docs_idx)
            save_models_index(project_root / model_entry.models_index, models_idx)
            _cascade_hash_a(store_path, project_root, store_index)

        def _cascade_hash_a(store_path, project_root, store_index):
            all_indices = [load_models_index(project_root / m.models_index) for m in store_index.models]
            store_index.hash_a = hash_models_layer(all_indices)
            save_store_index(store_path, store_index)

        def _reindex_model_docs(store_path, project_root, store_index, model_entry, model_type):
            models_idx = load_models_index(project_root / model_entry.models_index)
            docs_idx = load_documents_index(project_root / models_idx.documents_index)
            for doc in docs_idx.documents:
                doc_path = project_root / doc.path
                if doc_path.exists():
                    text = doc_path.read_text(encoding="utf-8")
                    doc.hash_c = hash_text(text)
                    doc.hash_d = hash_fields(model_type, text)
            save_documents_index(project_root / models_idx.documents_index, docs_idx)
            models_idx.hash_b = hash_documents_index(docs_idx)
            save_models_index(project_root / model_entry.models_index, models_idx)

        # ── store ─────────────────────────────────────────────────────────────
        if args.command == "store":
            if args.store_command == "init":
                project_root = Path(args.path).resolve()
                store_path = project_root / ".sldb"
                if (store_path / "store_index.yaml").exists() and not args.force:
                    raise SystemExit(f"Store already exists at {store_path}. Use --force to overwrite.")
                save_store_index(store_path, StoreIndex())
                sys.stdout.write(f"Initialized store at {store_path}\n")
                return 0

            if args.store_command == "add":
                store_path = _resolve_store(getattr(args, "store", None))
                project_root = store_path.parent
                other = Path(args.path).resolve()
                if not (other / "store_index.yaml").exists():
                    raise SystemExit(f"No valid store found at {other}")
                store_index = load_store_index(store_path)
                name = args.name or other.parent.name
                if any(s.name == name for s in store_index.stores):
                    raise SystemExit(f"Store '{name}' is already linked.")
                try:
                    rel = str(other.relative_to(project_root))
                except ValueError:
                    rel = str(other)
                store_index.stores.append(StoreEntry(name=name, path=rel))
                save_store_index(store_path, store_index)
                sys.stdout.write(f"Linked store '{name}' at {rel}\n")
                return 0

            if args.store_command == "check":
                from sldb.store.diagnostics import diagnose_store, DiagnosisNote
                store_path = _resolve_store(args.store)
                project_root = store_path.parent
                result = diagnose_store(store_path, project_root, pythonpath=args.pythonpath)
                if args.format == "text":
                    sys.stdout.write(f"{'PASS' if result.is_valid else 'FAIL'}: store integrity check\n")
                    for m in result.models:
                        sys.stdout.write(f"  model {m.name}: {'ok' if m.hash_b_ok else 'FAIL(hash_b)'}\n")
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

            if args.store_command == "update":
                store_path = _resolve_store(args.store)
                project_root = store_path.parent
                store_index = load_store_index(store_path)
                for model_entry in store_index.models:
                    try:
                        model_type = _resolve_model_ref(model_entry.model_ref, args.pythonpath)
                    except SystemExit:
                        model_type = None
                    if model_type:
                        _reindex_model_docs(store_path, project_root, store_index, model_entry, model_type)
                _cascade_hash_a(store_path, project_root, store_index)
                sys.stdout.write(f"Store reindexed at {store_path}\n")
                return 0

        # ── model ─────────────────────────────────────────────────────────────
        if args.command == "model":
            if args.model_command == "add":
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
                    name=model_type.__name__, model_ref=args.model, path=model_path,
                    documents_index=docs_index_rel, hash_b=hash_documents_index(docs_index),
                )
                save_models_index(project_root / models_index_rel, models_idx)
                store_index.models.append(ModelEntry(
                    name=model_type.__name__, model_ref=args.model,
                    path=model_path, models_index=models_index_rel,
                ))
                _cascade_hash_a(store_path, project_root, store_index)
                sys.stdout.write(f"Registered model '{model_type.__name__}'\n")
                return 0

            if args.model_command == "update":
                store_path = _resolve_store(args.store)
                project_root = store_path.parent
                model_type, model_entry, store_index = _registered_model(store_path, args.name, args.pythonpath)
                _reindex_model_docs(store_path, project_root, store_index, model_entry, model_type)
                _cascade_hash_a(store_path, project_root, store_index)
                sys.stdout.write(f"Reindexed model '{args.name}'\n")
                return 0

        # ── doc ───────────────────────────────────────────────────────────────
        if args.command == "doc":
            if args.doc_command == "add":
                store_path = _resolve_store(args.store)
                project_root = store_path.parent
                model_type, model_entry, store_index = _registered_model(store_path, args.model, args.pythonpath)
                data = _parse_payload(args.payload)
                rendered = render_model_markdown(model_type, data)
                is_valid, details = validate_model_input_roundtrip(model_type, rendered)
                if not is_valid:
                    raise SystemExit(
                        f"Rendered document is not idempotent.\n"
                        f"First payload:  {details['first_payload']}\n"
                        f"Second payload: {details['second_payload']}"
                    )
                out_path = Path(args.output).resolve()
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(rendered + "\n", encoding="utf-8")
                doc_name = args.name or out_path.stem
                _track_document(store_path, project_root, store_index, model_type, model_entry, out_path, doc_name)
                sys.stdout.write(f"Created and tracked '{doc_name}' at {out_path}\n")
                return 0

            if args.doc_command == "track":
                store_path = _resolve_store(args.store)
                project_root = store_path.parent
                model_type, model_entry, store_index = _registered_model(store_path, args.model, args.pythonpath)
                doc_path = Path(args.path).resolve()
                if not doc_path.exists():
                    raise SystemExit(f"Document not found: {doc_path}")
                text = doc_path.read_text(encoding="utf-8")
                try:
                    is_valid, details = validate_model_input_roundtrip(model_type, text)
                except Exception as exc:
                    if not args.force:
                        raise SystemExit(f"Document failed idempotency check: {exc}\nUse --force to track anyway.")
                    is_valid = False
                if not is_valid and not args.force:
                    raise SystemExit(
                        f"Document failed idempotency check. Use --force to track anyway.\n"
                        f"First payload:  {details['first_payload']}\n"
                        f"Second payload: {details['second_payload']}"
                    )
                doc_name = args.name or doc_path.stem
                _track_document(store_path, project_root, store_index, model_type, model_entry, doc_path, doc_name)
                sys.stdout.write(f"Tracked '{doc_name}' under '{args.model}'\n")
                return 0

            if args.doc_command == "update":
                store_path = _resolve_store(args.store)
                project_root = store_path.parent
                model_type, model_entry, store_index = _registered_model(store_path, args.model, args.pythonpath)
                models_idx = load_models_index(project_root / model_entry.models_index)
                docs_idx = load_documents_index(project_root / models_idx.documents_index)
                doc_entry = next((d for d in docs_idx.documents if d.name == args.name), None)
                if doc_entry is None:
                    raise SystemExit(f"Document '{args.name}' not found under '{args.model}'.")
                new_data = _parse_payload(args.payload)
                rendered = render_model_markdown(model_type, new_data)
                doc_path = project_root / doc_entry.path
                doc_path.write_text(rendered + "\n", encoding="utf-8")
                text = doc_path.read_text(encoding="utf-8")
                doc_entry.hash_c = hash_text(text)
                doc_entry.hash_d = hash_fields(model_type, text)
                save_documents_index(project_root / models_idx.documents_index, docs_idx)
                models_idx.hash_b = hash_documents_index(docs_idx)
                save_models_index(project_root / model_entry.models_index, models_idx)
                _cascade_hash_a(store_path, project_root, store_index)
                sys.stdout.write(f"Updated '{args.name}'\n")
                return 0

    parser.error("Unknown command")
    return 2
