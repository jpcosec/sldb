---
id: atom-el-inventario-de-código-de-sldb-se-publica-como-hechos-de-fuente-y-cada-consumidor-los-proyecta
title: El inventario de código de sldb se publica como hechos de fuente, y cada consumidor
  los proyecta
five_wh_one_plus: how
tags:
- system:sldb
- topic:selfdoc
provenance: docs/architecture/code-docstring-indexing.spec.md
---

# El inventario de código de sldb se publica como hechos de fuente, y cada consumidor los proyecta

## Answer

sldb selfdoc escanea su propio código sin importarlo. Hay dos salidas: documentos PythonSymbolDoc y CliCommandDoc trackeados en el store (knowledge/), y un grafo de fuente regenerable (.sldb/runtime/graphs/python-source.graph.json) con contains, imports (siguiendo re-exports, con via) y references, con su evidencia. La metadata de un docstring (id, kind, tags) se lee estricta y sus errores frenan la escritura; los tags se heredan por la cadena léxica con su origen. python-check dice si todo está al día. Un consumidor proyecta esos hechos sin reinterpretarlos: spec2viz diagram from-graph --module-prefix … arma un diagrama válido. Spec: docs/architecture/code-docstring-indexing.spec.md.
