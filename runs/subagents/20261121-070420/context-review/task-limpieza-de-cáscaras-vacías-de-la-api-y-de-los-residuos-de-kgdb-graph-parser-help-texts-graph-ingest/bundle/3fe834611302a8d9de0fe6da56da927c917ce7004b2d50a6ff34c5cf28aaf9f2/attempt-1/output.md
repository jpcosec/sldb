REFORMULACION
Propósito: eliminar residuos de kgdb y cáscaras vacías de `sldb.api` sin alterar comportamiento observable. Resultado: cada archivo nombrado y cada módulo de `src/sldb/api` sin lógica propia borrado si no se usa, o reducido a lo usado; API pública de los `__all__` intacta; tabla archivo→decisión con evidencia en `result-summary.md`; CHANGELOG y commit. Repo: `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`). Límites: no cambiar comandos CLI ni API pública; no retirar subcomandos; en `stores.py` solo funciones/constantes sin uso; validar con tests y `tools/check.sh --fast`. Es una tarea ejecutable, no un agregado.

AMBIGUEDADES
1. «cada cáscara vacía de sldb.api» no tiene inventario ni aparece en `files`; obliga a inventar qué módulos concretos son cáscaras hasta que el grep los descubra.
2. «Uso = cualquier import o referencia por nombre en src/, tests/, tools/, docs/» no aclara imports dinámicos, `importlib`, strings o plugins; obliga a inventar si cuentan como uso.
3. «en src/sldb/cli/parsers/stores.py solo salen funciones o constantes sin uso» no fija cómo probar que una función que registra subcomandos está sin uso; obliga a inventar el criterio.
4. «result-summary.md del run-dir» no fija la ruta exacta; obliga a inventar si es `attempt-1`, `context-review` o la raíz del run.
5. «CHANGELOG y commit» no dice si un cambio no visible requiere entrada ni con qué formato; el ritual de closeout solo lo exige si es visible/release-relevant; obliga a inventar.
6. «el supervisor del desk verificó en parte (2026-11-16)» no enlaza el análisis ni qué parte es fiable; obliga a inventar qué hallazgos se aceptan.

DRY-RUN
Lecturas: Board, TaskDoc, rituales, archivos listados, grep de imports/referencias en `src/`, `tests/`, `tools/`, `docs/` y `pyproject.toml`; inspección de `src/sldb/api` (cuerpo, `__all__`), entry points, CHANGELOG y `result-summary.md` existente. Cambios previstos: inventario; borrar o reducir módulo a módulo; ajustar imports/reexports conservando `__all__`; escribir tabla con evidencia; entrada CHANGELOG; commit atómico. Dependencias: resultados de grep, entry points, tests, convención de CHANGELOG y ubicación del run-dir. Validaciones futuras: los cinco comandos listados, revisión de la tabla y árbol limpio. Sin ejecutar.

FUTURO
El nodo ejecutor produce inventario, `result-summary.md`, CHANGELOG y commit. El nodo de closeout/deskops verifica tests, commit, átomos y árbol limpio, y retira la tarea del Board. Un humano/revisor aprueba la tabla y decide si la evidencia de grep basta para conservar un módulo.
