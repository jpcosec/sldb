# T2 · Parte A del handoff: `/document/segments` en SLDB

Estado: en curso (worker `pi2`) · Worktree: `hum-ecosystem-worktrees/sldb-segments`
Worktree: `/home/jp/proyectos/hum-ecosystem-worktrees/sldb-segments`

## Qué
Render instrumentado con `SpanRecorder` como dependencia explícita, decodificador
de centinelas, árbol de segmentos, `sldb.api.build_document_segments`, ruta
`GET /document/segments`.

Referencia: `sldb-surface/HANDOFF-sldb-segments.md` §Parte A.

## Listo cuando
- Invariante: texto decodificado == `render_model_markdown` byte a byte en todo el store
- Baseline verde
- Se puede apagar `dev/reference_server.py` y apuntar la UI a `sldb serve`
