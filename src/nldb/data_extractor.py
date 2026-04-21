import re
from typing import List, Dict, Any
from markdown_it.tree import SyntaxTreeNode
from nldb.node_handler import SharedNodeHandler

class DataExtractor:
    """
    Applies compiled template recipes to a parsed Markdown Data Document 
    to robustly recover the payload values using sequential block cursor.
    """
    def __init__(self):
        self.node_handler = SharedNodeHandler()
        
    def extract_values(self, data_blocks: List[SyntaxTreeNode], recipes: List[Dict[str, Any]]) -> Dict[str, Any]:
        extracted_data = {}
        search_index = 0  
        last_outer_index = -1
        current_block_idx = -1

        for recipe in recipes:
            target_type = recipe["outer_type"]
            target_tag = recipe.get("outer_tag", "")
            handler_key = recipe.get("handler", "text")
            recipe_outer_idx = recipe["outer_index"]
            
            if recipe_outer_idx != last_outer_index:
                search_index = max(search_index, current_block_idx + 1)
                last_outer_index = recipe_outer_idx
                current_block_idx = -1 

            for block_idx in range(search_index, len(data_blocks)):
                if current_block_idx != -1 and block_idx != current_block_idx:
                    break

                block = data_blocks[block_idx]
                if getattr(block, "type", "") != target_type: continue
                
                is_anchor = recipe.get("anchor", False)
                if not is_anchor and getattr(block, "tag", "") != target_tag: continue
                    
                current_node = block
                if handler_key == "text":
                    def find_leaf(node):
                        if getattr(node, "type", "") == "text": return node
                        if getattr(node, "content", None): return node
                        for c in getattr(node, "children", []):
                            res = find_leaf(c)
                            if res: return res
                        return None
                    current_node = find_leaf(block)
                
                if not current_node: continue
    
                values = self.node_handler.handlers[handler_key].extract_data(current_node, recipe)
                
                if is_anchor:
                    current_block_idx = block_idx
                    break
                elif values:
                    extracted_data.update(values)
                    current_block_idx = block_idx
                    break
                    
        return extracted_data
