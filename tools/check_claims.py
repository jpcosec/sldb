#!/usr/bin/env python3
"""Puerta de afirmaciones: lo que la documentación dice sobre el código es cierto.

Un documento que nombra un archivo, un paquete o una cifra está afirmando algo
verificable. Cuando el código cambia, la afirmación se vuelve falsa y el
documento conserva su autoridad mientras miente — y eso es peor que no tenerlo,
porque alguien va a confiar en él.

Esta puerta recorre los documentos, extrae las afirmaciones comprobables y las
comprueba. No juzga prosa: solo lo que se puede refutar mecánicamente.

Qué rechaza:

- una ruta de archivo o directorio que ya no existe
- una referencia a `sldb.<paquete>` que no es un paquete
- un bloque de comando que invoca un subcomando inexistente
- una cifra marcada como verificable que no coincide

Qué no ve: si la prosa describe bien el comportamiento. Eso no es mecanizable y
queda para la revisión humana; esta puerta solo garantiza que las referencias
apunten a algo real.

    python tools/check_claims.py
    python tools/check_claims.py docs/architecture   # un subconjunto
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: Rutas en línea: `src/sldb/core/renderer.py`, `docs/faq.md`, con línea opcional.
PATH_REF = re.compile(r"`((?:src|docs|tests|tools|scripts|contracts)/[\w./-]+?)(?:#L\d+(?:-L?\d+)?)?`")

#: Referencias a paquetes: `sldb.store`, `sldb.core.renderer`.
MODULE_REF = re.compile(r"`(sldb\.[a-z_][\w.]*)`")

#: Invocaciones de la línea de comandos. Solo dentro de código — en bloques
#: cercados o entre comillas simples — porque en prosa «sldb can do X» no es una
#: invocación y tratarla como tal produce ruido que entierra los hallazgos reales.
#: Anclado a inicio de línea: sin eso, un `--store .sldb` al final de una línea
#: se lee como si `.sldb` iniciara una invocación nueva, y el comando siguiente
#: resulta ser `sldb`. Es el tipo de falso positivo que desacredita una puerta.
COMMAND = re.compile(
    r"^\s*(?:\$\s*)?(?:python3? -m sldb|sldb)\s+([a-z][a-z-]*)(?:\s+([a-z][a-z-]*))?",
    re.M)
CODE_SPAN = re.compile(r"`([^`\n]+)`")
CODE_BLOCK = re.compile(r"```[a-z]*\n(.*?)```", re.S)

#: Una cifra que el autor marcó como verificable: `<!-- verify: 586 archivos -->`
#: seguido del comando que la produce.
VERIFY = re.compile(r"<!--\s*verify:\s*(.+?)\s*=\s*(.+?)\s*-->")

#: Carpetas que no se auditan: lo generado se regenera, y los ejemplos contienen
#: rutas ficticias a propósito.
SKIP = {"build", "dist", "__pycache__", ".git", "node_modules", "runs"}

#: Una referencia marcada como inexistente a propósito. Un diagnóstico necesita
#: citar lo que está roto, y sin esta marca la puerta reporta como defecto cada
#: ejemplo de defecto — volviendo imposible documentar un hallazgo.
#:
#:     `src/nldb/` <!-- gone -->
#:
#: Un bloque cercado se marca entero con `<!-- gone -->` sola en la línea anterior.
GONE = re.compile(r"<!--\s*gone\s*-->")


def marked_gone(text: str, position: int) -> bool:
    """Si la referencia que termina en `position` lleva la marca de inexistente.

    La marca vale para el resto de la línea, de modo que una tabla puede marcar
    varias referencias de una fila sin repetirla en cada celda.
    """
    line_end = text.find("\n", position)
    line_start = text.rfind("\n", 0, position) + 1
    return bool(GONE.search(text[line_start:line_end if line_end != -1 else len(text)]))


def block_marked_gone(text: str, position: int) -> bool:
    """Si el bloque cercado que abre en `position` lleva la marca en la línea anterior.

    La marca no cabe en la línea de apertura sin romper el cercado, y una propuesta
    cita comandos que todavía no existen en bloques enteros.
    """
    line_start = text.rfind("\n", 0, position) + 1
    previous = text[text.rfind("\n", 0, max(line_start - 1, 0)) + 1:line_start]
    return marked_gone(text, position) or bool(GONE.fullmatch(previous.strip()))


def subcommands() -> set[tuple[str, ...]]:
    """Los comandos que la interfaz acepta, leídos de su propio analizador.

    Se le pregunta a la estructura, no al texto de ayuda: raspar `--help` deja
    fuera lo que no encaje con el formato de impresión, y un detector que falla
    en silencio marca como falsas afirmaciones que eran verdaderas.

    Devuelve tuplas, de modo que `('docs',)` y `('docs', 'track')` se distinguen
    y un documento que invoca un subcomando de segundo nivel inexistente se
    atrapa igual.
    """
    script = (
        "import argparse, json, sys;"
        "sys.path.insert(0, 'src');"
        "from sldb.cli.parsers.core import build_parser;"
        "out=[];"
        "\ndef walk(parser, prefix):\n"
        "    for action in parser._actions:\n"
        "        if isinstance(action, argparse._SubParsersAction):\n"
        "            for name, sub in action.choices.items():\n"
        "                out.append(prefix + [name]); walk(sub, prefix + [name])\n"
        "walk(build_parser(), []);"
        "print(json.dumps(out))"
    )
    try:
        done = subprocess.run([sys.executable, "-c", script], cwd=ROOT,
                              capture_output=True, text=True, timeout=120)
        import json
        return {tuple(path) for path in json.loads(done.stdout)}
    except Exception as exc:
        print(f"  aviso  no se pudo leer el analizador de la interfaz: "
              f"{str(exc).splitlines()[0][:70]}")
        print("  aviso  las invocaciones de comandos no se comprueban en esta corrida")
        return set()


def packages() -> set[str]:
    """Los módulos importables, por nombre completo."""
    names = set()
    for path in (ROOT / "src" / "sldb").rglob("*.py"):
        rel = path.relative_to(ROOT / "src").with_suffix("")
        parts = [p for p in rel.parts if p != "__init__"]
        for i in range(1, len(parts) + 1):
            names.add(".".join(parts[:i]))
    return names


def resolves(ref: str, known: set[str]) -> bool:
    """Si la referencia apunta a algo real.

    Una cita suele incluir lo que se importa del módulo — `sldb.api.x.find_doc`
    o `sldb.api.y.MyClass` — y también aparece con la extensión `.py`. Las tres
    formas son correctas y hay que aceptarlas, o la puerta reporta como falso lo
    que el autor escribió bien.
    """
    if ref in known or ref.removesuffix(".py") in known:
        return True
    # El prefijo más largo que sea un módulo: lo que sobra es el nombre importado.
    parts = ref.split(".")
    return any(".".join(parts[:i]) in known for i in range(len(parts), 1, -1))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=None,
                        help="archivos o carpetas a auditar (por omisión: docs/ y la raíz)")
    args = parser.parse_args()

    targets: list[Path] = []
    for raw in (args.paths or ["docs", "README.md", "standards.md", "CHANGELOG.md"]):
        path = ROOT / raw
        if path.is_dir():
            targets += [p for p in sorted(path.rglob("*.md"))
                        if not SKIP & set(p.relative_to(ROOT).parts)]
        elif path.is_file():
            targets.append(path)

    known_pkgs, known_cmds = packages(), subcommands()
    problems: list[str] = []
    counted = 0

    for doc in targets:
        text = doc.read_text(encoding="utf-8", errors="ignore")
        where = doc.relative_to(ROOT)

        for match in PATH_REF.finditer(text):
            counted += 1
            ref = match.group(1)
            if not (ROOT / ref).exists() and not marked_gone(text, match.start()):
                problems.append(f"{where}: la ruta `{ref}` no existe")

        for match in MODULE_REF.finditer(text):
            counted += 1
            ref = match.group(1)
            if resolves(ref, known_pkgs) or marked_gone(text, match.start()):
                continue
            problems.append(f"{where}: el módulo `{ref}` no existe")

        if known_cmds:
            tops = {path[0] for path in known_cmds}
            # Un comando que no abre subcomandos recibe argumentos libres, y esos
            # no se comprueban contra nada: `find type.x.y` pasa un término de
            # búsqueda, no un subcomando.
            leaves = {c for c in tops if not any(
                len(p) > 1 and p[0] == c for p in known_cmds)}
            spans = [(m.group(1), m.start(), marked_gone) for m in CODE_SPAN.finditer(text)]
            spans += [(m.group(1), m.start(), block_marked_gone) for m in CODE_BLOCK.finditer(text)]
            for snippet, at, gone in spans:
                for cmd, sub in set(COMMAND.findall(snippet)):
                    counted += 1
                    if gone(text, at):
                        continue
                    if cmd not in tops:
                        problems.append(
                            f"{where}: el comando `sldb {cmd}` no existe")
                    elif sub and cmd not in leaves and (cmd, sub) not in known_cmds:
                        problems.append(
                            f"{where}: `sldb {cmd}` existe pero no acepta `{sub}`")

        for label, command in VERIFY.findall(text):
            counted += 1
            got = subprocess.run(command, shell=True, capture_output=True,
                                 text=True, cwd=ROOT).stdout.strip()
            if got != label.strip():
                problems.append(
                    f"{where}: la cifra «{label}» ya no es cierta (ahora: «{got}»)")

    for problem in problems:
        print(f"  ERROR  {problem}")
    print(f"{'FAIL' if problems else 'PASS'}: afirmaciones — "
          f"{len(targets)} documentos, {counted} afirmaciones comprobadas, "
          f"{len(problems)} falsas")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
