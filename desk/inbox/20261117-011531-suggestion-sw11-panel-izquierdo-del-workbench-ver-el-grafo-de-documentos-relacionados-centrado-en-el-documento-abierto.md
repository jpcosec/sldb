---
sldb:
  by: agent
  at: '2026-11-17T05:15:06Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T01:15:31'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T02:14:08'
---

# SW11 · Panel izquierdo del Workbench: ver el grafo de documentos relacionados, centrado en el documento abierto.

_Describe the incoming message with enough evidence to triage._

Qué pasa hoy: el panel dibuja el documento como ROOT y, a la derecha, solo sus piezas compuestas y las referencias que encuentra en el payload. Con documentos que no componen nada (una nota del inbox, un tipo de relación) queda un nodo ROOT solo en un panel de 560 x 640 px. No se ven los documentos que apuntan a este ni sus vecinos.
Qué pide: un grafo con el documento abierto al centro y los documentos relacionados alrededor (lo que referencia y lo que lo referencia), navegable.
Hallazgos a confirmar primero, porque condicionan todo lo demás: (1) el componente ya recibe edges de GET /edges?id= (prop edges; lo usa para el contador de backlinks, :232). En los dos stores locales probados (UIs/graph_ui y workbench_demo) GET /edges?id=<doc> devolvió {"edges": []} y GET /graph/neighborhood?node=<doc>&depth=1 devolvió solo el propio nodo, para una tarea, un átomo, un RelationTypeDoc y el informe Levira, aunque .sldb_cache/edges existe en ambos. No determiné si el id va en otro formato, si el índice de aristas está sin construir o si es un defecto de serve: es lo primero que hay que averiguar, y si es de sldb serve va como tarea aparte. (2) Los hijos del árbol salen de parsear referencias del payload en la UI (parseRefString y el recorrido de data.payload, TopologyMindmap.tsx:31-46 y :195-225). Eso es calcular en la UI lo que sldb sabe: el grafo nuevo debe salir de lo que entrega sldb (/edges, /graph/neighborhood), no de más parseo local.
Referencia: el Workspace de graph_ui ya tiene una proyección "Grafo Local" de 1 y 2 saltos (UIs/graph_ui/frontends/mindmap/views/workspace/node/). Sirve para ver el comportamiento esperado; no se copia código entre repos.
Puntos a resolver en el contrato: cuántos saltos (1 y 2 como en graph_ui); cómo conviven el árbol de composición actual y el grafo (lente, pestaña o un solo dibujo); qué se muestra cuando sldb no entrega relaciones (decirlo, no dejar el panel vacío); tope de nodos para documentos muy referenciados.
done_when sugerido: con un documento que tiene relaciones entrantes y salientes en un store real, el panel muestra ambas con el documento al centro y un clic en un vecino lo abre; con uno sin relaciones lo dice; ningún vecino sale de parseo en la UI.
Toca TopologyMindmap.tsx: en serie con SW3.

Origen: comentario que JP dejó sobre la propia interfaz al recorrer el Workbench de sldb/surface (2026-11-17, vía la sesión supervisora local, con el store real de UIs/graph_ui servido por sldb serve). Instrucción de JP: cada comentario se registra como tarea, no se resuelve en el momento. Base de código: df3903db en origin/main de sldb. Contexto de producto: el Workbench es LA UI de SLDB, general y autónoma (corrección de JP del mismo día); principios firmes: papel con fierros ocultables, toda escritura tiene nombre, la UI no calcula. Va en la cola después de la serie SW1-SW9, salvo que JP diga otra cosa. La evidencia viene de lectura del código y de consultas a sldb serve local; confirmar cada punto antes de escribir el TaskDoc.
