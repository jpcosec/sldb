# T2 · Parte A del handoff: `/document/segments` en SLDB

Estado: **HECHO** · Worktree: `hum-ecosystem-worktrees/sldb-segments`
Worktree: `/home/jp/proyectos/hum-ecosystem-worktrees/sldb-segments`
Commit: `74285b5` — "segments: GET /document/segments real, por render instrumentado"

## Qué
Render instrumentado con `SpanRecorder` como dependencia explícita, decodificador
de centinelas, árbol de segmentos, `sldb.api.build_document_segments`, ruta
`GET /document/segments`.

Referencia: `sldb-surface/HANDOFF-sldb-segments.md` §Parte A.

## Resultado
Suite completa: 1099 passed.

Verificado contra el store real:
- `/document/segments` responde 200 para `domain-cobranza-datos` (16 segmentos) y para
  `complete-systemprompt` (56 segmentos). Este último es el caso que hacía reventar el
  monkey-patch anterior con `KeyError: 'applies_to'`.
- Los segmentos concatenados reconstruyen el texto EXACTO (1174 y 2394 chars) y cada
  offset `start`/`end` coincide con el texto real.

Se implementó instrumentando el renderer con centinelas, no parseando de nuevo.

## Paso que queda
Borrar el monkey-patch externo (`dev/reference_server.py` / `segments_prototype.py`).
