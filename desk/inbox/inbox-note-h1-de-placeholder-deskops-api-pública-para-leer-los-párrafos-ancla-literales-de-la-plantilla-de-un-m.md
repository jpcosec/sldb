---
sldb:
  by: agent
  at: '2026-11-12T00:36:42Z'
  authority: generated
  via: create_document
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-12T00:36:39'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# H1 de placeholder (deskops): API pública para leer los párrafos ancla literales de la plantilla de un modelo

_Describe the incoming message with enough evidence to triage._

Origen: task.debug de deskops 'edit no guarda el párrafo placeholder de la plantilla como contenido' (rama wt/placeholder-r, informe placeholder-worker-report.md en deskops). Para no guardar como contenido el párrafo placeholder que la plantilla escribe antes de un campo (por ejemplo '_Outline the expected implementation route or affected surface._' antes de implementation_path), deskops necesita saber qué párrafo literal ancla cada campo. Hoy lo saca con internos de sldb: AST_Handler().split_nodes sobre model.__template__ y TemplateExtractor().extract_nodes, recorriendo las recetas (outer_type paragraph, anchor, props). Propuesta: una función pública en sldb.api que, dado un modelo, devuelva por campo el texto del párrafo ancla literal que extract consume y render escribe; o que el render/save de sldb descarte por su cuenta un valor de campo cuyo párrafo coincide con su propia ancla, para que ningún consumidor tenga que hacerlo. Decide sldb.
