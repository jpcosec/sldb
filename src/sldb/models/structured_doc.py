from __future__ import annotations
import os
from importlib import import_module
from pathlib import Path
from typing import Any, TypeVar
from pydantic import BaseModel, model_validator
from sldb.models.doc_anchor_value import check_anchor_fields

class StructuredNLDoc(BaseModel):
    __authority__: str = "generated"
    __semantics__: dict[str, Any] = {"representation": ["markdown"], "source": ["document", "markdown"]}
    __template__: str = ""
    __compositions__: dict[str, dict[str, Any]] = {}
    __containment__: dict[str, list[str]] = {}
    __references__: list[str] = []
    __doc_anchors__: list[str] = []

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)
        if cls is StructuredNLDoc: return
        missing = sorted(n for n, i in cls.model_fields.items() if not i.description or not i.description.strip())
        if missing: raise TypeError(f"{cls.__name__} fields must define a non-empty description: {', '.join(missing)}")

    @model_validator(mode="after")
    def _doc_anchor_forms(self): return check_anchor_fields(self)

    def render_payload(self, recorder: Any = None, ref_root: Path | None = None, field_resolver: Any = None) -> dict[str, Any]:
        payload = self.model_dump(mode="json")
        for name in self.__compositions__:
            payload[name] = self.compose_field(name, recorder=recorder, ref_root=ref_root, field_resolver=field_resolver)
        return payload

    def compose_field(self, name: str, recorder: Any = None, ref_root: Path | None = None, field_resolver: Any = None) -> str:
        """The composed field's text. `ref_root` resolves relative refs; the CWD is the fallback."""
        spec = self.__compositions__.get(name, {})
        refs = getattr(self, spec.get("source_field") or "", []) or []
        if not spec.get("source_field") or not isinstance(refs, list): return ""
        if spec.get("ref") == "field":
            return self._compose_by_field(refs, spec, recorder, field_resolver)
        return self._compose_by_doc(refs, spec, recorder, ref_root)

    def _compose_by_field(self, refs: list[Any], spec: dict[str, Any], rec: Any, res: Any) -> str:
        if res is None: return ""
        rendered = [t for i, r in enumerate(refs) if (t := self._render_field_ref(r, i, spec, rec, res))]
        return spec.get("separator", "\n").join(rendered)

    def _render_field_ref(self, raw_ref: Any, idx: int, spec: dict[str, Any], rec: Any, res: Any) -> str:
        ref_str = str(raw_ref).strip()
        try: resolved = res.resolve(ref_str)
        except Exception: return ""
        if (val := resolved.get("value")) is None: return ""
        text = _format_field_val(val, resolved.get("payload") or {}, spec.get("template", "{value}"))
        return _wrap_field_piece(rec, text, resolved, idx, ref_str) if rec is not None else text

    def _compose_by_doc(self, refs: list[Any], spec: dict[str, Any], rec: Any, ref_root: Path | None) -> str:
        if (model_type := self._resolve_composition_model(spec.get("model"))) is None: return ""
        rendered = [t for i, r in enumerate(refs) if (t := self._render_doc_ref(r, i, spec, model_type, rec, ref_root))]
        return spec.get("separator", "\n").join(rendered)

    def _render_doc_ref(self, raw: Any, idx: int, spec: dict[str, Any], m_type: type, rec: Any, root: Path | None) -> str:
        if not (p := self._payload_for_ref(raw, m_type, root)): return ""
        try: text = spec.get("template", "- {title}").format(**p)
        except Exception: return ""
        return _wrap_doc_piece(rec, text, m_type.__name__, idx, str(raw).strip()) if rec else text

    def _payload_for_ref(self, raw: Any, m_type: type, root: Path | None) -> dict[str, Any] | None:
        # the read guard of sldb.store.source_read, inline: models (layer 0) does not import the store
        if not (path := self._resolve_ref(raw, root)).exists() or path.is_symlink() or (root is not None and not path.resolve().is_relative_to(root.resolve())): return None
        try: return self._extract_composed_payload(m_type, path)
        except Exception: return None

    @staticmethod
    def _resolve_ref(raw_ref: Any, ref_root: Path | None) -> Path:
        ref = Path(str(raw_ref).strip().strip("`"))
        return ref if ref_root is None or ref.is_absolute() else ref_root / ref

    def _resolve_composition_model(self, value: Any):
        if value is None or isinstance(value, type): return value
        if isinstance(value, str) and ":" in value:
            mod_name, _, attr_name = value.partition(":")
            obj: Any = import_module(mod_name)
            for attr in attr_name.split("."): obj = getattr(obj, attr)
            return obj
        return None

    def _extract_composed_payload(self, model_type: type[StructuredNLDoc], path: Path) -> dict[str, Any]:
        from sldb.runtime.validation import extract_model_data
        with open(os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)), encoding="utf-8") as f:
            return extract_model_data(model_type, f.read())


def _format_field_val(val: Any, payload: dict[str, Any], template: str) -> str:
    try: return template.format(**{"value": val, "val": val, **payload})
    except Exception: return str(val)


def _wrap_field_piece(recorder: Any, text: str, res: dict[str, Any], idx: int, ref_str: str) -> str:
    source = {"doc": res.get("doc"), "path": res.get("path") or ref_str, "model": res.get("model"), "field": res.get("field")}
    return recorder.wrap(text, {"piece": True, "source": source, "ref_index": idx, "ref": ref_str})


def _wrap_doc_piece(recorder: Any, text: str, model_name: str, idx: int, ref_str: str) -> str:
    source = {"doc": None, "path": ref_str.strip("`"), "model": model_name, "field": None}
    return recorder.wrap(text, {"piece": True, "source": source, "ref_index": idx, "ref": ref_str})

M = TypeVar("M", bound="StructuredNLDoc")
