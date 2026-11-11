"""`sldb tags namespaces|tree|check`: thin printing wrappers over `sldb.api.tags`.

`check` reports its findings exactly as `sldb rules check` does (`{"findings": [...]}` in JSON,
one line each in text, the tally at the end) and exits 1 only when one is an error.
"""

from __future__ import annotations

from typing import Any

from sldb.api.tags import tag_check, tag_namespaces, tag_tree
from sldb.cli import alert_sink
from sldb.cli.output_format import emit
from sldb.core.exceptions import SLDBError


class TagsCLI:
    """The tag namespaces of a store through the CLI."""

    def run(self, args: Any) -> int:
        commands = {"namespaces": self.namespaces, "tree": self.tree, "check": self.check}
        if args.tags_command not in commands:
            raise SLDBError(f"Unknown command: {args.tags_command}")
        return commands[args.tags_command](args)

    def namespaces(self, args: Any) -> int:
        found = tag_namespaces(args.store)
        emit({"namespaces": found}, args.format, "\n".join(_namespace_line(n) for n in found) or "No tag namespaces declared")
        return 0

    def tree(self, args: Any) -> int:
        tree = tag_tree(args.store, args.namespace)
        lines = [line for root in tree["roots"] for line in _tree_lines(root, 0)]
        lines += [f"orphan: {o['tag']} used by {', '.join(o['used_by'])}" for o in tree["orphans"]]
        lines += [f"unplaced: {u['tag']} ({u['document']})" for u in tree["unplaced"]]
        emit(tree, args.format, "\n".join(lines) or f"No tags in namespace {tree['namespace']}")
        return 0

    def check(self, args: Any) -> int:
        findings = tag_check(args.store)
        text = args.format == "text"
        if not text:
            emit({"findings": [f.as_dict() for f in findings]}, args.format, "")
        alert_sink.report(findings, text=text)
        if text:
            print(f"tags check: {alert_sink.tally(findings) or 'sin hallazgos'}")
        return 1 if any(f.level == "error" for f in findings) else 0


def _namespace_line(namespace: dict[str, Any]) -> str:
    anchored = namespace.get("anchored_by")
    flags = [k for k in ("hierarchical", "folder_axis") if namespace.get(k)]
    return f"{namespace['name']}: {', '.join(flags) or 'flat'}" + (f"; anchored by {anchored['model']}.{anchored['field']}" + (" (bare)" if anchored.get("value") == "bare" else "") if anchored else "")


def _tree_lines(node: dict[str, Any], depth: int) -> list[str]:
    line = "  " * depth + node["tag"] + (f" ({node['document']})" if node["document"] else "")
    return [line] + [l for child in node["children"] for l in _tree_lines(child, depth + 1)]
