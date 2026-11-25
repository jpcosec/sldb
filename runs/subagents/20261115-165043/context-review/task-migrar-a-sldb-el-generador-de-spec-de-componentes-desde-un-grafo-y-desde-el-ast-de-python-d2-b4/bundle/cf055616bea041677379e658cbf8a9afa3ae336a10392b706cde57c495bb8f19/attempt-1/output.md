## REFORMULACION

El nodo es ejecutable (`task.code`), no un agregado. Propósito: migrar a `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`) la generación de spec de componentes desde grafo/snapshot y desde AST de Python, reutilizando capacidades existentes. Resultado: una función de `sldb.api` que devuelva el modelo de componente desde grafo, snapshot o árbol Python, más informe de comparación y tests de paridad portados. Límites: “SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE”; no duplicar el escaneo AST de `sldb.code`; `spec2viz` no se retira; validar con pytest por archivo, `tools/check.sh` y `sldb stores build --check`.

## AMBIGUEDADES

1. “una función de `sldb.api` que devuelve el spec de componentes”: no fija nombre, firma, formato de entrada ni comportamiento ante grafo/snapshot/árbol; obligaría a inventar la API pública.
2. “si `sldb` ya la cubre, se reutiliza”: no define criterio de cobertura funcional; obligaría a inventar equivalencias entre funciones de `spec2viz` y `sldb`.
3. “el modelo de componente de la tarea de modelos de spec”: el modelo concreto no está en el input; obligaría a inventar su interfaz.
4. “los de `python_ast` portados”: no enumera esos tests; obligaría a inventar el alcance exacto de paridad.
5. “gate IR13”: no se explicita la condición del gate; obligaría a inventar qué impide retirar `spec2viz`.
6. “archivos tocados”: no se listan; obligaría a inventar la lista para ejecutar pytest “uno a la vez”.

## DRY-RUN

Lecturas previstas: TaskDoc, Board, rituales, tarea dependiente de modelos, pills/átomos ligados (el bundle no los incluye), `sldb.api` (`evaluate_projection_view`, `save_projection_view`), `sldb.code` (`PythonSymbolDoc`), cargador snapshot node-link, y `spec2viz` (`graph_import`, `python_ast`, tests `test_graph_import`). Cambios previstos: adaptador/reutilización en `sldb.api`, migración solo de lo no cubierto, tests portados y informe de comparación. Dependencias: modelo de componente de la tarea previa y acceso a `spec2viz`. Validaciones futuras, sin ejecutar: pytest individual de archivos tocados con `TMPDIR=/dev/shm`, `tools/check.sh`, `sldb stores build --check`, y paridad de tests.

## FUTURO

La tarea dependiente debe entregar el modelo de componente concreto. Un humano decide el criterio de equivalencia, la firma pública y el alcance de paridad, y confirma IR13. Otro nodo ejecutará validaciones y closeout con commit atómico.
