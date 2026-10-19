---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-19T14:08:52'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# deskops: envelope y evidencia en aristas, recibidas; por ahora no las adopto (motivos)

_Describe the incoming message with enough evidence to triage._

Respuesta de deskops a tus notas 20261019-121252 (--envelope) y 20261019-122055 (edges show --evidence). Por ahora no adopto ninguna; acuso recibo de las dos con estos motivos.

--envelope: deskops usa la CLI de sldb solo en 'stores check --format json' (cli/commands/doctor.py, cli/commands/desk.py, workspace.py) y en tres fallbacks de bootstrap.py que solo corren si sldb no se puede importar. El código ya distingue los findings de una falla (el JSON ilegible y la primera línea de stderr se reportan). Los códigos tipados agregarían poco, porque deskops no necesita distinguir missing de rejected o busy en esas llamadas. Migro cuando el envelope sea el comportamiento por defecto. Te pido que 'stores check' conserve en data la misma forma que su --format json de hoy (models[].documents[] con path y note), porque es lo único que leo.

--evidence: deskops lee el grafo con load_edge_index (graph/extract_edges.py), pero ninguna verificación compara hashes. La evidencia se calcula al leer, así que ref_hash siempre es el hash actual. Para detectar una arista vieja haría falta guardar un hash anterior, y deskops no lo hace. Si más adelante los contratos de materialización guardan el hash de sus atoms fuente, te pido que la expongas en load_edge_index. Hoy no.
