"""`sldb views run|list`: thin printing wrappers over `sldb.api.run_view` and `sldb.api.list_views`.

With `--format json` the output is exactly the API's result (`run_view`'s mapping, or
`{"views": [...]}`), the same JSON `GET /views/<name>` and `GET /views` answer with.
"""

from __future__ import annotations

from typing import Any

from sldb.api.views import list_views, run_view
from sldb.cli.output_format import emit
from sldb.core.exceptions import SLDBError


class ViewsCLI:
    """The composed views of a store through the CLI."""

    def run(self, args: Any) -> int:
        commands = {"run": self.run_view, "list": self.list}
        if args.views_command not in commands:
            raise SLDBError(f"Unknown command: {args.views_command}")
        return commands[args.views_command](args)

    def run_view(self, args: Any) -> int:
        result = run_view(args.store, args.name, args.param or {})
        emit(result, args.format, "\n".join(_result_lines(result)))
        return 0

    def list(self, args: Any) -> int:
        views = list_views(args.store)
        emit({"views": views}, args.format, "\n".join(_view_line(v) for v in views) or "No composed views")
        return 0


def _view_line(view: dict[str, Any]) -> str:
    params = ", ".join(p["name"] + ("*" if p["required"] else "") for p in view["params"])
    return f"{view['name']}: {view['title']} [{', '.join(view['sections'])}]" + (f" params: {params}" if params else "")


def _result_lines(result: dict[str, Any]) -> list[str]:
    lines = [f"view {result['view']} revision {result['revision'][:12]}" + (f" params {result['params']}" if result["params"] else "")]
    for key, section in result["sections"].items():
        lines.append(f"{key}:")
        for value, rows in _blocks(section):
            lines.append(f"  {value} ({len(rows)})")
            lines += [f"    {row['export_id']}" for row in rows]
    return lines


def _blocks(section: dict[str, Any]) -> list[tuple[str, list]]:
    if "groups" in section:
        return [(str(group["value"]), group["rows"]) for group in section["groups"]]
    return [("rows", section["rows"])]
