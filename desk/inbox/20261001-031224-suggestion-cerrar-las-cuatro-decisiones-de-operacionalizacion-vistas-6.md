---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-01T03:12:24'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Cerrar las cuatro decisiones de OPERACIONALIZACION-VISTAS §6

_Describe the incoming message with enough evidence to triage._

Tomarlas como decididas según su recomendación y llevarlas a código: (1) offsets del ancla sobre el campo body del átomo, no sobre el render canónico (requiere source_field); (2) valor descartado en status, no borrar; (3) prosa generada con marca generado y hash de los átomos de origen, desactualizada si el hash cambia, nunca reescrita sola; (4) extractor externo a la UI y a /extract/segments que escribe AtomDoc con status propuesto y nunca toca confirmado. Conviene hacerlo después de fijar el set bootstrap porque las cuatro tocan AtomDoc.

## Avance (2026-10-18)

(1) `source_field` (default `body`) y (2) `descartado` en `status` ya están en surface/dev/atoms-store/models.py y en levira-store (152fc723). Faltan (3) la prosa generada con marca y hash de los átomos de origen y (4) el extractor externo; quedan bloqueadas por 20261001-031225 (átomo y field).
