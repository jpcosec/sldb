---
sldb:
  by: agent
  at: '2026-11-25T06:27:30Z'
  authority: generated
  via: create_document
id: task-el-listado-de-specs-y-vistas-de-sldb-serve-trae-la-cobertura-de-atomos-de-cada-una
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El listado de specs y vistas de sldb serve trae la cobertura de atomos de cada una

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de IR 20261125-032512-suggestion-sldb-serve-la-cobertura-de-atomos-de-cada-spec-o-vista-en-el-payload-de-notations-y-views (U2 de la UI de specIR: paridad con spec2viz, que mostraba n/m de atomos por diagrama; la UI no calcula).

## Goal

_Describe the concrete result this task must produce._

Que cada entrada de /notations (specs) y /views traiga covered y total de atomos, calculados por sldb.

## Scope

_State what is in scope and what is out of scope._

src/sldb/cli/serve/notations_payloads.py, views_payloads.py y un test. Fuera: la UI.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/sldb. Averiguar como sldb ya relaciona una spec o vista con sus atomos (aristas o campos que la apuntan; ver como el catalogo de specIR calculaba la cobertura en IR/src/specir/visual/catalog si hace falta el criterio) y exponer en cada entrada del listado coverage: {covered: int, total: int}; si la spec no declara atomos, coverage: null. Test nuevo tests/serve/test_listing_coverage.py con un store temporal: una spec con 3 atomos de los que 2 existen da {covered: 2, total: 3}; una sin atomos da null.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/serve/test_listing_coverage.py

## Done When

_Name the observable condition that makes the task complete._

/notations y /views traen coverage por entrada y el test nuevo pasa.
