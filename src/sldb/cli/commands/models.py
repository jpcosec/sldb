"""Models CLI commands module."""
from __future__ import annotations

from typing import Any
import yaml

from sldb.cli.commands.model import ModelCLI
from sldb.cli.graph_ops import ast_for_target
from sldb.cli.commands.models_list import ModelsListCLI
from sldb.cli.commands.models_create import ModelsCreateCLI
from sldb.cli.commands.models_validate import ModelsValidateCLI
from sldb.cli.commands.models_template import ModelsTemplateCLI
from sldb.cli.commands.models_fields import ModelsFieldsCLI

class ModelsCLI:
    """Plural model surface for the redesigned CLI."""

    def __init__(self) -> None:
        """Initialize ModelsCLI with all sub-command handlers."""
        self._model = ModelCLI()
        self._list_cli = ModelsListCLI()
        self._create_cli = ModelsCreateCLI()
        self._validate_cli = ModelsValidateCLI()
        self._template_cli = ModelsTemplateCLI()
        self._fields_cli = ModelsFieldsCLI()

    def run(self, args: Any) -> int:
        """Run the appropriate models subcommand.

        Args:
            args (Any): The parsed arguments from the CLI.

        Returns:
            int: The exit code of the executed subcommand.
        """
        cmd = args.models_command
        if cmd in {"add", "update"}:
            args.model_command = cmd
            return self._model.run(args)
        return self._run_subcommand(cmd, args)

    def _run_subcommand(self, cmd: str, args: Any) -> int:
        handlers = {"remove": self._remove, "inherit": self._inherit, "list": self._list_cli.list, "show": self._show, "create": self._create_cli.create, "validate": self._run_validate, "template": self._template_cli.template, "fields": self._fields_cli.fields}
        if cmd in handlers:
            return handlers[cmd](args)
        raise SystemExit(f"Unknown models command: {cmd}")

    def _remove(self, args: Any) -> int:
        from sldb.api import remove_model

        removed = remove_model(args.store, args.model, args.pythonpath, untrack_documents=args.with_documents)
        print(f"Removed model: {removed.name} ({removed.model_ref})")
        return 0

    def _inherit(self, args: Any) -> int:
        from sldb.api import inherit_model

        inherited = inherit_model(args.store, args.model, args.pythonpath)
        print(f"Inherited model: {inherited.name} ({inherited.model_ref}) from '{args.model.split(':', 1)[0]}'")
        return 0

    def _run_validate(self, args: Any) -> int:
        return self._validate_cli.validate(args, self._model)

    def _show(self, args: Any) -> int:
        payload = ast_for_target(args.store, args.pythonpath, f"models/{args.model}")
        print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
        return 0
