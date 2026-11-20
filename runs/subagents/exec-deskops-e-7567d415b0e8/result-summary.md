# Resultado — notations from-graph --label-field / --kind-field / --group-field

Estado: implementado y probado; SIN commit y SIN `deskops advance` porque `tools/check.sh --fast` sale con rc 1 por algo ajeno.

## Bloqueo
`bash tools/check.sh --fast` -> rc 1: `identidad: directorio versionado sin clasificar en la raíz: workbench_demo` (agregado en 562847e2, no tocado por esta tarea). Hace falta que el coordinador clasifique `workbench_demo` en el contrato de identidad; luego commitear los archivos de abajo.

## Cambios (archivos de la tarea)
- src/sldb/api/notations/component_spec_fields.py (nuevo): lee campo o `tag:<ns>`, aplica label/kind, crea contenedores `group` con `contains`.
- src/sldb/api/notations/component_spec_graph.py: `component_spec_from_graph(payloads=, label_field=, kind_field=, group_field=)`.
- src/sldb/cli/commands/notations_from_graph.py: carga los payloads del store (solo con `--store` y algún flag) y los pasa.
- src/sldb/cli/parsers/notations.py: los tres flags en `_from_graph_filters`; el --help documenta que `--snapshot` no tiene payload (solo id y modelo).
- tests/notations/test_notations_from_graph_cli.py: 3 tests nuevos (label+kind, grupos con contains, sin flags igual).
- CHANGELOG.md: una línea bajo 0.1.13. OJO: CHANGELOG.md ya tenía 2 líneas sin commitear de otras tareas; al commitear, stagear solo mi línea (git apply --cached de ese hunk).

Notas: el contenedor de grupo es un nodo kind `group`, label = valor; los documentos sin valor de grupo quedan fuera de contenedores. Solo documentos locales (sin stores enlazados). Sin avisos a otros repos.

## Validación
Ver validation.log: los dos pytest pasan (25); check --fast rc 1 (ajeno).

## Actualización (autorizada por el coordinador)
`check.sh --fast`: la puerta `identidad` falla SOLO por `workbench_demo` (preexistente de 562847e2; tarea de decisión aparte); las demás puertas pasan. Commit hecho con los archivos nombrados y trailer Task-Id; en CHANGELOG.md se stageó solo mi línea.

## Commit y advance
- Mis archivos y mi línea de CHANGELOG quedaron en el commit 0f91540d ("on_write: save_document_payload devuelve las alertas..."), NO en uno propio con trailer `Task-Id` de esta tarea: mi `git commit` falló por falta de identidad git y, antes de reintentar, otro agente commiteó el índice compartido con mis archivos ya stageados. Revisar al hacer closeout (no hay commit con mi Task-Id).
- Un primer `deskops advance` falló con "Rollback incomplete" (por el estado compartido del store); el segundo pasó: tarea en ritual-testing.
