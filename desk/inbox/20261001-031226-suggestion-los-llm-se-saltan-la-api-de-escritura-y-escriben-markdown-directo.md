---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-01T03:12:26'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Los LLM se saltan la API de escritura y escriben Markdown directo

_Describe the incoming message with enough evidence to triage._

Diagnóstico: el render es demasiado natural, parece la cosa y no una proyección; escribirlo cuesta una llamada y la API cuesta descubrimiento sin dar nada visible a cambio; el archivo no se queja y la divergencia aparece después en stores check. Cambiar la economía, no las instrucciones: (a) hook PreToolUse sobre Write/Edit que bloquee rutas trackeadas por el store y escriba en el error el comando correcto; (b) sldb docs register <ruta> o POST /docs con markdown que extraiga, valide, rechace ruido estructural, indexe y devuelva el render canónico con diff (el invariante es nada entra sin pasar por extract→render, no nadie escribe Markdown); (c) CLAUDE.md en la raíz y la skill de src/sldb/assets/skills/sldb.md cargándose sola cuando hay .sldb/, como deskops-workflow con desk/. Orden: hook, luego register.

## Avance (2026-10-18)

Sigue abierta: no hay hook PreToolUse ni `docs register`. `POST /docs` (4c3c2e0e) existe, pero recibe un payload JSON, no markdown, y no devuelve el render ni el diff.
