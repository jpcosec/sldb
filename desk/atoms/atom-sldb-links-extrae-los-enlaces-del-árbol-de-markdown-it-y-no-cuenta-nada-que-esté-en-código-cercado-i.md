---
sldb:
  by: agent
  at: '2026-11-17T16:32:34Z'
  authority: generated
  via: create_document
id: atom-sldb-links-extrae-los-enlaces-del-árbol-de-markdown-it-y-no-cuenta-nada-que-esté-en-código-cercado-i
title: sldb links extrae los enlaces del árbol de markdown-it y no cuenta nada que
  esté en código cercado, indentado o en línea
five_wh_one_plus: what
tags:
- system:sldb
- topic:links
provenance: tarea del scan de enlaces (pedido de sldb-ui); intento markdown-it, ejecutores
  deskops-e-2793fe94705d(-a2) y deskops-e-f8f7d079d2e1, tester PASA en runs/subagents/20261116-test-lk-md-c2
---

# sldb links extrae los enlaces del árbol de markdown-it y no cuenta nada que esté en código cercado, indentado o en línea

## Answer

parse_links (src/sldb/links/parser.py) corre sus dos regex de siempre sobre scannable_text (src/sldb/links/scan_text.py), que parsea el documento con el markdown-it de sldb.core.ast (gfm-like con front matter, text_join y linkify apagados, una instancia por proceso) y deja fuera los tokens fence, code_block y code_inline. Front matter y html_block se leen crudos desde sus líneas fuente, cortadas como markdown-it (\r\n, \r, \n). El orden de salida y ParsedLink no cambian. Decisión del supervisor del 2026-11-17: no reconocer Markdown con reglas propias.
