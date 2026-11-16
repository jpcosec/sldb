---
sldb:
  by: agent
  at: '2026-11-16T08:50:53Z'
  authority: generated
  via: save_document_payload
id: task-surface-dev-prosa-generada-con-marca-y-hash-de-sus-átomos-de-origen-y-extractor-externo-de-átomos-pr
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:local
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
from_drawer: drawer task-cerrar-las-cuatro-decisiones-de-operacionalizacion-vistas-6
  (retirado en el triaje 2026-11-16; contenido en git antes del commit del triaje)
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

Precisiones (preflight-1): la tarea del set bootstrap está cerrada cuando su TaskDoc ya no existe en desk/tasks (deskops closeout la retira) o su status es closed. El acuerdo con JP es su respuesta por el canal de coordinación, anotada en result-summary.md con fecha. hash_origen = sha256 de los source_hash de los átomos citados, ordenados alfabéticamente y unidos con "\n". La función es esta_desactualizada(doc, store) -> bool en surface/dev/levira-store/models.py. El extractor es un script python en surface/dev/atoms-store que recibe --store y un archivo de texto y escribe un AtomDoc propuesto por párrafo no vacío, con id derivado del sha256 del párrafo, y salta los ids existentes. seed.sh agrega un documento de prosa generada con hash vigente y otro con hash viejo.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

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
