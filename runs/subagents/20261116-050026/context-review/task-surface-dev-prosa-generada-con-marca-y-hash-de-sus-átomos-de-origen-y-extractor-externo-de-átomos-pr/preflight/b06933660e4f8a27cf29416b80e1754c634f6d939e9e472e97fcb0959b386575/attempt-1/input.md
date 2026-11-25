FILE:desk/tasks/task-surface-dev-prosa-generada-con-marca-y-hash-de-sus-átomos-de-origen-y-extractor-externo-de-átomos-pr.md
---
sldb:
  by: agent
  at: '2026-11-16T04:18:25Z'
  authority: generated
  via: create_document
id: task-surface-dev-prosa-generada-con-marca-y-hash-de-sus-átomos-de-origen-y-extractor-externo-de-átomos-pr
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field
pills: []
files:
- surface/dev/levira-store/models.py
- surface/dev/atoms-store/models.py
- docs/surface/OPERACIONALIZACION-VISTAS.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-cerrar-las-cuatro-decisiones-de-operacionalizacion-vistas-6.md
---

# Surface dev: prosa generada con marca y hash de sus átomos de origen, y extractor externo de átomos propuesto (decisiones 3 y 4 de OPERACIONALIZACION-VISTAS §6)

## Rationale

_Explain why this task exists or the business driver behind it._

docs/surface/OPERACIONALIZACION-VISTAS.md §6 deja cuatro decisiones con recomendación, que se toman como decididas. (1) offsets sobre el campo body (source_field) y (2) valor descartado en status ya están en surface/dev/atoms-store/models.py (152fc723). Faltan (3) prosa generada con marca "generado" y hash de los átomos de origen, que se ve desactualizada si el hash cambia y nunca se reescribe sola (surface/dev/levira-store/models.py tiene generada_por pero no el hash); y (4) un extractor fuera de la UI y de /extract/segments que escribe AtomDoc con status propuesto y nunca toca los confirmado. El ítem quedó bloqueado por la convergencia átomo/field, que es la tarea task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field. sldb/surface/ es de JP y tiene trabajo suyo: esta tarea corre en la máquina local de JP, coordinada con él. Origen: drawer desk/drawer/tasks/task-cerrar-las-cuatro-decisiones-de-operacionalizacion-vistas-6.md.

## Goal

_Describe the concrete result this task must produce._

En los stores de surface/dev, un documento de prosa generada guarda la marca generado y el sha256 de los source_hash de sus átomos de origen, y una función de lectura dice si está desactualizado; un extractor por línea de comandos escribe AtomDoc nuevos con status propuesto sin modificar ninguno confirmado; §6 del doc dice que las cuatro decisiones están tomadas y dónde quedó cada una.

## Scope

_State what is in scope and what is out of scope._

Entra: campos nuevos en el modelo de prosa de surface/dev/levira-store/models.py (generado: bool, hash_origen: str) con su marcador en la plantilla; una función que recalcula el hash desde los átomos citados y compara; el extractor como script o comando de surface/dev que usa sldb.api (create_document) para escribir los propuesto y salta los ids que ya existen confirmado; actualizar §6 de docs/surface/OPERACIONALIZACION-VISTAS.md. Antes de tocar surface/, confirmar con JP que su trabajo sin commitear ahí está commiteado o que esta tarea no lo pisa. Tests junto a los stores de surface/dev si existe carpeta de tests ahí; si no, un test en tests/ que carga los modelos con sus stores de ejemplo. No entra: cambios de UI en el navegador, cambiar los modelos de átomo base de sldb (los define la tarea del set bootstrap).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Esperar a que la tarea del set bootstrap esté cerrada. 2) Leer surface/dev/atoms-store/models.py, surface/dev/levira-store/models.py y §6 del doc. 3) Acordar con JP el estado de surface/. 4) Implementar (3) y (4). 5) Regenerar cada store con su seed.sh (idempotente: borra y recrea .sldb, docs/ y data/ dentro de su carpeta) y correr stores check, como en Validation; agregar al seed.sh los documentos de ejemplo de prosa generada.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm bash surface/dev/levira-store/seed.sh && cd surface/dev/levira-store && PYTHONPATH=../../../src:. python -m sldb stores check --store .sldb --pythonpath .
- TMPDIR=/dev/shm bash surface/dev/atoms-store/seed.sh && cd surface/dev/atoms-store && PYTHONPATH=../../../src:. python -m sldb stores check --store .sldb --pythonpath .

## Done When

_Name the observable condition that makes the task complete._

Los dos seed.sh corren y sus stores pasan stores check; un documento de prosa con hash viejo se lee como desactualizado; el extractor corrido dos veces no duplica ni toca confirmados; §6 actualizado; commit hecho por JP o con su visto bueno.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-surface-dev-prosa-generada-con-marca-y-hash-de-sus-átomos-de-origen-y-extractor-externo-de-átomos-pr: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

