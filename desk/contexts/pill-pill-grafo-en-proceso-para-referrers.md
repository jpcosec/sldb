---
sldb:
  by: agent
  at: '2026-11-16T07:47:08Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-grafo-en-proceso-para-referrers
status: active
summary: grafo en proceso para referrers
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: grafo en proceso para referrers

## What

_Define the context or guardrail this pill carries._

Las respuestas del bundle-1 de la tarea: precisiones de implementación que la revisión en frío pidió y que el contrato deja abiertas.

## Why

_Explain why this context matters for safe execution._

La revisión cold-bundle (bundle-1) mostró que sin estas precisiones el ejecutor tendría que inventar estos detalles.

## When

_Describe when an agent should apply this pill._

Al ejecutar la tarea, antes de tocar código.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/sldb/api/edges/project_graph/project_graph.py, tests/api/test_project_graph.py

## How

_Describe the correct way to apply this guidance._

Un ProjectGraph se arma en proceso con ProjectGraph(root, config), igual que en tests/api/test_project_graph.py (líneas 104-139); config es un ProjectGraphConfig como el CONFIG de ese test. El desk mínimo de la nota es: un store en tmp_path con un átomo 'atom-a' trackeado y un archivo de tarea con la línea 'Depends on atom:atom-a.' que el config declara como fuente de menciones; sin graph, referrers(store, 'atom-a') devuelve []; con graph, devuelve esa mención. H-c: se descarta solo la mención que repite, en el mismo documento y la misma línea del frontmatter, un hit schema.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
