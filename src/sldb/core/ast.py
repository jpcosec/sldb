from typing import List

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode


class AST_Handler:
    """
    Handles parsing markdown strictly into high-level block nodes.
    """

    def __init__(self):
        from mdit_py_plugins.front_matter import front_matter_plugin

        self.md = MarkdownIt("gfm-like").enable("table").use(front_matter_plugin)

    def split_nodes(self, raw_markdown: str) -> List[SyntaxTreeNode]:
        tokens = self.md.parse(raw_markdown)
        root = SyntaxTreeNode(tokens)
        return root.children
