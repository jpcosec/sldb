# Disposición GO03 (ronda 1)

- 1 corregido: GO03 depende ahora de GO02, que fija la firma eval(predicado, sujeto) → findings {node, holds, clause, seen}; aceptación prueba eval con has(id).
- 2 corregido: clave graph_backend en store.yaml, ausente = networkx, inválida = error con lista; en la aceptación.
- 3 corregido: los seis comandos graph y api/graph se enrutan por el backend; output_scope ampliado a api/graph y cli/parsers/graph_analysis.py.

Estado: input corregido; requiere nueva revisión (ronda 2) sobre el input nuevo.
