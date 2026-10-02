from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import yaml

from sldb.cli.utils import read_text, write_text
from sldb.cli.model_utils import resolve_model_ref
from sldb.runtime.validation import (
    extract_model_data,
    render_model_markdown,
    validate_model_data_roundtrip,
    validate_model_input_roundtrip,
)


class BasicCLI:
    """Handles basic SLDB operations: extract, render, validate."""

    def extract(self, args: Any) -> int:
        model_type = resolve_model_ref(args.model, args.pythonpath)
        payload = extract_model_data(model_type, read_text(args.input))
        fmt = self._get_format(args)
        output = yaml.safe_dump(payload) if fmt == "yaml" else json.dumps(payload, indent=2)
        write_text(args.output, output)
        return 0

    def _get_format(self, args: Any) -> str:
        if args.format:
            return args.format
        return "yaml" if str(args.output).endswith((".yaml", ".yml")) else "json"

    def render(self, args: Any) -> int:
        """Render a payload to Markdown. `--ref-root` is where a composed field's refs resolve."""
        model_type = resolve_model_ref(args.model, args.pythonpath)
        data = yaml.safe_load(read_text(args.input))
        ref_root = getattr(args, "ref_root", None)
        output = render_model_markdown(model_type, data, Path(ref_root) if ref_root else None)
        write_text(args.output, output + "\n")
        return 0

    def validate(self, args: Any) -> int:
        model_type = resolve_model_ref(args.model, args.pythonpath)
        valid, details = self._run_validation(model_type, args)
        self._print_validation(valid, details, args)
        return 0 if valid else 1

    def _run_validation(self, model_type: Any, args: Any) -> tuple[bool, dict]:
        if args.input:
            return validate_model_input_roundtrip(model_type, read_text(args.input))
        return validate_model_data_roundtrip(model_type, yaml.safe_load(read_text(args.data)))

    def _print_validation(self, valid: bool, details: dict, args: Any) -> None:
        if args.format == "text":
            mode = "input" if args.input else "data"
            print(f"{'PASS' if valid else 'FAIL'}: model is idempotent in {mode} mode")
        else:
            print(json.dumps({"valid": valid, **details}, indent=2))
