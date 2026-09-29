# T8 · Identidad de sección e id como hoja de ruta semántica

Estado: pendiente · Dificultad: alta · Bloqueada por diseño

## Dos caras del mismo problema
- **H1**: las secciones se direccionan por slug jerárquico posicional; headings
  repetidos reciben sufijo `-2`; no hay id estable no-posicional ni `sections move`.
- **Id de atom**: `domain/domain-cobranza-canal.md` repite lo que ya dice el tag
  `domain:cobranza.canal`. Propuesta §17.

## Antes de diseñar
Revisar la rama `refactor-target` de SLDB: merkle, anchor states, stand-off
addressing, reconciliación ante drift.
