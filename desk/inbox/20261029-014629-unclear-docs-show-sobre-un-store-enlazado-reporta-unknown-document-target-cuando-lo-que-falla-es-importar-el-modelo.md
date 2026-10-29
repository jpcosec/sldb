---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-29T01:46:29'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# docs show sobre un store enlazado reporta 'Unknown document target' cuando lo que falla es importar el modelo

_Describe the incoming message with enough evidence to triage._

Desde el store central de deskops (links a ../sldb/.sldb), 'sldb docs show sldb:ArchitectureNarrativeDoc/arch-code-docstring-indexing --store .sldb' responde 'Unknown document target' mientras 'sldb docs exists' con el mismo target responde ok. La causa real es que el modelo del store enlazado (docs.models:ArchitectureNarrativeDoc, path docs/models.py relativo a la raíz de sldb) no se puede importar sin --pythonpath ../sldb; con --pythonpath ../sldb el show funciona. El error de import se traga y se reporta como target desconocido: eso es una alerta silenciosa. Esperado: (a) el mensaje distingue 'documento no existe' de 'no pude importar el modelo X del store enlazado Y (pythonpath?)', y (b) idealmente el store enlazado aporta su propio pythonpath (la raíz del proyecto del link) sin que el llamador lo adivine. Reproducción 2026-10-29: cd deskops && sldb docs show 'sldb:ArchitectureNarrativeDoc/arch-code-docstring-indexing' --store .sldb
