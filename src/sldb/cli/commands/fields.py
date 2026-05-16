from __future__ import annotations

import json
from typing import Any

import yaml

from sldb.cli.graph import query_field_records
from sldb.cli.utils import (
    deep_delete,
    deep_get,
    deep_set,
    ensure_list,
    get_store_context,
    parse_data_value,
    registered_model,
    resolve_model_ref,
)
from sldb.runtime.validation import (
    render_model_markdown,
    validate_model_input_roundtrip,
)
from sldb.store.hashing import hash_fields, hash_text
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_store_index,
    save_documents_index,
    save_models_index,
    store_lock,
)
from sldb.store.ops import cascade_hash_a
from sldb.store.query import load_runtime_documents
from sldb.store.semantic import rebuild_semantic_indexes


class FieldsCLI:
    """Field CRUD and query surface."""

    def run(self, args: Any) -> int:
        command = args.fields_command
        if command == "show":
            return self.show(args)
        if command == "query":
            return self.query(args)
        if command in {"create", "update", "remove", "append", "clean"}:
            return getattr(self, command)(args)
        raise SystemExit(f"Unknown fields command: {command}")

    def show(self, args: Any) -> int:
        target = args.target.strip("/")
        if target.startswith("models/"):
            model_name, field_path = self._parse_model_target(target)
            model_type, _entry, _idx = registered_model(
                get_store_context(args.store)[0], model_name, args.pythonpath
            )
            if field_path is None:
                payload = {
                    "model": model_name,
                    "fields": [
                        {
                            "name": name,
                            "description": field.description or "",
                            "annotation": getattr(
                                field.annotation, "__name__", repr(field.annotation)
                            ),
                        }
                        for name, field in model_type.model_fields.items()  # type: ignore[attr-defined]
                    ],
                }
            else:
                field = model_type.model_fields[field_path]  # type: ignore[attr-defined]
                payload = {
                    "model": model_name,
                    "field": field_path,
                    "description": field.description or "",
                    "annotation": getattr(
                        field.annotation, "__name__", repr(field.annotation)
                    ),
                }
            print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
            return 0

        runtime_doc, field_path = self._resolve_doc_target(
            args.target, args.store, args.pythonpath
        )
        value = deep_get(runtime_doc.payload, field_path)
        if args.format == "yaml":
            print(yaml.safe_dump({"value": value}, sort_keys=False, allow_unicode=True))
        else:
            print(json.dumps({"value": value}, indent=2))
        return 0

    def query(self, args: Any) -> int:
        rows = query_field_records(
            args.store,
            args.pythonpath,
            args.field,
            include_linked=args.global_scope,
        )
        if args.format == "yaml":
            print(
                yaml.safe_dump({"results": rows}, sort_keys=False, allow_unicode=True)
            )
        else:
            print(json.dumps({"results": rows}, indent=2))
        return 0 if rows else 1

    def create(self, args: Any) -> int:
        return self._mutate(args, mode="create")

    def update(self, args: Any) -> int:
        return self._mutate(args, mode="update")

    def remove(self, args: Any) -> int:
        return self._mutate(args, mode="remove")

    def append(self, args: Any) -> int:
        return self._mutate(args, mode="append")

    def clean(self, args: Any) -> int:
        return self._mutate(args, mode="clean")

    def _mutate(self, args: Any, mode: str) -> int:
        runtime_doc, field_path = self._resolve_doc_target(
            args.target, args.store, args.pythonpath
        )
        payload = json.loads(json.dumps(runtime_doc.payload))

        if mode == "create":
            deep_set(payload, field_path, parse_data_value(args.value), create=True)
        elif mode == "update":
            deep_set(payload, field_path, parse_data_value(args.value), create=False)
        elif mode == "remove":
            deep_delete(payload, field_path)
        elif mode == "append":
            ensure_list(payload, field_path).append(parse_data_value(args.value))
        elif mode == "clean":
            field_values = ensure_list(payload, field_path)
            cleaned = []
            seen = set()
            for item in field_values:
                if args.drop_empty and item in (None, "", [], {}):
                    continue
                marker = json.dumps(item, sort_keys=True, ensure_ascii=True)
                if args.dedupe and marker in seen:
                    continue
                seen.add(marker)
                cleaned.append(item)
            deep_set(payload, field_path, cleaned, create=False)

        return self._save_payload(runtime_doc, payload, args.store, args.pythonpath)

    def _save_payload(
        self,
        runtime_doc: Any,
        payload: dict[str, Any],
        store_arg: str | None,
        pythonpath: str | None,
    ) -> int:
        sp, root = get_store_context(store_arg)
        idx = load_store_index(sp)
        m_entry = next(
            (m for m in idx.models if m.name == runtime_doc.model_name), None
        )
        if m_entry is None:
            raise SystemExit(f"Model '{runtime_doc.model_name}' not registered.")
        m_idx = load_models_index(root / m_entry.models_index)
        d_idx = load_documents_index(root / m_idx.documents_index)
        doc_entry = next(
            (d for d in d_idx.documents if d.name == runtime_doc.name), None
        )
        if doc_entry is None:
            raise SystemExit(f"Doc '{runtime_doc.name}' not registered.")

        model_type = resolve_model_ref(m_entry.model_ref, pythonpath)
        rendered = render_model_markdown(model_type, payload)
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            raise SystemExit(f"Field mutation broke idempotency: {details}")

        doc_path = root / doc_entry.path
        doc_path.write_text(rendered + "\n", encoding="utf-8")
        doc_entry.hash_c = hash_text(rendered + "\n")
        doc_entry.hash_d = hash_fields(model_type, rendered + "\n")
        with store_lock(sp):
            save_documents_index(root / m_idx.documents_index, d_idx)
            save_models_index(root / m_entry.models_index, m_idx)
            rebuild_semantic_indexes(sp, root, resolve_model_ref, pythonpath)
            cascade_hash_a(sp, root, idx)
        print(f"Updated field payload for '{runtime_doc.name}'")
        return 0

    def _resolve_doc_target(
        self, target: str, store_arg: str | None, pythonpath: str | None
    ) -> tuple[Any, str]:
        normalized = target.strip("/")
        if not normalized.startswith("docs/"):
            raise SystemExit("Field targets must start with 'docs/'.")
        tail = normalized.removeprefix("docs/")
        parts = tail.split("/")
        if len(parts) < 2:
            raise SystemExit(
                "Expected docs/<doc>/<field> or docs/<model>/<doc>/<field>."
            )

        store_path, _root = get_store_context(store_arg)
        docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
        candidates = []
        for doc in docs:
            one = f"{doc.name}/"
            two = f"{doc.model_name}/{doc.name}/"
            joined = "/".join(parts)
            if joined.startswith(two):
                candidates.append((doc, joined[len(two) :]))
            elif joined.startswith(one):
                candidates.append((doc, joined[len(one) :]))
        if not candidates:
            raise SystemExit(f"Unknown docs field target: {target}")
        if len(candidates) > 1:
            exact = [item for item in candidates if item[1]]
            candidates = exact or candidates
        if len(candidates) != 1:
            raise SystemExit(f"Ambiguous docs field target: {target}")
        runtime_doc, field_path = candidates[0]
        if not field_path:
            raise SystemExit("Missing field path after document target.")
        return runtime_doc, field_path.replace("/", ".")

    @staticmethod
    def _parse_model_target(target: str) -> tuple[str, str | None]:
        parts = target.removeprefix("models/").split("/", 1)
        return parts[0], parts[1].replace("/", ".") if len(parts) > 1 else None
