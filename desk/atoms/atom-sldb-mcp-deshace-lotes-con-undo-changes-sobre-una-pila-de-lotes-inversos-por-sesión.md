---
sldb:
  by: agent
  at: '2026-11-17T12:12:04Z'
  authority: generated
  via: create_document
id: atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión
title: sldb mcp deshace lotes con undo_changes sobre una pila de lotes inversos por
  sesión
five_wh_one_plus: what
tags:
- system:sldb
- topic:mcp
provenance: tarea undo_changes (nota de IR 184421, IR04b); ejecutor deskops-e-7015d1ec50ff,
  tester PASA en runs/subagents/20261116-test-undo
---

# sldb mcp deshace lotes con undo_changes sobre una pila de lotes inversos por sesión

## Answer

Cada apply_changes exitoso de sldb mcp apila su BatchReport.inverse en una pila de la sesión del servidor, en memoria y sin persistir. undo_changes(steps=1) aplica los inversos del más reciente al más antiguo con apply_batch y sus guardas: si alguien escribió entre medio responde stale sin escribir y el lote queda en la pila; con steps>1 se detiene en el primer fallo; sin nada que deshacer responde nothing_to_undo. El undo es una escritura nueva y la procedencia (sldb.by/at/via) refleja al actor de la sesión.
