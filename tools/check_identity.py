#!/usr/bin/env python3
"""Puerta de identidad: la frontera entre el producto y su autoaplicación.

Este repositorio es dos cosas: una biblioteca genérica, y esa biblioteca aplicada
a sí misma. La frontera entre las dos existía en el código y no estaba escrita en
ninguna parte, así que nadie podía decidir si una pieza nueva pertenecía.

El contrato está en `contracts/identity.toml`. Acá solo se verifica.

Qué rechaza:

- un modelo de autoaplicación importado desde un paquete del producto — la
  dirección que convierte una biblioteca en un programa de un solo sitio
- un paquete sin grupo asignado
- un directorio de primer nivel versionado y sin clasificar

Qué no ve: si una función es autoaplicable, y si un documento escrito a mano
debería derivarse. Ambas exigen juicio y están marcadas como no mecanizadas en
el contrato.

    python tools/check_identity.py
    python tools/check_identity.py --show    # la identidad declarada
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "sldb"
CONTRACT = ROOT / "contracts" / "identity.toml"

#: Directorios y archivos de primer nivel que no se clasifican: son del entorno,
#: no del sistema.
EXEMPT = {
    "src", "tests", "docs", "tools", "scripts", "build", "dist", "uv.lock",
    "pyproject.toml", "README.md", "CHANGELOG.md", "LICENSE", "standards.md",
    "propuesta",
}


def load() -> dict:
    if not CONTRACT.is_file():
        sys.exit(f"falta el contrato de identidad: {CONTRACT.relative_to(ROOT)}")
    return tomllib.loads(CONTRACT.read_text(encoding="utf-8"))


def executable_source(path: Path) -> str:
    """El código de un archivo sin comentarios ni cadenas de documentación.

    Citar una ruta de ejemplo en una docstring —«un ref es una ruta de proyecto,
    como `desk/tasks/task-a.md`»— no cruza ninguna frontera: explica. Lo que la
    cruza es código que depende de esa ruta.

    Sin esta distinción la puerta reporta como violación toda buena
    documentación, que es la forma más rápida de enseñar a ignorarla.
    """
    import ast as _ast

    text = path.read_text(encoding="utf-8", errors="ignore")
    try:
        tree = _ast.parse(text)
    except SyntaxError:
        return text

    # Las docstrings son expresiones de cadena solas en su enunciado.
    drop: set[int] = set()
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Expr) and isinstance(node.value, _ast.Constant) \
                and isinstance(node.value.value, str):
            drop.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))

    return "\n".join(
        "" if i in drop else re.sub(r"#.*$", "", line)
        for i, line in enumerate(text.splitlines(), 1))


def versioned_top_level() -> set[str]:
    """Lo que está bajo control de versiones, en el primer nivel."""
    done = subprocess.run(["git", "ls-files"], cwd=ROOT,
                          capture_output=True, text=True)
    return {line.split("/")[0] for line in done.stdout.splitlines() if line}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action="store_true",
                        help="imprime la identidad declarada y sale")
    args = parser.parse_args()

    contract = load()
    product = contract["product"]["packages"]
    self_app = contract["self_application"]
    self_models = self_app["models"]

    if args.show:
        print(contract["statement"].strip())
        print(f"\n  producto        {', '.join(product)}")
        print(f"  autoaplicación  {', '.join(self_app['packages'] + self_models)}")
        print(f"                  {', '.join(self_app['directories'])}")
        print(f"  ajeno           {', '.join(f['path'] for f in contract['foreign'])}")
        state = contract.get("status", {})
        if state:
            print(f"\n  estado: {state['state']} — {state['former_claim']} "
                  f"no ocurrió ({state['commits_after_claim']} commits después)")
        return 0

    problems: list[str] = []

    # La frontera que importa: el producto es genérico, así que no puede nombrar
    # el contenido concreto de ESTE repositorio.
    #
    # La versión anterior de esta puerta compraba los modelos de `selfdoc` como
    # «autoaplicación» y verificaba que el producto no los importara. Al corregir
    # la identidad esa lista quedó vacía, y con ella la puerta pasó a no medir
    # nada mientras seguía imprimiendo PASS. Una puerta vacía es peor que ninguna:
    # afirma una garantía inexistente.
    #
    # La regla correcta es sobre rutas, no sobre modelos: un paquete genérico que
    # menciona `knowledge/` o `desk/` dejó de ser genérico.
    owned = [d for d in self_app["directories"] if not d.startswith(".")]
    paths = {d: re.compile(rf"['\"]{re.escape(d)}/") for d in owned}
    for pkg in product:
        for path in sorted((SRC / pkg).rglob("*.py")):
            code = executable_source(path)
            known_debt = {d["at"].split("#")[0] for d in contract.get("boundary_debt", [])}
            if str(path.relative_to(ROOT)) in known_debt:
                continue
            for directory, pattern in paths.items():
                if pattern.search(code):
                    problems.append(
                        f"{path.relative_to(ROOT)}: el producto ({pkg}) nombra "
                        f"`{directory}/`, que es contenido de este repositorio")

    # Y los modelos del producto declarados en el contrato tienen que existir.
    # Sin esto, el contrato puede listar cualquier cosa y nadie se enteraría.
    declared_models = [m for group in contract["product"].get("models", {}).values()
                       for m in group]
    for model in declared_models:
        if not (SRC / "models" / f"{model}.py").is_file():
            problems.append(
                f"el contrato declara el modelo `{model}` y no existe en "
                f"src/sldb/models/")

    # El inverso: un modelo que existe y el contrato no clasifica.
    for path in sorted((SRC / "models").glob("*.py")):
        if path.stem not in {*declared_models, "__init__"}:
            problems.append(
                f"el modelo `{path.stem}` existe y el contrato no lo clasifica")

    # Los paquetes mezclados cuentan deuda, no violación: la frontera corre por
    # dentro de ellos y no se puede verificar hasta separarlos.
    mixed = contract["product"].get("mixed", {}).get("packages", [])
    self_models = self_models or []

    # Un paquete sin grupo no se puede juzgar, así que agregar uno obliga a
    # decidir de qué lado de la frontera queda.
    classified = set(product) | set(self_app["packages"]) | set(mixed)
    for pkg in sorted(p.name for p in SRC.iterdir()
                      if p.is_dir() and not p.name.startswith("__")):
        if pkg not in classified and pkg not in {"examples", "assets", "templates", "links"}:
            problems.append(f"paquete sin grupo en el contrato: {pkg}")

    # Un directorio versionado y sin clasificar hace que la identidad sea
    # indecidible: nadie puede responder si pertenece.
    known = (set(self_app["directories"]) |
             {f["path"] for f in contract["foreign"]} |
             {o["path"] for o in contract.get("orphan", [])} | EXEMPT)
    for entry in sorted(versioned_top_level()):
        if entry in known or entry.startswith("."):
            continue
        kind = "directorio" if (ROOT / entry).is_dir() else "archivo"
        problems.append(
            f"{kind} versionado sin clasificar en la raíz: {entry} — "
            f"decide si es producto, autoaplicación o ajeno")

    for problem in problems:
        print(f"  ERROR  {problem}")

    if mixed:
        print(f"  deuda  {', '.join(mixed)}: contienen producto y autoaplicación "
              f"mezclados; la frontera no se verifica ahí dentro")

    if debt := contract.get("boundary_debt", []):
        print(f"  deuda  {len(debt)} cruces de frontera contados: código del "
              f"producto que nombra contenido de este repositorio")
        print(f"  deuda  mientras existan, «el producto es genérico» es aspiracional")

    if orphans := contract.get("orphan", []):
        print(f"  deuda  {len(orphans)} huérfanos en la raíz, contados en el "
              f"contrato con la acción pendiente de cada uno")

    foreign = len(contract["foreign"])
    manual = sum(1 for r in contract["rejects"] if not r["mechanized"])
    print(f"  nota   {foreign} directorios declarados ajenos")
    print(f"  nota   {len(declared_models)} modelos del producto clasificados, "
          f"{len(owned)} directorios de contenido vigilados")
    print(f"  nota   {manual} de {len(contract['rejects'])} reglas de rechazo "
          f"no son mecanizables y quedan para revisión humana")
    state = contract.get("status", {})
    if state.get("state") == "activo":
        print(f"  nota   estado: activo (resuelto {state['resolved']}); "
              f"el congelamiento declarado no ocurrió")
    print(f"{'FAIL' if problems else 'PASS'}: identidad — "
          f"{len(product)} paquetes de producto, "
          f"{len(declared_models)} modelos clasificados, "
          f"{len(problems)} violaciones")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
