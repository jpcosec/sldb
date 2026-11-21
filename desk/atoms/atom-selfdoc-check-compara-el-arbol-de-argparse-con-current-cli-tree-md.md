---
sldb:
  by: agent
  at: '2026-11-21T10:20:02Z'
  authority: generated
  via: create_document
id: atom-selfdoc-check-compara-el-arbol-de-argparse-con-current-cli-tree-md
title: selfdoc check compara el árbol de argparse con current-cli-tree.md
five_wh_one_plus: how
tags:
- system:sldb
- topic:selfdoc
---

# selfdoc check compara el árbol de argparse con current-cli-tree.md

## Answer

sldb selfdoc check recorre el árbol de argparse del CLI y lo compara con current-cli-tree.md: un subcomando o grupo que falta en la doc da cli_tree_missing y uno que la doc nombra pero el CLI ya no tiene da cli_tree_stale, los dos errores que ponen ok en falso (b8e564c2; src/sldb/selfdoc/cli_tree.py, report.py, report_findings.py). El tester dio FALLA solo por la puerta 'identidad' por workbench_demo, la excepción autorizada (f055723d).
