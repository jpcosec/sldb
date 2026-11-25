REFORMULACION
Propósito: retirar residuos de kgdb y cáscaras vacías de sldb.api sin alterar comportamiento observable. Resultado: cada archivo nombrado (y cada módulo de src/sldb/api sin lógica propia) borrado si no se usa o reducido a lo usado; tabla archivo→borrado|reducido|conservado con evidencia de grep en result-summary.md; CHANGELOG y commit. Repo: sldb en /mnt/ssd/proyectos/SLDB_1. Límites: no retirar subcomandos del CLI, no cambiar API pública ni tests; en stores.py solo salen funciones/constantes sin uso. Es tarea hoja (atoms: []), no agregado.

AMBIGUEDADES
1. "src/sldb/cli/parsers/graph.py" figura como residuo, pero "No se retira ningún subcomando del CLI" y todas sus funciones cuelgan de add_graph_group: obligaría a inventar qué se reduce exactamente.
2. La definición de cáscara vale solo para api: "cáscara = módulo de src/sldb/api cuyo cuerpo solo tiene docstring, imports, reexports o __all__". Para help_texts_graph.py, ingest_sldb.py y python_source_graph.py (con lógica/constantes) no hay criterio: obligaría a inventar cuándo se borran.
3. "result-summary.md del run-dir": no se identifica la ruta del run-dir; obligaría a inventar ubicación y formato.
4. "sin cambiar ningún comportamiento observable" frente a "CHANGELOG.": no se sabe si procede entrada ni con qué tipo; obligaría a inventar la decisión editorial.
5. "Uso = cualquier import o referencia por nombre en src/, tests/, tools/, docs/ o en los entry points de pyproject.toml": no cubre imports dinámicos, strings ni reexports transitivos; obligaría a inventar su tratamiento.

DRY-RUN
Un ejecutor futuro: lee Board, TaskDoc, rituales y los cinco archivos; hace inventario con grep según la definición de uso; clasifica cada módulo de api y cada función/constante de stores.py; borra o reduce uno a uno; mantiene __all__ públicos; actualiza CHANGELOG; escribe result-summary.md; corre las cinco validaciones en orden (tests pequeños primero, luego tools/check.sh --fast); si algo falla, revierte el ítem. No ejecuta nada ahora.

FUTURO
Deskops/Board enlazan pills y átomos (hoy vacíos) y ejecutan closeout/commit; un humano confirma si los residuos kgdb deben desaparecer pese a conservar subcomandos; el arnés fija la ruta del run-dir.
