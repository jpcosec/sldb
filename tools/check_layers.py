#!/usr/bin/env python3
"""Puerta de capas: el grafo de paquetes no tiene ciclos y respeta el orden declarado.

El orden vive en `contracts/layers.toml`, no acá. Un orden escrito dentro de la
herramienta que lo verifica no se puede consultar sin leer código, y lo que no se
puede consultar no se discute.

Qué rechaza:

- un import que cierra un ciclo entre paquetes
- un import que sube de capa (una capa baja importando una alta)
- un paquete sin capa asignada — para que agregar uno obligue a decidir dónde va

Qué no ve: imports dentro de un mismo paquete, e imports construidos con
`importlib`. Son el límite declarado de esta puerta.

    python tools/check_layers.py
    python tools/check_layers.py --graph    # el grafo, para leerlo
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

#: Un import de `sldb.<paquete>`, en cualquier forma: arriba del archivo o
#: diferido dentro de una función.
IMPORT = re.compile(r"^(\s*)(?:from|import)\s+sldb\.([a-z_]+)", re.M)


def load_contract() -> tuple[dict[str, int], dict]:
    if not CONTRACT.is_file():
        sys.exit(f"falta el contrato de capas: {CONTRACT.relative_to(ROOT)}")
    data = tomllib.loads(CONTRACT.read_text(encoding="utf-8"))
    layers = {pkg: i for i, group in enumerate(data["layers"]) for pkg in group["packages"]}
    return layers, data


def scan() -> tuple[dict[str, set[str]], list[dict]]:
    """Las aristas entre paquetes, y cada import individual con su ubicación."""
    edges: dict[str, set[str]] = defaultdict(set)
    details = []
    for path in sorted(SRC.rglob("*.py")):
        parts = path.relative_to(SRC).parts
        src_pkg = parts[0] if len(parts) > 1 else "<root>"
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in IMPORT.finditer(text):
            indent, dst_pkg = match.group(1), match.group(2)
            if dst_pkg == src_pkg:
                continue
            edges[src_pkg].add(dst_pkg)
            details.append({
                "from": src_pkg, "to": dst_pkg,
                "at": f"{path.relative_to(ROOT)}#L{text[:match.start()].count(chr(10)) + 1}",
                "deferred": bool(indent),
            })
    return edges, details


def find_cycles(edges: dict[str, set[str]]) -> list[list[str]]:
    """Todo ciclo dirigido, por búsqueda en profundidad sobre la pila activa."""
    cycles, seen = [], set()

    def walk(node: str, stack: list[str]) -> None:
        for nxt in sorted(edges.get(node, ())):
            if nxt in stack:
                cycle = stack[stack.index(nxt):] + [nxt]
                key = frozenset(cycle)
                if key not in seen:
                    seen.add(key)
                    cycles.append(cycle)
            elif nxt not in stack:
                walk(nxt, stack + [nxt])

    for pkg in sorted(edges):
        walk(pkg, [pkg])
    return cycles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", action="store_true", help="imprime el grafo y sale")
    args = parser.parse_args()

    layers, contract = load_contract()
    edges, details = scan()

    if args.graph:
        for pkg in sorted(edges):
            lvl = layers.get(pkg, "?")
            print(f"  [{lvl}] {pkg:10} -> {', '.join(sorted(edges[pkg])) or '—'}")
        return 0

    problems: list[str] = []
    counted_cycles: list[list[str]] = []

    # Un paquete sin capa no se puede juzgar: agregar uno obliga a decidir.
    known = set(layers) | {"<root>"}
    for pkg in sorted(set(edges) | {p for dsts in edges.values() for p in dsts}):
        if pkg not in known:
            problems.append(f"paquete sin capa asignada en el contrato: {pkg}")

    # Un ciclo pasa solo si cada arista que sube está contada en [allow].upward.
    # Así la puerta rechaza un ciclo NUEVO sin exigir que los viejos se arreglen
    # hoy: la deuda contada pasa, la deuda silenciosa no.
    counted = {tuple(x) for x in contract.get("allow", {}).get("upward", [])}

    def accounted(a: str, b: str) -> bool:
        """Si esta arista está autorizada por el contrato.

        Dos vías: una excepción explícita, o estar dentro de la misma capa — que
        la regla del contrato permite, y que es como se declara un grupo de
        paquetes mutuamente dependientes sin fingir que no lo son.
        """
        return (a, b) in counted or layers.get(b, 0) <= layers.get(a, 0)

    for cycle in find_cycles(edges):
        unaccounted = [f"{a}→{b}" for a, b in zip(cycle, cycle[1:])
                       if not accounted(a, b)]
        if unaccounted:
            problems.append(
                f"ciclo no contado: {' → '.join(cycle)} "
                f"(aristas sin autorizar: {', '.join(unaccounted)})")
        else:
            counted_cycles.append(cycle)

    allowed = {tuple(x) for x in contract.get("allow", {}).get("upward", [])}
    for edge in details:
        src, dst = edge["from"], edge["to"]
        if src not in layers or dst not in layers:
            continue
        if layers[dst] > layers[src] and (src, dst) not in allowed:
            problems.append(
                f"import hacia arriba: {src}(capa {layers[src]}) → "
                f"{dst}(capa {layers[dst]}) en {edge['at']}")

    # Una excepción que ya se reparó y nadie borró es la forma en que esta lista
    # se convierte en ficción: seguiría autorizando algo que no ocurre.
    live = {(e["from"], e["to"]) for e in details}
    for src, dst in sorted(allowed):
        if (src, dst) not in live:
            problems.append(
                f"excepción vencida en el contrato: {src} → {dst} ya no ocurre; "
                f"bórrala de [allow].upward")

    for problem in problems:
        print(f"  ERROR  {problem}")
    for cycle in counted_cycles:
        print(f"  deuda  ciclo contado: {' → '.join(cycle)}")

    deferred = [e for e in details if e["deferred"]]
    pending = len(contract.get("pending", []))
    print(f"  nota   {len(deferred)} imports diferidos (dentro de funciones), "
          f"no bloquean pero suelen esquivar un ciclo")
    if pending:
        print(f"  nota   {pending} reparaciones pendientes declaradas en el contrato; "
              f"mientras existan, el orden de capas es aspiracional")
    print(f"{'FAIL' if problems else 'PASS'}: capas — "
          f"{len(edges)} paquetes, {sum(len(v) for v in edges.values())} aristas, "
          f"{len(problems)} violaciones, {len(counted_cycles)} ciclos contados")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
