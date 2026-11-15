---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T19:20:54'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb notations: validar una notación, una paleta o un spec por nombre o ruta desde la CLI

_Describe the incoming message with enough evidence to triage._

La matriz de cobertura de spec2viz (IR 456b862, docs/spec2viz/matriz-de-cobertura.md) deja en modo 'usar sldb directamente' la validación de notaciones y paletas (spec2viz notation validate / palette validate, con el contraste WCAG) y en 'migrado a sldb' la validación de specs (load_spec/validate_spec, D3). sldb no tiene hoy un comando que valide una notación, una paleta o un spec por nombre o ruta. Pedido: 'sldb notations validate <nombre|ruta>' (notación, paleta y spec por tipo), con hallazgos en el formato de findings de sldb. Además, como IR13c se retiró, nadie porta a sldb las pruebas de spec2viz de notaciones, paletas, vista resuelta y ViewDoc: conviene una tarea en sldb que las porte.
