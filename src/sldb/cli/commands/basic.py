from __future__ import annotations

import json
from typing import Any
import yaml

from sldb.cli.utils import read_text, write_text, resolve_model_ref
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

        fmt = args.format or (
            "yaml" if str(args.output).endswith((".yaml", ".yml")) else "json"
        )
        output = (
            yaml.safe_dump(payload) if fmt == "yaml" else json.dumps(payload, indent=2)
        )
        write_text(args.output, output)
        return 0

    def render(self, args: Any) -> int:
        model_type = resolve_model_ref(args.model, args.pythonpath)
        data = yaml.safe_load(read_text(args.input))
        output = render_model_markdown(model_type, data)
        write_text(args.output, output + "\n")
        return 0

    def validate(self, args: Any) -> int:
        model_type = resolve_model_ref(args.model, args.pythonpath)
        if args.input:
            valid, details = validate_model_input_roundtrip(
                model_type, read_text(args.input)
            )
        else:
            valid, details = validate_model_data_roundtrip(
                model_type, yaml.safe_load(read_text(args.data))
            )

        if args.format == "text":
            mode = "input" if args.input else "data"
            print(f"{'PASS' if valid else 'FAIL'}: model is idempotent in {mode} mode")
        else:
            print(json.dumps({"valid": valid, **details}, indent=2))
        return 0 if valid else 1
