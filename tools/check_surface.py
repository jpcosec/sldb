#!/usr/bin/env python3
"""Puerta de superficie: lo que los consumidores importan está declarado.

La superficie de esta biblioteca no se diseñó: la construyeron sus consumidores
importando lo que necesitaban. Esta puerta lee lo que piden los cinco proyectos
del ecosistema y lo compara con lo declarado en `contracts/identity.toml`.

Qué rechaza:

- un símbolo que un consumidor importa y ninguna puerta declara
- un consumidor importando un nombre privado (con guion bajo)
- un consumidor importando de `cli/` desde código de producción
- una cifra del contrato que ya no corresponde

Qué no ve: si la superficie es *buena*. Solo si corresponde a lo que se usa.

Los consumidores viven fuera de este repositorio, así que la puerta se salta sola
cuando no los encuentra — y lo dice, en vez de pasar en silencio.

    python tools/check_surface.py
    python tools/check_surface.py --report    # qué pide cada consumidor
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ECOSYSTEM = ROOT.parent
CONTRACT = ROOT / "contracts" / "identity.toml"

#: `from sldb.algo import A, B` y `from sldb import C`.
IMPORT = re.compile(r"from\s+(sldb[\w.]*)\s+import\s+([^\n(]+)")

#: Una ruta de prueba. Un consumidor puede invocar la interfaz desde sus pruebas
#: —eso es probar el transporte como transporte— y no cuenta como acoplamiento.
TESTS = re.compile(r"(^|/)tests?(/|$)")


def load() -> dict:
    return tomllib.loads(CONTRACT.read_text(encoding="utf-8"))


def requested(consumers: list[str]) -> dict[str, list[dict]]:
    """Qué símbolo pide cada consumidor, con dónde y de qué módulo."""
    found: dict[str, list[dict]] = defaultdict(list)
    for name in consumers:
        root = ECOSYSTEM / name
        if not root.is_dir():
            continue
        for path in root.rglob("*.py"):
            rel = str(path.relative_to(ECOSYSTEM))
            is_test = bool(TESTS.search(str(path.parent))) or path.name.startswith("test_")
            text = path.read_text(encoding="utf-8", errors="ignore")
            for module, names in IMPORT.findall(text):
                for symbol in (n.strip() for n in names.split(",")):
                    symbol = symbol.split(" as ")[0].strip()
                    if symbol and symbol.isidentifier():
                        found[symbol].append(
                            {"consumer": name, "module": module,
                             "at": rel, "test": is_test})
    return found


def declared(contract: dict) -> set[str]:
    """Los símbolos que el contrato declara, más los que el paquete ya exporta."""
    names = {s for door in contract["surface"]["door"]
             for s in door.get("examples", [])}
    names |= set(contract["surface"]["multi_consumer"])
    for init in (ROOT / "src" / "sldb").rglob("__init__.py"):
        text = init.read_text(encoding="utf-8", errors="ignore")
        if match := re.search(r"__all__\s*=\s*\[(.*?)\]", text, re.S):
            names |= set(re.findall(r"['\"]([A-Za-z_]\w*)['\"]", match.group(1)))
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="store_true",
                        help="qué pide cada consumidor, y sale")
    args = parser.parse_args()

    contract = load()
    surface = contract.get("surface")
    if not surface:
        print("PASS: superficie — el contrato no declara una superficie todavía")
        return 0

    consumers = surface["consumers"]
    asked = requested(consumers)
    present = sorted({c["consumer"] for hits in asked.values() for c in hits})

    if not present:
        print(f"  aviso  ninguno de los {len(consumers)} consumidores está "
              f"en {ECOSYSTEM}")
        print("  aviso  la superficie no se comprueba en esta corrida")
        print("PASS: superficie — omitida por falta de consumidores")
        return 0

    if args.report:
        by_consumer: dict[str, set[str]] = defaultdict(set)
        for symbol, hits in asked.items():
            for hit in hits:
                by_consumer[hit["consumer"]].add(symbol)
        for name in sorted(by_consumer, key=lambda c: -len(by_consumer[c])):
            print(f"  {name:15} {len(by_consumer[name]):3} símbolos")
        print("\n  con más de un consumidor:")
        for symbol, hits in sorted(asked.items(),
                                   key=lambda x: -len({h['consumer'] for h in x[1]})):
            users = {h["consumer"] for h in hits}
            if len(users) > 1:
                print(f"    {symbol:26} {len(users)}  {', '.join(sorted(users))}")
        return 0

    known = declared(contract)
    debts = {d["id"] for d in contract.get("surface_debt", [])}
    problems: list[str] = []

    private = sorted(s for s in asked if s.startswith("_"))
    if private and "privados-importados" not in debts:
        for symbol in private:
            where = asked[symbol][0]
            problems.append(f"{where['consumer']} importa el privado `{symbol}` "
                            f"desde {where['module']} ({where['at']})")

    from_cli = sorted({
        (hit["consumer"], symbol) for symbol, hits in asked.items() for hit in hits
        if hit["module"].startswith("sldb.cli") and not hit["test"]})
    if from_cli and "interfaz-como-libreria" not in debts:
        for consumer, symbol in from_cli:
            problems.append(f"{consumer} importa `{symbol}` de la interfaz "
                            f"desde código de producción")

    undeclared = sorted(s for s in asked
                        if s not in known and not s.startswith("_"))
    if undeclared and "sin-nombre-publico" not in debts:
        for symbol in undeclared:
            users = {h["consumer"] for h in asked[symbol]}
            problems.append(f"`{symbol}` lo piden {', '.join(sorted(users))} "
                            f"y ninguna puerta lo declara")

    total = surface["symbols_requested"]
    if len(asked) != total:
        problems.append(f"el contrato dice {total} símbolos pedidos; "
                        f"los consumidores piden {len(asked)}")

    for problem in problems:
        print(f"  ERROR  {problem}")

    print(f"  nota   {len(present)} de {len(consumers)} consumidores presentes: "
          f"{', '.join(present)}")
    if private:
        print(f"  deuda  {len(private)} privados importados desde fuera: "
              f"{', '.join(private)}")
    if from_cli:
        print(f"  deuda  {len(from_cli)} imports de la interfaz desde código "
              f"de producción")
    if undeclared:
        print(f"  deuda  {len(undeclared)} símbolos pedidos sin puerta que los declare")
    print(f"{'FAIL' if problems else 'PASS'}: superficie — "
          f"{len(asked)} símbolos pedidos, {len(known)} declarados, "
          f"{len(problems)} violaciones")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
