import json
from typing import Any
from sldb.cli.dict_utils import deep_delete, deep_set, ensure_list
from sldb.cli.utils import parse_data_value
from sldb.cli.commands.fields_target import resolve_doc_target
from sldb.cli.commands.fields_save import save_payload

def mutate_field(args: Any, mode: str) -> int:
    runtime_doc, field_path = resolve_doc_target(args.target, args.store, args.pythonpath)
    payload = json.loads(json.dumps(runtime_doc.payload))
    _apply_mutation(payload, field_path, args, mode)
    return save_payload(runtime_doc, payload, args.store, args.pythonpath, getattr(args, "format", "text"), f"{mode}:{field_path}")

def _value(args: Any) -> Any:
    return args.value if getattr(args, "string", False) else parse_data_value(args.value)

def _apply_mutation(payload: dict[str, Any], field_path: str, args: Any, mode: str) -> None:
    if mode == "create": deep_set(payload, field_path, _value(args), create=True)
    elif mode == "update": deep_set(payload, field_path, _value(args), create=False)
    elif mode == "remove": deep_delete(payload, field_path)
    elif mode == "append": ensure_list(payload, field_path).append(_value(args))
    elif mode == "clean": _apply_clean(payload, field_path, args)

def _apply_clean(payload: dict[str, Any], field_path: str, args: Any) -> None:
    field_values = ensure_list(payload, field_path)
    cleaned = _clean_list(field_values, args.drop_empty, args.dedupe)
    deep_set(payload, field_path, cleaned, create=False)

def _clean_list(items: list[Any], drop_empty: bool, dedupe: bool) -> list[Any]:
    cleaned, seen = [], set()
    for item in items:
        if drop_empty and item in (None, "", [], {}): continue
        marker = json.dumps(item, sort_keys=True, ensure_ascii=True)
        if dedupe and marker in seen: continue
        seen.add(marker)
        cleaned.append(item)
    return cleaned
