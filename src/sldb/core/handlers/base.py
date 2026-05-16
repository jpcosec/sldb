from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from sldb.core.node import SLDBNode


class BaseNodeHandler(ABC):
    """
    Base class for all node handlers.
    """

    def __init__(self, router=None):
        self.router = router

    def get_text(self, node: SLDBNode) -> str:
        """
        Retrieves the text content of a node, preferring raw content to preserve markup.
        """
        # If the node has explicit content (like inline or text), use it.
        # This preserves Markdown markup (e.g. __bold__) in inline nodes.
        if node.content:
            return node.content

        if node.type == "softbreak":
            return "\n"

        if node.children:
            return "".join(self.get_text(child) for child in node.children)

        return ""

    @abstractmethod
    def compile_recipe(self, node: SLDBNode) -> list[dict[str, Any]]:
        """Compiles a list of extraction recipes for the given node."""
        pass

    @abstractmethod
    def extract_data(self, node: SLDBNode, recipe: dict[str, Any]) -> Any:
        """Extracts data from the node using the provided recipe."""
        pass
