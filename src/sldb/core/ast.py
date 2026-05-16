from abc import ABC, abstractmethod
from typing import List

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

from sldb.core.node import SLDBNode


class BaseASTHandler(ABC):
    """
    Abstract base class for parsing content into a unified SLDBNode tree.
    """

    @abstractmethod
    def split_nodes(self, raw_content: str) -> List[SLDBNode]:
        pass


class MarkdownASTHandler(BaseASTHandler):
    """
    Handles parsing markdown strictly into high-level SLDBNode block nodes.
    """

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
            _raw=node,
        )


# Legacy alias for backward compatibility within the core library
AST_Handler = MarkdownASTHandler
