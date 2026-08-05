#!/usr/bin/env python3
"""Genera docs/architecture/sldb_Kernel_Vistas_UML.html.

Fuentes (diagram-traceability-contract):
  - docs/architecture/vistas/template.html
  - docs/architecture/vistas/vistas.yml   (registry)
  - docs/architecture/vistas/*.mmd        (fuentes Mermaid)

El HTML es un artefacto GENERADO. No editarlo a mano.
"""
import sys
from pathlib import Path

import yaml

ARCH = Path(__file__).resolve().parent.parent / "docs" / "architecture"


def render(arch: Path = ARCH) -> str:
    reg = yaml.safe_load((arch / "vistas" / "vistas.yml").read_text())
    tpl = (arch / reg["template"]).read_text()

    nav = "\n".join(f'  <a href="#{v["id"]}">{v["nav"]}</a>' for v in reg["vistas"])

    sections = []
    for v in reg["vistas"]:
        mmd = (arch / v["mmd"]).read_text().strip()
        attrs = ""
        if v["specs"]:
            attrs += " " + " ".join(f'data-spec="{s}"' for s in v["specs"])
        if v["puml"]:
            attrs += f' data-puml="{v["puml"]}"'
        indented = "\n".join("      " + line for line in mmd.splitlines())
        sections.append(
            f'''<section id="{v["id"]}"{attrs}>
  <div class="lbl">{v["lbl"]}</div>
  <h2>{v["title"]}</h2>
  <p class="desc">{v["desc"]}</p>
  <div class="board">
    <div class="mermaid">
{indented}
    </div>
  </div>
</section>'''
        )

    return tpl.replace("{{NAV}}", nav).replace("{{SECTIONS}}", "\n\n".join(sections))


def main() -> int:
    out = ARCH / "sldb_Kernel_Vistas_UML.html"
    out.write_text(render())
    print(f"generado: {out} ({len(render())} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
