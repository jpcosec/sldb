REFORMULACION
Encargo: limpiar residuos de kgdb y cáscaras vacías de la API en el repo sldb. Resultado: cada archivo nombrado (`parsers/graph.py`, partes de `parsers/stores.py`, `help_texts_graph.py`, `ingest_sldb.py`, `python_source_graph.py`) y cada módulo de `src/sldb/api` sin lógica propia queda borrado si no se usa, o reducido a lo usado, sin cambiar comportamiento observable (CLI, API pública, tests). Límites: conservar la API pública declarada en `__all__`; no retirar subcomandos; en `stores.py` solo salen funciones/constantes sin uso; no cambiar comandos ni API pública. Entregables: `result-summary.md` con tabla archivo→borrado/reducido/conservado y evidencia, CHANGELOG y commit.

AMBIGUEDADES
1. “cada módulo de src/sldb/api que no tenga lógica propia” frente a “cáscara = módulo ... cuyo cuerpo solo tiene docstring, imports, reexports o __all__”. Obliga a inventar si imports con efectos laterales, reexports dinámicos o código condicional cuentan como “sin lógica”.
2. “Uso = cualquier import o referencia por nombre en src/, tests/, tools/, docs/ o en los entry points”. Obliga a inventar si consumidores externos, `getattr`, plugins o referencias dinámicas fuera de esas rutas protegen un módulo; también si una mera mención en docs es “uso”.
3. “sin cambiar ningún comportamiento observable (CLI, API pública, tests)” y “mantener la API pública declarada en los __all__”. Obliga a inventar si un símbolo no incluido en `__all__` pero importado históricamente es API pública.
4. “en src/sldb/cli/parsers/stores.py solo salen funciones o constantes sin uso”. Obliga a inventar qué “partes” del archivo están afectadas si no hay inventario previo.

DRY-RUN
Lecturas: TaskDoc, `pyproject.toml`, `src/sldb/api`, archivos listados, `__all__`, tests, tools, docs y run-dir. Cambios previstos: borrar/reducir archivos tras grep de imports/referencias; crear `result-summary.md`; actualizar CHANGELOG; commit. Dependencias: entorno `uv`, tests existentes, backend de grafo. Validaciones futuras: los cinco comandos de Validation, sin ejecutarlos ahora.

FUTURO
Un ejecutor hará inventario y decidirá cada caso; un humano/coordinador podrá validar la tabla y el commit.
