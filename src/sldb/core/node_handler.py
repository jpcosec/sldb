import re
from abc import ABC, abstractmethod
from typing import Any

from markdown_it.tree import SyntaxTreeNode

MARKER_PATTERN = r"⸢([^⸥]+)⸥"
INLINE_RENDER_PATTERN = r"{{\s*.*?\s*}}"


def parse_marker(inner: str) -> dict[str, Any]:
    head, _, prop = inner.partition("•")
    parts = [part.strip() for part in head.split(",") if part.strip()]
    kind = parts[0] if parts else "rev"
    traits = parts[1:] if parts else []
    name = prop.strip() if prop else ""
    return {"kind": kind, "traits": traits, "name": name}


def build_text_pattern(content: str) -> dict[str, Any]:
    props_info = []
    regex_parts = []
    cursor = 0
    dynamic_found = False

    token_pattern = re.compile(f"{MARKER_PATTERN}|{INLINE_RENDER_PATTERN}")
    for match in token_pattern.finditer(content):
        regex_parts.append(re.escape(content[cursor : match.start()]))
        token = match.group(0)

        if token.startswith("{{"):
            regex_parts.append(".*?")
            dynamic_found = True
        else:
            marker = parse_marker(match.group(1))
            kind = marker["kind"]
            if kind in {"rev", "optrev"}:
                regex_parts.append("(.*?)")
                props_info.append(
                    {
                        "name": marker["name"],
                        "traits": marker["traits"],
                        "kind": kind,
                    }
                )
                dynamic_found = True
            else:
                regex_parts.append(".*?")
                dynamic_found = True

        cursor = match.end()

    regex_parts.append(re.escape(content[cursor:]))
    return {
        "props_info": props_info,
        "regex": f"^{''.join(regex_parts)}$",
        "dynamic_found": dynamic_found,
    }


class BaseNodeHandler(ABC):
    def __init__(self, router=None):
        self.router = router

    def get_text(self, node: SyntaxTreeNode) -> str:
        if getattr(node, "type", "") == "text":
            return getattr(node, "content", "")
        if getattr(node, "children", []):
            return "".join(self.get_text(child) for child in node.children)
        return getattr(node, "content", "") or ""

    @abstractmethod
    def compile_recipe(self, node: SyntaxTreeNode) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def extract_data(self, node: SyntaxTreeNode, recipe: dict[str, Any]) -> Any:
        pass


class TextNodeHandler(BaseNodeHandler):
    def compile_recipe(self, node: SyntaxTreeNode) -> list[dict[str, Any]]:
        if getattr(node, "children", []):
            return []

        content = getattr(node, "content", "").strip()
        if not content or ("⸢" not in content and "{{" not in content):
            return []

        pattern_data = build_text_pattern(content)
        if not pattern_data["dynamic_found"]:
            return []

        recipe = {
            "props": [marker["name"] for marker in pattern_data["props_info"]],
            "props_info": pattern_data["props_info"],
            "regex": pattern_data["regex"],
            "handler": "text",
        }
        if not pattern_data["props_info"]:
            recipe["anchor"] = True
        return [recipe]

    def extract_data(
        self, node: SyntaxTreeNode, recipe: dict[str, Any]
    ) -> dict[str, Any]:
        content = getattr(node, "content", "").strip()
        if not content:
            return {}

        regex_pattern = re.compile(recipe["regex"])
        match = regex_pattern.match(content)
        if match:
            results = {}
            if "props_info" not in recipe:
                return {}
            for index, info in enumerate(recipe["props_info"]):
                val = match.group(index + 1).strip()
                traits = info["traits"]
                if info.get("kind") == "optrev" and val == "":
                    val = None
                if "dict" in traits or "json" in traits:
                    import yaml

                    try:
                        val = yaml.safe_load(val)
                    except Exception:
                        pass
                elif "list" in traits or (val.startswith("[") and val.endswith("]")):
                    clean_val = val.strip("`").strip()
                    if clean_val.startswith("[") and clean_val.endswith("]"):
                        import json

                        try:
                            val = json.loads(clean_val.replace("'", '"'))
                        except Exception:
                            inner = clean_val[1:-1].strip()
                            val = (
                                [item.strip() for item in inner.split("|")]
                                if inner
                                else []
                            )
                results[info["name"]] = val
            return results
        return {}


