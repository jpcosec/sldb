---
sldb:
  by: agent
  at: '2026-11-16T08:23:21Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T20:34:56'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:23:05'
---

# code/scan-tree-nested-imports: component_spec_from_python no ve los from-imports anidados

_Describe the incoming message with enough evidence to triage._

Desde IR13a (paridad de D2 con spec2viz sobre un paquete real, src/specir de IR, y también sobre spec2viz/spec2viz y sldb/src/sldb/api): component_spec_from_python lee los imports de sldb.code.scan_tree (attrs.imports), que solo trae las sentencias del nivel superior del módulo. generate_python_ast_spec de spec2viz recorría todo el árbol (ast.walk), así que también veía los 'from x import y' dentro de funciones, if o try (imports perezosos, TYPE_CHECKING). Ejemplo en IR: specir/visual/commands.py importa specir.visual.compilers y specir.visual.lint_mermaid dentro de funciones y esas aristas imports faltan en el spec de sldb. Es una dependencia real que el diagrama pierde. Pedido: que scan_tree registre también los imports anidados (marcados como tales si hace falta) y que component_spec_from_python los emita, o declarar la pérdida como decisión. Las otras diferencias con spec2viz (cuenta 'import x', resuelve relativos, no repite aristas) son mejoras y IR las declaró en la matriz (SV-F02). Prueba en IR: tests/visual/test_sync_generation_parity.py::test_python_ast_generation_of_specir_matches_spec2viz_up_to_the_declared_differences.
