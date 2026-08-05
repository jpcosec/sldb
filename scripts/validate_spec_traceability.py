#!/usr/bin/env python3
"""Valida la trazabilidad spec ↔ atoms ↔ vistas ↔ puml ↔ HTML.

Contratos gobernantes:
  - docs/architecture/contracts/specyaml-schema-contract.md
  - docs/architecture/contracts/diagram-traceability-contract.md

Exit 0 = todo verde (warnings no son fatales). Exit 1 = errores.
"""
import importlib.util
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ARCH = ROOT / "docs" / "architecture"
SPEC_DIR = ARCH / "spec2viz"
PUML_DIR = ARCH / "core-diagrams"
ATOMS_DIR = ROOT / "desk" / "atoms"
MANIFEST = SPEC_DIR / "manifest.yml"

KINDS = {"core", "boundary", "database", "server", "client", "backend"}
EDGE_KEY = {"component": ("edges", "relation"), "deployment": ("connections", "protocol")}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text())
    except Exception as e:  # noqa: BLE001
        err(f"{path.relative_to(ROOT)}: YAML inválido: {e}")
        return None


def check_spec(path: Path, vista_ids: set[str], atoms: set[str]) -> tuple[str, list[str]] | None:
    spec = load_yaml(path)
    if spec is None:
        return None
    rel = path.relative_to(ROOT)
    for key in ("id", "title", "type", "version", "views", "data"):
        if key not in spec:
            err(f"{rel}: falta campo requerido '{key}'")
    sid = spec.get("id", "?")
    stype = spec.get("type")
    if stype not in EDGE_KEY:
        err(f"{rel}: type '{stype}' no soportado (component|deployment)")
        return None
    edge_coll, rel_key = EDGE_KEY[stype]

    data = spec.get("data") or {}
    nodes = data.get("nodes") or {}
    artifacts = data.get("artifacts") or {}
    if stype == "deployment" and not artifacts:
        warn(f"{rel}: deployment sin artifacts")
    all_ids = set(nodes) | set(artifacts)

    for nid, node in list(nodes.items()) + list(artifacts.items()):
        if not isinstance(node, dict):
            err(f"{rel}: nodo '{nid}' mal formado")
            continue
        if "label" not in node:
            err(f"{rel}: nodo '{nid}' sin label")
        kind = node.get("kind")
        if kind not in KINDS:
            err(f"{rel}: nodo '{nid}' kind '{kind}' fuera de vocabulario {sorted(KINDS)}")
        for ref in node.get("contains") or []:
            if ref not in all_ids:
                err(f"{rel}: nodo '{nid}' contains '{ref}' indefinido")
        for atom in node.get("atoms") or []:
            if atom not in atoms:
                err(f"{rel}: nodo '{nid}' referencia atom inexistente '{atom}'")

    for edge in data.get(edge_coll) or []:
        frm, to = edge.get("from"), edge.get("to")
        if frm not in all_ids:
            err(f"{rel}: edge from '{frm}' indefinido")
        if to not in all_ids:
            err(f"{rel}: edge to '{to}' indefinido")
        if rel_key not in edge:
            err(f"{rel}: edge {frm}→{to} sin '{rel_key}'")

    views = spec.get("views") or []
    for v in views:
        if v not in vista_ids:
            err(f"{rel}: views referencia vista inexistente '{v}'")
    if not views:
        warn(f"{rel}: spec sin vistas (cobertura visual vacía)")
    return sid, views


def main() -> int:
    atoms = {p.stem for p in ATOMS_DIR.glob("*.md")}
    if not atoms:
        err(f"no se encontraron atoms en {ATOMS_DIR}")

    manifest = load_yaml(MANIFEST) or {}
    registry_path = ARCH / "vistas" / "vistas.yml"
    registry = load_yaml(registry_path)
    if registry is None:
        print("\n".join("ERROR " + e for e in errors))
        return 1

    vistas = {v["id"]: v for v in registry.get("vistas") or []}
    vista_ids = set(vistas)

    # 1. registry: referencias existen
    puml_seen: dict[str, str] = {}
    for vid, v in vistas.items():
        for key in ("nav", "lbl", "title", "desc", "mmd", "specs"):
            if key not in v:
                err(f"vistas.yml: vista '{vid}' sin campo '{key}'")
        mmd = v.get("mmd")
        if mmd and not (ARCH / mmd).exists():
            err(f"vistas.yml: vista '{vid}' mmd inexistente: {mmd}")
        puml = v.get("puml")
        if puml:
            if not (PUML_DIR / puml).exists():
                err(f"vistas.yml: vista '{vid}' puml inexistente: {puml}")
            elif puml in puml_seen:
                err(f"vistas.yml: puml '{puml}' asignado a dos vistas ({puml_seen[puml]}, {vid})")
            puml_seen[puml] = vid
        if not v.get("specs"):
            warn(f"vistas.yml: vista '{vid}' sin specs asociados")

    # 2. specs: esquema + views
    spec_views: dict[str, list[str]] = {}
    spec_files = {s["id"]: s["file"] for s in manifest.get("specs") or []}
    for sid, fname in spec_files.items():
        result = check_spec(SPEC_DIR / fname, vista_ids, atoms)
        if result:
            got_sid, views = result
            if got_sid != sid:
                err(f"manifest: spec '{sid}' apunta a archivo con id '{got_sid}'")
            spec_views[got_sid] = views

    # 3. simetría spec.views ↔ vista.specs
    for vid, v in vistas.items():
        for sid in v.get("specs") or []:
            if sid not in spec_views:
                err(f"vista '{vid}' referencia spec desconocido '{sid}'")
            elif vid not in spec_views[sid]:
                err(f"asimetría: vista '{vid}' declara spec '{sid}' pero el spec no declara la vista")
    for sid, views in spec_views.items():
        for vid in views:
            if vid in vistas and sid not in (vistas[vid].get("specs") or []):
                err(f"asimetría: spec '{sid}' declara vista '{vid}' pero la vista no declara el spec")

    # 4. headers puml
    for puml_path in sorted(PUML_DIR.glob("*.puml")):
        head = puml_path.read_text().splitlines()[:6]
        m_v = next((l for l in head if l.startswith("' vista:")), None)
        m_g = next((l for l in head if l.startswith("' governed-by:")), None)
        rel = puml_path.relative_to(ROOT)
        if not m_v or not m_g:
            err(f"{rel}: falta header de trazabilidad (vista / governed-by)")
            continue
        vid = m_v.split(":", 1)[1].strip()
        specs = [s.strip() for s in m_g.split(":", 1)[1].split(",") if s.strip() != "none"]
        if puml_path.name not in puml_seen:
            err(f"{rel}: puml sin vista asignada en vistas.yml")
        elif puml_seen[puml_path.name] != vid:
            err(f"{rel}: header vista '{vid}' != registry '{puml_seen[puml_path.name]}'")
        elif sorted(specs) != sorted(vistas[vid].get("specs") or []):
            err(f"{rel}: header governed-by {specs} != registry specs {vistas[vid].get('specs')}")

    # 5. drift del HTML generado
    gen_path = ROOT / "scripts" / "generate_vistas_html.py"
    spec = importlib.util.spec_from_file_location("generate_vistas_html", gen_path)
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    expected = gen.render(ARCH)
    committed = (ARCH / "sldb_Kernel_Vistas_UML.html").read_text()
    if committed != expected:
        err("HTML desactualizado: regenerar con scripts/generate_vistas_html.py")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} errores, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
