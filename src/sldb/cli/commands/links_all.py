"""`sldb docs recover --all/--glob`: audit the links of many documents in one go."""
from __future__ import annotations
import glob
import json
from pathlib import Path
from typing import Any
import yaml
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBError
from sldb.links.audit import audit_links
from sldb.links.tracked import tracked_documents

def batch_requested(args: Any) -> bool:
    return bool(getattr(args, "all", False) or getattr(args, "glob", None) or not args.doc)

def select_documents(args: Any, sp: Path, root: Path) -> list[tuple[str, Path]]:
    docs = tracked_documents(sp, root) if args.all else []
    docs += [(p, Path(p).resolve()) for p in sorted(glob.glob(args.glob or "", recursive=True)) if Path(p).is_file()]
    return list({path: (name, path) for name, path in docs}.values())

def _line(p: dict) -> str:
    if p["kind"] == "unresolved": return f"{p['doc']}: [[{p['target']}]] no resuelve"
    return f"{p['doc']}: predicado '{p['predicate']}' no está en el store (CUSTOM) -> {p['target']}"

def _print(fmt: str, docs: int, problems: list[dict]) -> None:
    data = {"documents": docs, "problems": problems}
    if fmt == "json": print(json.dumps(data, indent=2))
    elif fmt == "yaml": print(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
    else: print("\n".join([*map(_line, problems), f"{docs} documentos revisados, {len(problems)} problemas"]))

def recover_all(args: Any) -> int:
    if not (args.all or args.glob): raise SLDBError("docs recover needs a doc, --all or --glob.")
    sp, root = get_store_context(args.store)
    docs = select_documents(args, sp, root)
    problems = audit_links(sp, docs)
    _print(args.format, len(docs), problems)
    bad = [p for p in problems if p["kind"] == "unresolved" or args.fail_on_custom]
    return 1 if bad else 0
