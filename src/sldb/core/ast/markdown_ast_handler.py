from typing import List
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from sldb.core.node import SLDBNode
from .base_ast_handler import BaseASTHandler

class MarkdownASTHandler(BaseASTHandler):
    """Handles parsing markdown strictly into high-level SLDBNode block nodes."""
    def __init__(self):
        from mdit_py_plugins.front_matter import front_matter_plugin
        self.md = MarkdownIt("gfm-like").enable("table").use(front_matter_plugin)

    def split_nodes(self, raw_markdown: str) -> List[SLDBNode]:
        tokens = self.md.parse(raw_markdown)
        root = SyntaxTreeNode(tokens)
        return [self._convert(child) for child in root.children]

    def _convert(self, node: SyntaxTreeNode) -> SLDBNode:
        return SLDBNode(
            type=node.type,
            tag=node.tag,
            content=node.content,
            map=list(node.map) if node.map else None,
            children=[self._convert(c) for c in node.children],
            metadata=_token_metadata(node),
            _raw=node,
        )


def _token_metadata(node: SyntaxTreeNode) -> dict:
    """What the token carries beyond its text: a fence's language (`info`), the markup that
    opened it (`markup`: ``` or ~~~, `-` or `*`) and its attributes; only what is present."""
    token = node.token or node.nester_tokens.opening if not node.is_root else None
    found = {"info": getattr(token, "info", ""), "markup": getattr(token, "markup", ""), "attrs": dict(getattr(token, "attrs", None) or {})}
    return {key: value for key, value in found.items() if value}

