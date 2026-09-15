from __future__ import annotations

import contextlib
import json
import sys
from pathlib import Path
from typing import Any
import yaml

from sldb.core.exceptions import SLDBModelDraftError, SLDBModelEditError, SLDBModelError, SLDBValidationError
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.cli.commands.models_utils import registered_model_source, draft_path as get_draft_path, load_model_from_path, tracked_docs_for_model
from sldb.cli.commands.models_validate_utils import restored_on_failure, store_index_files, validate_template_contract

class ModelsValidateCLI:
    def validate(self, args: Any, model_cli: Any) -> int:
        path, mod, attr = registered_model_source(args)
        d_path = get_draft_path(path)
        m_path = d_path if d_path.exists() else path
        m_type = load_model_from_path(m_path, mod, attr, args.pythonpath)
        details = self._init_validate_details(args.model, d_path, m_path)
        self._run_validations(args, m_type, details)
        self._handle_promotion(args, path, d_path, details, model_cli)
        return self._output_validate(args, details)

    def _init_validate_details(self, model: str, d_path: Path, m_path: Path) -> dict[str, Any]:
        return {"model": model, "draft": d_path.exists(), "path": str(m_path), "documents": []}

    def _run_validations(self, args: Any, m_type: Any, details: dict[str, Any]) -> None:
        try:
            validate_template_contract(m_type)
            for d_name, d_path in tracked_docs_for_model(args):
                self._validate_doc(args.model, d_name, d_path, m_type, details)
        except (SLDBValidationError, SLDBModelError):
            raise
        except Exception as exc:
            raise SLDBModelEditError(f"Draft for '{args.model}' is invalid: {exc}") from exc

    def _validate_doc(self, model: str, d_name: str, d_path: str, m_type: Any, details: dict[str, Any]) -> None:
        valid, d_details = validate_model_input_roundtrip(m_type, Path(d_path).read_text(encoding="utf-8"))
        details["documents"].append({"name": d_name, "path": d_path, "valid": valid})
        if not valid:
            raise SLDBValidationError(f"Draft for '{model}' failed validation on '{d_name}'.", d_details)

    def _handle_promotion(self, args: Any, path: Path, d_path: Path, details: dict[str, Any], model_cli: Any) -> None:
        if args.promote:
            self._promote_draft(args, path, d_path, details, model_cli)
        else:
            details["promoted"] = False

    def _promote_draft(self, args: Any, path: Path, draft_path: Path, details: dict[str, Any], model_cli: Any) -> None:
        """Install the draft and reindex. If the reindex fails, the active model, the draft and the
        indexes are put back, so the store stays consistent and the promote can be retried."""
        if not draft_path.exists():
            raise SLDBModelDraftError(f"No draft template for '{args.model}' to promote.")
        with restored_on_failure([path, draft_path, *store_index_files(args.store)]):
            path.write_text(draft_path.read_text(encoding="utf-8"), encoding="utf-8")
            self._reindex(args, model_cli)
        draft_path.unlink()
        details["promoted"] = True

    def _reindex(self, args: Any, model_cli: Any) -> None:
        args.model_command = "update"
        args.bump_version = True
        # --format json/yaml promises a parseable stdout: update's progress line goes to stderr.
        with contextlib.redirect_stdout(sys.stderr) if args.format != "text" else contextlib.nullcontext():
            model_cli.update(args)

    def _output_validate(self, args: Any, details: dict[str, Any]) -> int:
        if args.format == "text":
            return self._output_validate_text(args, details)
        res = {"valid": True, **details}
        if args.format == "json":
            print(json.dumps(res, indent=2))
        else:
            print(yaml.safe_dump(res, sort_keys=False, allow_unicode=True))
        return 0

    def _output_validate_text(self, args: Any, details: dict[str, Any]) -> int:
        docs = details["documents"]
        status = "PASS" if not docs or all(d["valid"] for d in docs) else "FAIL"
        d_label = "draft" if details["draft"] else "active model"
        print(f"{status}: validated {d_label} for '{args.model}'")
        return 0

