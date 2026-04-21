import re
from typing import List, Dict, Tuple, Any
from markdown_it.tree import SyntaxTreeNode
from sldb.node_handler import SharedNodeHandler

class TemplateExtractor:
    """
    Extracts deterministic search recipes from the Template's block nodes. 
    It identifies exactly where markers live inside the block using SharedNodeHandler.
    """
    def __init__(self):
        self.node_handler = SharedNodeHandler()
        
    def extract_nodes(self, block_nodes: List[SyntaxTreeNode]) -> List[Dict[str, Any]]:
        extracted_recipes = []
        
        for outer_index, block_node in enumerate(block_nodes):
            outer_type = getattr(block_node, "type", "")
            found_recipe_in_block = False
            
            def dive(node: SyntaxTreeNode, current_path: List[int]):
                nonlocal found_recipe_in_block
                # 1. Does this node trigger a special container handler? (e.g. Table)
                handler_key = self.node_handler.get_handler_for_node(node)
                
                if handler_key and handler_key != "text":
                    # Let the specialized handler digest this container completely!
                    handler_recipes = self.node_handler.handlers[handler_key].compile_recipe(node)
                    if handler_recipes:
                        for r in handler_recipes:
                            r.update({
                                "outer_index": outer_index, 
                                "outer_type": outer_type,
                                "outer_tag": getattr(block_node, "tag", ""),
                                "inner_path": current_path
                            })
                            extracted_recipes.append(r)
                            found_recipe_in_block = True
                        return # DO NOT dive deeper into this specialized block naturally
                    
                # 2. Otherwise apply literal leaf mapping if it's terminal
                if handler_key == "text" or not getattr(node, "children", []):
                    literal_recipes = self.node_handler.handlers["text"].compile_recipe(node)
                    if literal_recipes:
                        for r in literal_recipes:
                            r.update({
                                "outer_index": outer_index, 
                                "outer_type": outer_type,
                                "outer_tag": getattr(block_node, "tag", ""),
                                "inner_path": current_path
                            })
                            extracted_recipes.append(r)
                            found_recipe_in_block = True
                        
                # Always try to dive unless it was a specialized container that matched
                for child_idx, child in enumerate(node.children):
                    dive(child, current_path + [child_idx])
                    
            dive(block_node, [])
            # If no marker was found in this block, add it as an anchor
            if not found_recipe_in_block:
                content = self.node_handler.handlers["text"].get_text(block_node).strip()
                # Even if content is empty (like an hr), we want an anchor to maintain sequence
                extracted_recipes.append({
                    "outer_index": outer_index,
                    "outer_type": outer_type,
                    "outer_tag": getattr(block_node, "tag", ""),
                    "inner_path": [],
                    "props": [],
                    "regex": f"^{re.escape(content)}$" if content else "^$",
                    "handler": "text",
                    "anchor": True
                })
            
        return extracted_recipes
