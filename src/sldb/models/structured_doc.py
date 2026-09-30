from __future__ import annotations
from importlib import import_module
from pathlib import Path
from typing import Any, TypeVar
from pydantic import BaseModel, PrivateAttr

class StructuredNLDoc(BaseModel):
    # Every tracked record is rendered as Markdown, but its subject can come from another
    # adapter. Subclasses override source when they describe code, data, or another
    # non-Markdown source format. Store semantic indexes expose both dimensions.
    __semantics__: dict[str, Any] = {
        "representation": ["markdown"],
        "source": ["document", "markdown"],
    }
    __template__: str = ""
    __compositions__: dict[str, dict[str, Any]] = {}
    # Project root that anchors relative child paths in __compositions__ when the
    # renderer runs from a different cwd (a server, the CLI, the store). When unset,
    # relative child paths keep the historic process-cwd behavior. Subclasses may
    # declare this declaratively; rendering orchestration may set _composition_root
    # on the instance instead, which takes precedence.
    __composition_root__: Path | None = None
    _composition_root: Path | None = PrivateAttr(default=None)
    # Per-render diagnostics for children that could not be composed. Rendered
    # markdown stays unchanged; broken children are reported here instead of being
    # silently indistinguishable from "no children".
    _composition_issues: list[str] = PrivateAttr(default_factory=list)
    # Declarative graph metadata: which fields hold document ids.
    # __containment__ maps field -> allowed target models (visual containment).
    # __references__ lists fields holding doc ids that are not containment.
    __containment__: dict[str, list[str]] = {}
    __references__: list[str] = []

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)
        if cls is StructuredNLDoc: return
        missing_descriptions = sorted(name for name, info in cls.model_fields.items() if not info.description or not info.description.strip())
        if missing_descriptions: raise TypeError(f"{cls.__name__} fields must define a non-empty description: {', '.join(missing_descriptions)}")

    def render_payload(self) -> dict[str, Any]:
        payload = self.model_dump(mode="json")
        for name in self.__compositions__: payload[name] = self.compose_field(name)
        return payload

    @property
    def composition_issues(self) -> list[str]:
        """Broken children from the latest compose_field runs: missing paths,
        invalid/empty child payloads, and template-format errors."""
        return list(self._composition_issues)

    def compose_field(self, name: str) -> str:
        spec = self.__compositions__.get(name, {})
        refs = getattr(self, spec.get("source_field") or "", []) or []
        model_type = self._resolve_composition_model(spec.get("model"))
        if not spec.get("source_field") or not isinstance(refs, list) or model_type is None: return ""
        root = self._composition_root or self.__composition_root__
        def _render(raw_ref): return self._compose_child(name, spec, model_type, raw_ref, root)
        return spec.get("separator", "\n").join(filter(None, map(_render, refs)))

    def _issue(self, name: str, message: str) -> str:
        self._composition_issues.append(f"compose_field[{name}]: {message}")
        return ""

    def _compose_child(self, name: str, spec: dict[str, Any], model_type: type[StructuredNLDoc], raw_ref: Any, root: Path | None) -> str:
        ref = str(raw_ref).strip().strip("`")
        path = Path(ref)
        if not path.is_absolute() and root is not None: path = Path(root) / path
        if not path.exists(): return self._issue(name, f"missing child {ref!r} ({path})")
        try: payload = self._extract_composed_payload(model_type, path)
        except Exception as exc: return self._issue(name, f"invalid child payload {ref!r} ({path}): {exc}")
        if not payload: return self._issue(name, f"empty child payload {ref!r} ({path})")
        try: return spec.get("template", "- {title}").format(**payload)
        except Exception as exc: return self._issue(name, f"template error for child {ref!r}: {exc}")

    def _resolve_composition_model(self, value: Any):
        if value is None or isinstance(value, type): return value
        if isinstance(value, str) and ":" in value:
            obj: Any = import_module(value.split(":", 1)[0])
            for attr in value.split(":", 1)[1].split("."): obj = getattr(obj, attr)
            return obj
        return None

    def _extract_composed_payload(self, model_type: type[StructuredNLDoc], path: Path) -> dict[str, Any]:
        from sldb.runtime.validation import extract_model_data
        return extract_model_data(model_type, path.read_text(encoding="utf-8"))

M = TypeVar("M", bound="StructuredNLDoc")
