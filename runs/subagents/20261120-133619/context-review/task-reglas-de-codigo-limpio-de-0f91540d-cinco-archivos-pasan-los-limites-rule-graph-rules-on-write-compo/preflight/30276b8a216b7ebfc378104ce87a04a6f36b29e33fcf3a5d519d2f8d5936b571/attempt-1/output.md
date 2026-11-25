## REFORMULACION

Encargo: en el repo `/mnt/ssd/proyectos/SLDB_1/sldb`, hacer que `tests/test_clean_code_rules.py` pase entero sin subir límites, partiendo funciones y creando módulos donde haga falta, preservando comportamiento. Resultado: los cinco archivos señalados (`rule_graph.py`, `rules_on_write.py`, `component_spec_graph.py`, `store_check.py`, `diagnostics.py`) cumplen los límites indicados; los tests de las tareas previas siguen verdes sin tocar asserts; todo módulo nuevo fuera de “carpeta con eje” se declara en `contracts/layers.toml`. Límites: no cambiar comportamiento ni límites; el commit selectivo con trailer `Task-Id` y `deskops advance` son obligatorios.

## AMBIGUEDADES

1. “Un módulo nuevo fuera de una carpeta con eje se declara en contracts/layers.toml”: no define “carpeta con eje” ni el formato de declaración. Obliga a inventar el criterio y la sintaxis.
2. “97 líneas efectivas (máx. 80)”: no define “efectivas” (¿sin blancos/comentarios/imports?). Obliga a inferir la métrica del test.
3. “los tests de las cuatro tareas (…cinco archivos…)”: cita cuatro tareas pero enumera cinco archivos. Obliga a decidir si sobra uno o falta una tarea.
4. “partir cada uno (funciones auxiliares, módulo hermano)”: no fija criterio de extracción ni nombres/ubicación de módulos. Obliga a inventar el diseño.
5. “salvo 'identidad' por workbench_demo (excepción autorizada; decisión aparte)”: no aclara qué hacer si “identidad” falla por otra causa. Obliga a inventar el tratamiento.
6. “commit SOLO de tus archivos”: no indica cómo proceder si otro agente modifica las mismas rutas. Obliga a inventar resolución de conflictos.

## DRY-RUN

Lecturas: este TaskDoc, `tests/test_clean_code_rules.py`, los cinco archivos y sus tests asociados, `contracts/layers.toml`, `tools/check.sh`. Cambios previstos: extraer auxiliares/módulos hermanos en cada archivo; declarar módulos nuevos en `layers.toml`; commit selectivo con `Task-Id`; `deskops advance`. Dependencias: `pytest`, `git`, `bash`, `TMPDIR=/tmp`. Validaciones futuras: `pytest` de clean-code, luego cada uno de los cinco tests, después `check.sh --fast`, y verificación del commit. Sin ejecutar nada.

## FUTURO

El nodo `integrate` corre la suite completa. Un humano decide la excepción de “identidad”/`workbench_demo` y cualquier conflicto entre agentes. Otro nodo puede revisar la declaración en `layers.toml`.
