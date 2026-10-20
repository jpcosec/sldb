#!/usr/bin/env python3
"""Puerta de ejes: el mapa de capacidades corresponde al código.

Las capas dicen quién puede importar a quién. Los ejes dicen qué sabe hacer el
sistema. Son dimensiones ortogonales y ambas se degradan en silencio: un mapa de
capacidades escrito a mano envejece igual que cualquier inventario.

El mapa está en `contracts/layers.toml`, sección `[[axis]]`.

Qué rechaza:

- una ruta declarada en un eje que no existe
- un archivo de `src/` que ningún eje reclama
- una dependencia externa confinada a un eje que se filtró a otro
- un eje marcado `extractable` que empezó a importar de fuera

Qué no ve: si la descripción de lo que un eje «sabe hacer» es buena. Eso es prosa
y queda para revisión humana.

    python tools/check_axes.py
    python tools/check_axes.py --map    # el mapa con el acoplamiento medido
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "sldb"
CONTRACT = ROOT / "contracts" / "layers.toml"

#: Fuera del mapa por diseño: la interfaz es transporte y no una capacidad, los
#: ejemplos y plantillas son material, y la raíz del paquete solo reexporta.
#: Fuera del mapa por diseño: la interfaz es transporte, no una capacidad, y los
#: ejemplos y plantillas son material. Todo lo demás debe pertenecer a un eje.
UNMAPPED = {"cli", "examples", "assets", "templates"}

#: Archivos de la raíz del paquete que no son una capacidad: el punto de entrada.
UNMAPPED_FILES = {"__main__.py"}

#: Nombre del módulo de Python para cada dependencia declarada en el contrato.
MODULE = {"markdown-it-py": "markdown_it", "pydantic": "pydantic",
          "jinja2": "jinja2", "networkx": "networkx", "click": "click",
          "argparse": "argparse", "ast": "ast", "tree-sitter": "tree_sitter", "tree-sitter-python": "tree_sitter_python"}


def load() -> dict:
    return tomllib.loads(CONTRACT.read_text(encoding="utf-8"))


def owner_map(axes: list[dict]) -> tuple[dict[str, str], set[str]]:
    """Qué eje reclama cada archivo, y qué ejes declaran una carpeta entera.

    La distinción importa: un eje que declara `links` absorbe cualquier archivo
    nuevo que alguien ponga ahí, sin que nada lo note. Un eje que declara archivos
    uno por uno obliga a decidir. Lo primero es cómodo y lo segundo es una puerta,
    así que al menos hay que saber cuáles son cómodos.
    """
    owner: dict[str, str] = {}
    wildcard: set[str] = set()
    for axis in axes:
        for declared in axis["paths"]:
            target = SRC / declared
            if target.suffix == ".py":
                if target.is_file():
                    owner[str(target.relative_to(SRC))] = axis["id"]
                continue
            wildcard.add(axis["id"])
            for path in target.rglob("*.py"):
                if path.is_file():
                    owner[str(path.relative_to(SRC))] = axis["id"]
    return owner, wildcard


def coupling(owner: dict[str, str]) -> dict[tuple[str, str], int]:
    """Aristas entre ejes: un import de un archivo de A a un archivo de B."""
    edges: dict[tuple[str, str], int] = defaultdict(int)
    for rel, axis in owner.items():
        text = (SRC / rel).read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r"from sldb\.([\w.]+) import", text):
            base = match.group(1).replace(".", "/")
            for candidate in (f"{base}.py", f"{base}/__init__.py"):
                if (target := owner.get(candidate)) and target != axis:
                    edges[(axis, target)] += 1
                    break
    return edges


def print_units(contract: dict, sizes: dict[str, int]) -> None:
    """Las unidades viables declaradas, y la función que le falta a cada una.

    Los niveles del DAG no son las unidades, y confundirlos es el error natural
    al leer el grafo: un nivel responde «¿quién importa a quién?» y una unidad
    «¿qué se sostiene solo?».
    """
    units = contract.get("unit", [])
    if not units:
        print("  el contrato no declara unidades")
        return

    gaps: dict[str, list[str]] = {}
    for gap in contract.get("unit_gap", []):
        for unit in gap["missing_in"]:
            gaps.setdefault(unit, []).append(gap["function"])

    print("  unidad          ejes  arch.  necesita  la necesitan  le falta")
    for unit in units:
        total = sum(sizes.get(a, 0) for a in unit["axes"])
        mark = "·extraíble" if unit.get("extractable_today") else ""
        print(f"  {unit['id']:15} {len(unit['axes']):3} {total:6} "
              f"{unit['needs']:9} {unit['needed_by']:13}  "
              f"{', '.join(gaps.get(unit['id'], [])) or '—'} {mark}")

    for other in contract.get("non_unit", []):
        total = sum(sizes.get(a, 0) for a in other["axes"])
        print(f"\n  NO es unidad: {other['id']} ({total} archivos) — "
              f"{other['verdict']}")
        print(f"    necesita {other['needs']}, lo necesitan {other['needed_by']}")

    pins = contract.get("pins", {})
    if pins:
        print(f"\n  alfileres: {pins['core_knot']} aristas de peso 1 cierran el "
              f"nudo del núcleo, {pins['operation_knot']} de peso ≤2 el de operación")
        print("  mientras existan, reorganizar carpetas es cosmético")


def print_dag(axes: list[dict], owner: dict[str, str], sizes: dict[str, int]) -> None:
    """El orden de dependencia entre ejes, y los nudos que lo impiden.

    El grafo de ejes **no** es acíclico. Un dibujo por niveles es verdadero y
    engañoso a la vez: el orden existe, pero esconde que algunos de sus nodos son
    grupos de ejes mutuamente dependientes. Esto imprime las dos cosas.
    """
    import networkx as nx

    edges = coupling(owner)
    graph = nx.DiGraph([(a, b, {"weight": n}) for (a, b), n in edges.items()])
    graph.add_nodes_from(a["id"] for a in axes)

    acyclic = nx.is_directed_acyclic_graph(graph)
    print(f"  es DAG: {'sí' if acyclic else 'NO'}")
    if not acyclic:
        print(f"  {len(list(nx.simple_cycles(graph)))} ciclos entre ejes")

    groups = list(nx.strongly_connected_components(graph))
    knots = sorted((g for g in groups if len(g) > 1), key=len, reverse=True)

    condensed = nx.condensation(graph, groups)
    level: dict[int, int] = {}
    for node in nx.topological_sort(condensed):
        level[node] = max((level[p] for p in condensed.predecessors(node)),
                          default=-1) + 1

    print("\n  niveles (0 = no depende de nadie):")
    for node in sorted(level, key=lambda n: -level[n]):
        members = sorted(condensed.nodes[node]["members"])
        total = sum(sizes[m] for m in members)
        label = (f"nudo de {len(members)}: {', '.join(members)}"
                 if len(members) > 1 else members[0])
        print(f"    nivel {level[node]}  {label}  ({total} archivos)")

    for knot in knots:
        inner = sorted(((a, b, n) for (a, b), n in edges.items()
                        if a in knot and b in knot), key=lambda x: -x[2])
        weak = [e for e in inner if e[2] <= 2]
        print(f"\n  nudo de {len(knot)} ejes — {len(inner)} aristas internas, "
              f"{len(weak)} de peso ≤2:")
        for a, b, n in weak:
            print(f"    {a:20} → {b:20} {n}")

    print("\n  cuánto se desarma al ignorar las aristas débiles:")
    for threshold in (1, 2, 3, 5, 8):
        pruned = nx.DiGraph([(a, b) for (a, b), n in edges.items() if n > threshold])
        pruned.add_nodes_from(a["id"] for a in axes)
        left = [g for g in nx.strongly_connected_components(pruned) if len(g) > 1]
        verdict = ("DAG" if not left else
                   f"{len(left)} nudos, el mayor de {max(len(g) for g in left)}")
        print(f"    peso ≤{threshold}: {verdict}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", action="store_true", help="imprime el mapa y sale")
    parser.add_argument("--dag", action="store_true",
                        help="niveles, nudos y las aristas que los cierran")
    parser.add_argument("--units", action="store_true",
                        help="las unidades viables y qué función les falta")
    args = parser.parse_args()

    contract = load()
    axes = contract.get("axis", [])
    if not axes:
        sys.exit("el contrato no declara ejes")

    owner, wildcard = owner_map(axes)
    sizes: dict[str, int] = defaultdict(int)
    for axis in owner.values():
        sizes[axis] += 1

    if args.map:
        print("  eje                    archivos  identidad  externo")
        for axis in axes:
            mark = "sí" if axis.get("identity") else "  "
            print(f"  {axis['id']:22} {sizes[axis['id']]:5}      {mark}       "
                  f"{', '.join(axis.get('external') or []) or '—'}")
        print("\n  acoplamiento entre ejes:")
        for (a, b), n in sorted(coupling(owner).items(), key=lambda x: -x[1]):
            print(f"    {a:20} → {b:20} {n}")
        return 0

    if args.dag:
        print_dag(axes, owner, sizes)
        return 0

    if args.units:
        print_units(contract, sizes)
        return 0

    problems: list[str] = []

    # Una ruta declarada y ausente: el mapa habla de algo que ya no existe.
    for axis in axes:
        for declared in axis["paths"]:
            if not (SRC / declared).exists():
                problems.append(
                    f"el eje `{axis['id']}` declara `{declared}` y no existe")

    # Un archivo que ningún eje reclama: una capacidad nueva sin declarar, o un
    # archivo que cambió de sitio sin que el mapa lo siguiera.
    for path in sorted(SRC.rglob("*.py")):
        rel = path.relative_to(SRC)
        if (rel.parts[0] in UNMAPPED or rel.name == "__init__.py"
                or str(rel) in UNMAPPED_FILES):
            continue
        if str(rel) not in owner:
            problems.append(f"archivo sin eje: {rel} — decide a qué capacidad pertenece")

    # Una dependencia externa confinada a un eje es la prueba de que el eje tiene
    # frontera. Si se filtra a otro, la frontera se rompió.
    # Una dependencia puede estar declarada en varios ejes — `networkx` lo está en
    # dos. Lo que se verifica es que no aparezca en NINGUNO de los demás, no que
    # viva en uno solo. La primera versión salía del bucle cuando había más de un
    # declarante, y entonces las dos dependencias más importantes del sistema
    # quedaban sin vigilar.
    pervasive = set(contract.get("axis_external", {}).get("pervasive", []))
    confined = defaultdict(set)
    for axis in axes:
        for dep in axis.get("external") or []:
            confined[dep].add(axis["id"])
    for dep, owners in sorted(confined.items()):
        if dep not in MODULE or dep in pervasive:
            continue
        module = MODULE[dep]
        pattern = re.compile(rf"^\s*(?:import {module}|from {module}[\s.])", re.M)
        for rel, axis in sorted(owner.items()):
            if axis in owners:
                continue
            if pattern.search((SRC / rel).read_text(encoding="utf-8", errors="ignore")):
                problems.append(
                    f"{rel}: el eje `{axis}` usa `{dep}`, declarada de "
                    f"`{', '.join(sorted(owners))}`")

    # Un eje extraíble que empieza a importar de fuera deja de serlo, y esa es
    # justamente la propiedad por la que se lo marcó.
    for axis in axes:
        if not axis.get("extractable"):
            continue
        inside = {r for r, a in owner.items() if a == axis["id"]}
        for rel in sorted(inside):
            text = (SRC / rel).read_text(encoding="utf-8", errors="ignore")
            for match in re.finditer(r"from sldb\.([\w.]+) import", text):
                base = match.group(1).replace(".", "/")
                hit = next((owner.get(c) for c in (f"{base}.py", f"{base}/__init__.py")
                            if owner.get(c)), None)
                if hit and hit != axis["id"]:
                    problems.append(
                        f"{rel}: el eje `{axis['id']}` está marcado extraíble y "
                        f"ahora importa de `{hit}`")

    # Las unidades declaradas tienen que cubrir todos los ejes, y sus cifras de
    # acoplamiento tienen que corresponder al código. Un contrato de unidades que
    # envejece es peor que no tenerlo: afirma que algo se sostiene solo.
    units = contract.get("unit", []) + contract.get("non_unit", [])
    if units:
        declared = {a for u in units for a in u["axes"]}
        known = {a["id"] for a in axes}
        for extra in sorted(declared - known):
            problems.append(f"una unidad declara el eje `{extra}`, que no existe")
        for orphan in sorted(known - declared):
            problems.append(
                f"el eje `{orphan}` no pertenece a ninguna unidad — "
                f"decide si se sostiene solo o dentro de cuál")

        edges = coupling(owner)
        for unit in units:
            members = set(unit["axes"])
            needs = sum(1 for (a, b) in edges if a in members and b not in members)
            needed = sum(1 for (a, b) in edges if b in members and a not in members)
            if needs != unit["needs"] or needed != unit["needed_by"]:
                problems.append(
                    f"la unidad `{unit['id']}` declara necesitar {unit['needs']} "
                    f"y ser necesitada por {unit['needed_by']}; el código dice "
                    f"{needs} y {needed}")

    # El corte mínimo declarado del núcleo tiene que seguir siendo el mínimo. Si
    # alguien agrega una arista interna, el corte cambia y la cifra del contrato
    # pasa a describir un sistema que ya no existe.
    cut = contract.get("nucleo_min_cut")
    if cut:
        import networkx as nx
        nucleus = next((u for u in contract.get("unit", [])
                        if u["id"] == "nucleo"), None)
        knot = {"contrato", "render", "representacion", "superficie", "runtime"}
        inner = [(a, b, n) for (a, b), n in coupling(owner).items()
                 if a in knot and b in knot]
        declared_cuts = {tuple(c["edge"].split(" → ")) for c in cut["cuts"]}
        pruned = nx.DiGraph([(a, b) for a, b, _ in inner
                             if (a, b) not in declared_cuts])
        pruned.add_nodes_from(knot)
        if not nx.is_directed_acyclic_graph(pruned):
            problems.append(
                "el corte declarado en [nucleo_min_cut] ya no deja un DAG: "
                "aparecieron aristas internas nuevas en el núcleo")
        weight = sum(n for a, b, n in inner if (a, b) in declared_cuts)
        if weight != cut["total_weight"]:
            problems.append(
                f"[nucleo_min_cut] declara peso {cut['total_weight']}; "
                f"el código dice {weight}")
        for entry in cut["cuts"]:
            path, _, line = entry["at"].partition("#L")
            if not (SRC / path).is_file():
                problems.append(f"[nucleo_min_cut] apunta a `{path}`, que no existe")

    for problem in problems:
        print(f"  ERROR  {problem}")

    if cut:
        print(f"  nota   el núcleo se parte cortando {cut['edges']} aristas "
              f"de peso total {cut['total_weight']}")

    if units:
        viable = contract.get("unit", [])
        ready = [u["id"] for u in viable if u.get("extractable_today")]
        print(f"  nota   {len(viable)} unidades viables, {len(ready)} extraíbles hoy: "
              f"{', '.join(ready)}")
        for gap in contract.get("unit_gap", []):
            print(f"  deuda  función `{gap['function']}` ausente en "
                  f"{len(gap['missing_in'])} de {len(viable)} unidades")

    identity = [a["id"] for a in axes if a.get("identity")]
    debt = contract.get("axis_debt", [])
    print(f"  nota   {len(identity)} ejes de identidad: {', '.join(identity)}")
    print(f"  nota   {len(wildcard)} de {len(axes)} ejes declaran carpetas enteras "
          f"y absorben archivos nuevos sin avisar")
    if debt:
        print(f"  deuda  {len(debt)} deudas de eje declaradas: "
              f"{', '.join(d['id'] for d in debt)}")
    print(f"{'FAIL' if problems else 'PASS'}: ejes — {len(axes)} declarados, "
          f"{len(owner)} archivos mapeados, {len(problems)} violaciones")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
