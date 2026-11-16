---
sldb:
  by: agent
  at: '2026-11-16T07:40:03Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-una-carga-del-índice-en-attach-atom-edges
status: active
summary: una carga del índice en attach_atom_edges
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: una carga del índice en attach_atom_edges

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

src/sldb/api/matching/store_reader.py, src/sldb/store/edge_index/edge_index.py, src/sldb/store/edge_index/composed_reading.py, src/sldb/store/edge_index/shard_signature.py

## How

_Describe the correct way to apply this guidance._

La meta es a lo sumo 2 llamadas a load_edge_index por llamada a attach_atom_edges: una con enlaces y otra sin ellos, si hacen falta las dos. StoreReader guarda el EdgeIndex que devuelve load_edge_index y resuelve cada referencia con los métodos edges_from y edges_to de EdgeIndex. Los nombres reales de la caché compuesta (load_composed, disk_key) mandan sobre _COMPOSED. shards_signature existe en src/sldb/store/edge_index/shard_signature.py. La ruta del project.yml del comando de IR está en la nota de origen: leerla con deskops message read 20261115-224941 --root sldb.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.
