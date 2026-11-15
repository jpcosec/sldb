---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T02:24:46'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# [specIR] anclas de código para TSX y SQL

_Describe the incoming message with enough evidence to triage._

Necesidad: specIR ancla cada nodo extraído a su fuente con las anclas de código de SLDB (decisión IR05 D3, docs/decisiones/procedencia-y-divergencia.md en IR, JP 2026-11-15): from code:<ruta>::<símbolo> + CodeAnchorDoc vía sldb.api.anchors.record_anchor/check_anchors. Los extractores de specIR leerán Django (Python, cubierto), SQL (DDL/migraciones) y React TSX/TS. Revisado en sldb a3514755: src/sldb/code/scan.py recorre solo archivos .py con tree-sitter-python (extra [code]); no hay gramática ni normalización de fingerprints para TypeScript/TSX ni SQL (el typescript_scanner de kgdb está en el árbol muerto según docs/architecture/superseded-code-audit.md). Pedido: extender el escáner y record_anchor/check_anchors a TS/TSX (componentes, funciones, hooks, tipos) y a SQL (tablas, columnas, vistas), con la misma referencia code:<ruta>::<qualified_name>, fingerprints por nodo, estados y reconexión; idealmente con gramáticas tree-sitter como extras opcionales. Mientras tanto specIR marca esos nodos con verificacion sin_verificar y la ancla en desconocidos. Es una carencia nueva: la matriz de IR01 (docs/auditoria/sldb-api-frente-a-mcp.md) no tiene fila para anclar fuera de Python. TaskDoc: task-ir05-decisión-procedencia-y-divergencia-entre-código-y-modelo
