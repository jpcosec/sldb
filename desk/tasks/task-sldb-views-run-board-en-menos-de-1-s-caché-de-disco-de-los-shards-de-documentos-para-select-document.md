---
sldb:
  by: agent
  at: '2026-11-12T03:38:09Z'
  authority: generated
  via: create_document
id: task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/api/documents/select_documents.py
- src/sldb/api/views/
- src/sldb/store/io/
- src/sldb/store/edge_index/
- tests/
- docs/architecture/views.md
- CHANGELOG.md
- contracts/layers.toml
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb views run board en menos de 1 s: caché de disco de los shards de documentos para select_documents y costo del import de sldb.api (H11b)

## Rationale

_Explain why this task exists or the business driver behind it._

Resto de H11. La tarea H11 bajó sldb views run board de 7,0 a 1,6 s con el store construido (el índice compuesto persiste en disco y run_view lee solo el store que llama) pero no llegó a la meta de menos de 1 s. Lo que queda, medido por el worker de H11 sin perfil sobre 1,4 s: unos 0,55 s de importar sldb.api, 0,38 s de leer el JSON del índice y revisar los archivos, 0,35 s de select_documents, que parsea con yaml unos 540 shards de documentos en cada proceso, y el resto es la propia vista.

## Goal

_Describe the concrete result this task must produce._

sldb views run board, con el store construido y en un proceso nuevo, tarda menos de 1 s (mediana de 3) sobre el layout del benchmark de H11; el resultado y la revision de la vista no cambian, y un documento escrito o cambiado se nota en la siguiente corrida.

## Scope

_State what is in scope and what is out of scope._

En alcance: una caché de disco de los shards de documentos que select_documents lee, el costo del import de sldb.api (medirlo y recortar lo que se pueda de forma segura), tests, docs de vistas y CHANGELOG. Fuera: el índice de aristas y su caché compuesta (ya hechos en H11), el costo propio de deskops en view board (otra tarea de deskops), H12 (mensaje de store sin construir) y H13 (la revision depende de cachés del proceso).

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: informe del worker de H11 (sección de lo pendiente) y decisión del coordinador de proyecto. Precondición: H11 está integrada en sldb main. Esta tarea parte de ese main; si todavía no lo está, el worker para y avisa.

REPRODUCCIÓN: la del worker de H11, con caché frío y caliente, mediana de 3 en proceso nuevo, carga de la máquina registrada (runs/subagents/20261112-repro-h11b/repro.log). Con H11 aplicada, sldb views run board da 1,59 s con la caché de composición caliente, 3,9 s en la primera corrida tras el build y 2,6 s sin store construido. Desglose del caliente: importar sldb.api 0,55 s, índice JSON y revisión de archivos 0,38 s, select_documents 0,35 s, el resto la vista. El layout y el benchmark son los que dejó la tarea H11 (el script del benchmark vive en tests/perf de esa tarea); el worker lo vuelve a correr sobre su base como línea base propia antes de tocar nada.

CAUSA (a confirmar): select_documents parsea con yaml ~540 shards de documentos en cada proceso, sin caché de disco, y el import de sldb.api carga módulos que una vista no necesita.

CAMBIO (b1-b5), el worker mide cada paso antes y después:
b1: línea base propia y perfil de un proceso nuevo con python -X importtime (import de sldb.api) y con cProfile (select_documents), commiteados en el informe.
b2 (shards de documentos): una caché de disco, en el .sldb_cache del store que llama, de lo que select_documents necesita de los shards de documentos, guardada en JSON (nunca pickle: una caché de un clon no puede ejecutar código). La clave se calcula sin leer los shards que se quieren evitar: mtimes y tamaños de core/documents más la versión del índice y el contrato de cada modelo, igual que la caché de composición de H11. Cualquier diferencia es un fallo y se lee como antes.
b3 (import): del costo de importar sldb.api, lo que se pueda mover a imports perezosos sin cambiar la superficie pública ni el orden de los efectos. Si el recorte seguro es menor a 0,1 s, no se hace y el informe lo dice con la medición; el check de superficie de tools/check.sh --fast manda.
b4: tests: la vista da el mismo resultado y la misma revision con y sin la caché; escribir o cambiar un documento invalida la caché en la siguiente corrida; una caché corrupta o de otra versión se ignora sin error. tests/test_clean_code_rules.py es obligatorio (80 líneas efectivas por archivo, 10 de lógica por función, sin subir límites; un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml; los grados medidos salen de tools/check.sh --fast, no de mezclar números).
b5: docs de vistas y CHANGELOG. Si la meta de menos de 1 s no se alcanza, el informe dice cuánto falta y qué lo explica, con la medición.

VALIDACIÓN: el worker corre de a uno los tests que toca; antes de entregar, la suite completa de sldb de a un archivo desde /dev/shm, test_clean_code_rules y tools/check.sh --fast. Los 7 pasos del workflow de sldb los corre el coordinador. Las mediciones van siempre con caché frío además del caliente.

## Validation

_List the checks required before this task can close._

- Benchmark: sldb views run board, store construido, proceso nuevo, mediana de 3, menos de 1 s sobre el layout de H11; las medidas antes y después en el informe
- Test: el resultado y la revision de la vista son iguales con y sin la caché de shards de documentos; escribir o cambiar un documento invalida la caché; una caché corrupta se ignora
- Perfil de import de sldb.api y de select_documents, commiteados antes y después
- test_clean_code_rules (obligatorio) y tools/check.sh --fast
- suite completa de sldb de a un archivo desde /dev/shm en verde
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

b1-b5 hechos con las mediciones, tests verdes y la suite completa en verde, y la meta de menos de 1 s alcanzada o explicada con la medición; docs y CHANGELOG actualizados.
