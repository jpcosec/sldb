---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-01T03:12:23'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-01T23:33:24'
---

# Pills con placeholders del template encima de contenido real

_Describe the incoming message with enough evidence to triage._

Una pasada de deskops (2026-09-30 10:52) metió los seis placeholders en cursiva del template de pill (_Define the context..._, _Explain why..._, etc.) dentro de los 14 pills de desk/pills/, debajo de cada heading y encima del texto que ya tenían. Están sin commitear junto con la reindexación (.sldb/core/documents/PillDoc/*.yaml, PillDoc.yaml, store_index.yaml). Decidir: revertir (git checkout -- desk/pills .sldb/core) o commitear aparte. El arreglo de fondo es en deskops: la normalización al template debe saltarse secciones que ya tienen texto.
