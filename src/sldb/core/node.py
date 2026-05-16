from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class SLDBNode:
    """
    A unified node structure that abstracts away the specific AST library.
    """

    type: str
    tag: str = ""
    content: str = ""
    children: List[SLDBNode] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    # line mapping [start, end]
    map: Optional[List[int]] = None

    # Optional reference to the original library-specific node
    _raw: Any = None

    def find_leaf_text(self) -> str:
        """Helper to find the first leaf node with content."""
        if self.content:
            return self.content
        for child in self.children:
            text = child.find_leaf_text()
            if text:
                return text
        return ""
