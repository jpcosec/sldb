"""The component spec of a Python tree, from the facts of `sldb.code.scan_tree`.

Replaces spec2viz's `generate_python_ast_spec` without its own `ast` walk: the modules, their
top-level classes and their imports come from `sldb.code`, the only place that reads Python.
A node `module` per module (`__init__.py` skipped), `class` per top-level class, `defines`
from module to class, `imports` per resolved imported module (top-level and nested imports,
one edge per pair), and `external` for undeclared targets.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.notations.component_spec_findings import code_extra_missing, syntax_error
from sldb.api.notations.component_spec_python_build import _build_spec, _sanitize_id
from sldb.code.runtime import available
from sldb.code.scan import scan_tree
from sldb.core.finding import Finding


def component_spec_from_python(src_dir: str | Path, project_id: str = "project", title: str = "Python AST Architecture",
                               root_package: str | None = None) -> tuple[dict | None, list[Finding]]:
    """`(spec, findings)` for every `.py` under `src_dir`; `(None, [alert])` without the `[code]` extra."""
    if not available():
        return None, [code_extra_missing(src_dir)]
    elements: list[dict] = []
    relations: list[dict] = []
    findings: list[Finding] = []
    for module, classes in _modules(scan_tree(Path(src_dir)), root_package):
        findings += _module_elements(module, classes, elements, relations)
    return _build_spec(project_id, title, elements, relations), findings


def _modules(facts: list[dict], root_package: str | None) -> list[tuple[dict, list[dict]]]:
    """Each wanted module fact in path order, with its top-level class facts in source order."""
    classes: dict[str, list[dict]] = {}
    for fact in facts:
        if fact["kind"] == "class" and "." not in fact["qualified_name"]:
            classes.setdefault(fact["path"], []).append(fact)
    modules = sorted((f for f in facts if f["kind"] == "module" and _wanted(f["path"], root_package)), key=lambda f: tuple(f["path"].split("/")))
    return [(m, sorted(classes.get(m["path"], []), key=lambda c: c["span"]["start_line"])) for m in modules]


def _wanted(path: str, root_package: str | None) -> bool:
    return path.rsplit("/", 1)[-1] != "__init__.py" and (not root_package or path.startswith(root_package.replace(".", "/")))


def _module_elements(module: dict, classes: list[dict], elements: list[dict], relations: list[dict]) -> list[Finding]:
    """Elements and relations of one module; an unparsable file keeps only its module node."""
    name = module["qualified_name"]
    safe_id = f"module_{_sanitize_id(name)}"
    elements.append({"id": safe_id, "kind": "module", "label": name})
    if module["attrs"].get("has_error"):
        return [syntax_error(module["path"])]
    _class_elements(name, safe_id, classes, elements, relations)
    relations += [{"source": safe_id, "target": f"module_{_sanitize_id(t)}", "kind": "imports"} for t in _imports(name, module["attrs"]["imports"] + module["attrs"].get("nested_imports", []))]
    return []


def _class_elements(name: str, safe_id: str, classes: list[dict], elements: list[dict], relations: list[dict]) -> None:
    for cls in classes:
        cls_id = f"class_{_sanitize_id(name)}_{cls['name']}"
        elements.append({"id": cls_id, "kind": "class", "label": cls["name"]})
        relations.append({"source": safe_id, "target": cls_id, "kind": "defines"})


def _imports(module: str, imports: list[str]) -> list[str]:
    """Each imported module once, in first-seen order, relative ones resolved against `module`'s package."""
    targets = [_resolve(module, name) for entry in imports for name in entry.split(",")]
    return list(dict.fromkeys(t for t in targets if t))


def _resolve(module: str, target: str) -> str | None:
    if not target.startswith("."):
        return target
    level = len(target) - len(target.lstrip("."))
    rest = target[level:]
    return ".".join(module.split(".")[:-level] + ([rest] if rest else [])) or None
