# T1 · Ordenar el espacio de trabajo

Estado: pendiente · Bloquea: T3, T4

## Por qué
Los modelos compuestos quedaron en `/tmp/sysprompt` con store propio: `source.doc`
sale `null`, las rutas son absolutas y hay 3 backends corriendo.

## Pasos
- [ ] Bajar UIs 8840/8842 y backends 8787/8789; dejar 8841/8788
- [ ] Mover `complete_systemprompt.py` a `kb_models/knowledge/`, exportarlo en `__init__.py`
- [ ] `sldb models add kb_models.knowledge:CompleteSystemPrompt --store knowledge_antonia-cobranza/.sldb --pythonpath .`
- [ ] Regenerar payload con rutas relativas, vía `sldb find` / `sldb.api` (no rglob+regex)
- [ ] `sldb docs create` contra el store real
- [ ] `sldb stores check`
- [ ] Borrar `/tmp/sysprompt`

## Listo cuando
`source.doc` deja de ser `null` en las piezas y `stores check` pasa.
