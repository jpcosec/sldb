from __future__ import annotations


from sldb.core.handlers.list import ListNodeHandler
from sldb.core.handlers.table import TableNodeHandler
from sldb.core.handlers.text import TextNodeHandler
from sldb.core.handlers.yaml import YamlNodeHandler
from sldb.core.node import SLDBNode


class SharedNodeHandler:
    """
    Router for dispatching nodes to their appropriate handlers.
    """

    def __init__(self):
        self.handlers = {
            "text": TextNodeHandler(self),
            "bullet_list": ListNodeHandler(self),
            "ordered_list": ListNodeHandler(self),
            "list": ListNodeHandler(self),
            "table": TableNodeHandler(self),
            "fence": YamlNodeHandler(self),
            "front_matter": YamlNodeHandler(self),
            "yaml": YamlNodeHandler(self),
        }

    def get_handler_for_node(self, node: SLDBNode) -> str | None:
        """Determines which handler should process the node."""
        if node.type in self.handlers:
            return node.type
        return "text"
