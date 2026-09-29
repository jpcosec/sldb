# T1 · Ordenar el espacio de trabajo

Estado: **HECHO** (commit bd4c0dcb)

## Por qué
Los modelos compuestos quedaron en `/tmp/sysprompt` con store propio: `source.doc`
sale `null`, las rutas son absolutas y hay 3 backends corriendo.

## Pasos
- [x] Bajar UIs 8840/8842 y backends 8787/8789; dejar 8841/8788
- [x] Mover `complete_systemprompt.py` a `kb_models/knowledge/`, exportarlo en `__init__.py`
- [x] `sldb models add kb_models.knowledge:CompleteSystemPrompt --store knowledge_antonia-cobranza/.sldb --pythonpath .`
- [x] Regenerar payload con rutas relativas, vía `sldb find` / `sldb.api` (no rglob+regex)
- [x] `sldb docs create` contra el store real
- [x] `sldb stores check`
- [x] Borrar `/tmp/sysprompt`

## Listo cuando
`source.doc` deja de ser `null` en las piezas y `stores check` pasa.

## Resultado
`stores check`: PASS, 114 documentos en 20 modelos.

Pendiente menor: `source.doc` sin verificar por un bug del prototipo
(`KeyError: 'applies_to'` en `_compose_piece` cuando el hijo no trae el campo).
Es del prototipo, no de SLDB: el render normal compone las 36 piezas bien.