class YamlNodeHandler(BaseNodeHandler):
    def compile_recipe(self, node: SyntaxTreeNode) -> list[dict[str, Any]]:
        content = getattr(node, "content", "").strip()
        if not content or "⸢" not in content:
            return []
        match = re.search(MARKER_PATTERN, content)
        if match:
            marker = parse_marker(match.group(1))
            if marker["kind"] not in {"rev", "optrev"}:
                return [{"props": [], "handler": "yaml", "anchor": True}]
            return [
                {"props": [marker["name"]], "handler": "yaml", "kind": marker["kind"]}
            ]
        return []

    def extract_data(
        self, node: SyntaxTreeNode, recipe: dict[str, Any]
    ) -> dict[str, Any]:
        content = getattr(node, "content", "").strip()
        if not content:
            return {}
        import yaml

        try:
            data = yaml.safe_load(content)
            if recipe["props"]:
                if recipe.get("kind") == "optrev" and data is None:
                    return {recipe["props"][0]: None}
                return {recipe["props"][0]: data}
        except Exception:
            pass
        return {}


class TableNodeHandler(BaseNodeHandler):
    def compile_recipe(self, node: SyntaxTreeNode) -> list[dict[str, Any]]:
        tbody = next((child for child in node.children if child.type == "tbody"), None)
        if not tbody or not tbody.children:
            return []
        regex_map = {}
        all_props = []
        for col_idx, td in enumerate(tbody.children[0].children):
            content = self.get_text(td)
            pattern_data = build_text_pattern(content)
            if pattern_data["props_info"]:
                col_props = [info["name"] for info in pattern_data["props_info"]]
                all_props.extend(col_props)
                regex_map[col_idx] = {
                    "props": col_props,
                    "props_info": pattern_data["props_info"],
                    "regex": pattern_data["regex"],
                }
        return (
            [{"props": all_props, "regex_map": regex_map, "handler": "table"}]
            if all_props
            else []
        )

    def extract_data(
        self, node: SyntaxTreeNode, recipe: dict[str, Any]
    ) -> dict[int, dict[str, str]]:
        tbody = next((child for child in node.children if child.type == "tbody"), None)
        result_array = {}
        if not tbody:
            return result_array
        for row_index, tr in enumerate(tbody.children):
            row_data = {}
            for col_idx, td in enumerate(tr.children):
                if col_idx in recipe["regex_map"]:
                    rx_data = recipe["regex_map"][col_idx]
                    match = re.search(rx_data["regex"], self.get_text(td))
                    if match:
                        for index, info in enumerate(rx_data["props_info"]):
                            val = match.group(index + 1).strip()
                            if info.get("kind") == "optrev" and val == "":
                                val = None
                            row_data[info["name"]] = val
            if row_data:
                result_array[row_index] = row_data
        return {recipe["props"][0]: result_array}


class ListNodeHandler(BaseNodeHandler):
    def compile_recipe(self, node: SyntaxTreeNode) -> list[dict[str, Any]]:
        if not node.children:
            return []
        content = self.get_text(node.children[0])
        pattern_data = build_text_pattern(content)
        props = [info["name"] for info in pattern_data["props_info"]]
        if not props:
            return []
        return [
            {
                "props": props,
                "props_info": pattern_data["props_info"],
                "regex": pattern_data["regex"],
                "handler": "list",
            }
        ]

    def extract_data(
        self, node: SyntaxTreeNode, recipe: dict[str, Any]
    ) -> dict[str, list[str]]:
        results_array = []
        regex_pattern = re.compile(recipe["regex"])
        for li in node.children:
            content = self.get_text(li)
            item_data = {}
            match = regex_pattern.search(content)
            if match:
                for index, info in enumerate(recipe["props_info"]):
                    val = match.group(index + 1).strip()
                    if info.get("kind") == "optrev" and val == "":
                        val = None
                    item_data[info["name"]] = val
            if item_data:
                results_array.append(
                    item_data[recipe["props"][0]]
                    if len(recipe["props"]) == 1
                    else item_data
                )
        if recipe["props"]:
            return {recipe["props"][0]: results_array}
        return {}


class SharedNodeHandler:
    def __init__(self):
        self.handlers = {
            "text": TextNodeHandler(self),
            "table": TableNodeHandler(self),
            "list": ListNodeHandler(self),
            "yaml": YamlNodeHandler(self),
        }

    def get_handler_for_node(self, node: SyntaxTreeNode) -> str:
        if node.type == "table":
            return "table"
        if node.type in ["bullet_list", "ordered_list"]:
            return "list"
        if node.type in ["front_matter", "fence"]:
            return "yaml"
        if not getattr(node, "children", []):
            return "text"
        return ""
