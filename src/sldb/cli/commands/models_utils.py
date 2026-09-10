from __future__ import annotations

import ast
import importlib.util
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Any

from sldb.cli.store_context import get_store_context
from sldb.cli.utils import parse_data_value
from sldb.core.exceptions import SLDBModelDraftError, SLDBModelEditError, SLDBModelError
from sldb.runtime.validation import Validator
from sldb.store.io import load_store_index

def registered_model_source(args: Any) -> tuple[Path, str, str]:
    sp, root = get_store_context(args.store)
    idx = load_store_index(sp)
    m_entry = next((m for m in idx.models if m.name == args.model), None)
    if not m_entry:
        raise SLDBModelError(f"Model '{args.model}' not found.")
    model_path = Path(m_entry.path)
    if not model_path.is_absolute():
        model_path = root / model_path
    mod, attr = m_entry.model_ref.split(":", 1)
    return model_path.resolve(), mod, attr

def draft_path(path: Path) -> Path:
    return path.with_name(path.name + ".temp")

def load_model_from_path(path: Path, module_name: str, attr_path: str, pythonpath: str | None) -> Any:
    setup_sys_path(pythonpath)
    loader = SourceFileLoader(f"{module_name}__draft__", str(path))
    spec = importlib.util.spec_from_loader(f"{module_name}__draft__", loader)
    if spec is None or spec.loader is None:
        raise SLDBModelDraftError(f"Could not load model draft from {path}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return extract_attr(module, attr_path)

def setup_sys_path(pythonpath: str | None) -> None:
    search_paths = [str(Path.cwd().resolve())]
    if pythonpath:
        search_paths.insert(0, str(Path(pythonpath).resolve()))
    for candidate in reversed(search_paths):
        if candidate not in sys.path:
            sys.path.insert(0, candidate)

def extract_attr(obj: Any, attr_path: str) -> Any:
    for attr in attr_path.split("."):
        obj = getattr(obj, attr)
    return obj

def tracked_docs_for_model(args: Any) -> list[tuple[str, str]]:
    from sldb.store.facade import get_tracked_docs
    sp, root = get_store_context(args.store)
    return get_tracked_docs(args.model, sp, root)

def find_class_node(tree: ast.AST, class_name: str, path: Path) -> ast.ClassDef:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    raise SLDBModelEditError(f"Class '{class_name}' not found in {path}.")

def remove_node_block(source: str, node: ast.AST) -> str:
    lines = source.splitlines(keepends=True)
    start_line = node.lineno - 1
    end_line = node.end_lineno
    del lines[start_line:end_line]
    return "".join(lines)

def replace_rhs_expression(source: str, node: ast.AST, replacement: str) -> str:
    # ast col_offset/end_col_offset son offsets en BYTES utf-8; las líneas se
    # parten por bytes para que el corte no se corra con caracteres multibyte.
    lines = source.splitlines(keepends=True)
    s_line, e_line = node.lineno - 1, node.end_lineno - 1
    s_col, e_col = node.col_offset, node.end_col_offset
    if s_line == e_line:
        raw = lines[s_line].encode('utf-8')
        lines[s_line] = (raw[:s_col] + replacement.encode('utf-8') + raw[e_col:]).decode('utf-8')
    else:
        s_raw, e_raw = lines[s_line].encode('utf-8'), lines[e_line].encode('utf-8')
        lines[s_line : e_line + 1] = [(s_raw[:s_col] + replacement.encode('utf-8') + e_raw[e_col:]).decode('utf-8')]
    return "".join(lines)
