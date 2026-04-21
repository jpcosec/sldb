import re
from typing import List, Dict, Tuple, Any
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

class AST_Handler:
    """
    Handles parsing markdown strictly into High-Level block nodes to preserve 
    structural boundary logic, rather than blindly flattening the entire tree.
    """
    def __init__(self):
        from mdit_py_plugins.front_matter import front_matter_plugin
        self.md = MarkdownIt("gfm-like").enable("table").use(front_matter_plugin)
        
    def split_nodes(self, raw_markdown: str) -> List[SyntaxTreeNode]:
        """
        Breaks the parsed AST root exclusively into its top-level block children
        (e.g., [Paragraph_1, Heading_1, Paragraph_2, List_1]).
        """
        tokens = self.md.parse(raw_markdown)
        root = SyntaxTreeNode(tokens)
        return root.children
