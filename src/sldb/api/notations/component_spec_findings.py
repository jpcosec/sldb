"""The findings the component spec generators report, in sldb's format (level, code, subject, what, fix)."""

from __future__ import annotations

from pathlib import Path

from sldb.api.notations.component_spec_constants import GraphEdges, GraphNodes
from sldb.core.finding import Finding, alert

CODE_EXTRA = "pip install 'structuredLanguageDB[code]'"


def code_extra_missing(src_dir: str | Path) -> Finding:
    """Sin el extra opcional `[code]` no hay escaner de Python: no se genera ni se escribe nada."""
    return alert("component-spec/code-extra-missing", str(src_dir), "no hay tree-sitter", CODE_EXTRA)


def syntax_error(path: str) -> Finding:
    """Archivo no analizable: queda su modulo, sin clases ni imports (como en spec2viz)."""
    return alert("component-spec/syntax-error", path, "archivo no analizable: el modulo queda sin clases ni imports", "corregir la sintaxis del archivo")


def dangling_edges(nodes: GraphNodes, edges: GraphEdges) -> list[Finding]:
    """Una alerta por arista con un extremo que no es nodo del grafo: el spec la descarta."""
    return [
        alert("component-spec/dangling-edge", f"{source} -> {target}", f"arista {relation or '-'} con un extremo fuera del grafo: descartada",
              "agregar el nodo que falta al grafo o quitar la arista")
        for source, target, relation in edges
        if source not in nodes or target not in nodes
    ]
