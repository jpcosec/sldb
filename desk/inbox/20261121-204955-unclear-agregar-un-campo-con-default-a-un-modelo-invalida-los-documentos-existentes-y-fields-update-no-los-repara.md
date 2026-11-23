---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: minegocio
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-21T20:49:55'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# Agregar un campo con default a un modelo invalida los documentos existentes y fields update no los repara

_Describe the incoming message with enough evidence to triage._

Caso (minegocio, 2026-11-21): a un StructuredNLDoc ya registrado se le agrego un campo de frontmatter con valor por defecto (espera_segundos: int = 4, con su marcador rev en __template__). Esperado: los documentos existentes, que no tienen la clave, siguen validos tomando el default del modelo, o hay un comando que migra. Real: quedan store/doc-invalid ('espera_segundos: Input should be a valid integer', input None) y 'sldb fields update docs/asistente/espera_segundos 4' falla con el mismo error porque valida el documento antes de escribir. La unica salida fue editar el Markdown a mano y correr 'sldb stores update'. Afectados: AsistenteDoc en negocios/*/wiki/asistente.md de /home/jp/proyectos/WebProjects/minegocio. Pedido: que una clave ausente tome el default del modelo al leer, o un comando de migracion que escriba el default en los documentos existentes.
