## REFORMULACION
Encargo ejecutable (no agregado): corregir la violación de clean code introducida por task-sldb-version en `src/sldb/store/package_version.py`, donde `source_revision` tiene 12 líneas de lógica (máximo 10). Resultado: `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` verdes, sin cambio de comportamiento ni de API pública (los nombres siguen importándose del módulo original vía reexport), con una línea en `CHANGELOG.md` y commit. Repo: SLDB (`/mnt/ssd/proyectos/SLDB_1`). Límites: solo las reglas indicadas (1 clase/archivo, 80 líneas efectivas/archivo, 10 líneas de lógica/función) y solo estos archivos; otras violaciones se anotan, no se tocan; no se modifican tests de comportamiento.

## AMBIGUEDADES
1. «Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet'»: el input no incluye `CHANGELOG.md` ni verifica que esa cabecera exista con esa grafía; obligaría a inventar el encabezado real y el formato de la entrada.
2. «Extraer la corrida de git (subprocess.run con timeout y el manejo de FileNotFoundError, TimeoutExpired y rc distinto de 0) a una función privada _git_describe(dir)»: no dice si el chequeo `(checkout / ".git").exists()` queda en `source_revision` o dentro de `_git_describe`; obligaría a inventar la frontera y por tanto el reparto exacto de líneas.
3. «80 líneas efectivas por archivo y 10 líneas de lógica por función»: no define cómo se cuentan las líneas efectivas ni qué excluye la métrica; obligaría a inventar la regla de conteo para decidir si hace falta extraer también a módulo nuevo.
4. «los tests de la tarea original siguen verdes sin cambios»: no enumera cuáles son; obligaría a inventar el conjunto (¿`test_cli_v2.py`, `test_cli_envelope.py`, ambos?).

## DRY-RUN
Lecturas: `src/sldb/store/package_version.py`, `tests/test_clean_code_rules.py`, `CHANGELOG.md`, `tools/check.sh`, tests de CLI citados. Cambios previstos: añadir `_git_describe(dir)` con el `subprocess.run` y su manejo de excepciones/rc; reducir `source_revision` a composición; si la métrica lo exige, extraer a módulo hermano con reexport desde el original; una línea en CHANGELOG. Dependencias: `git`, `uv` con extras `code`/`dev`, `pytest`. Validaciones futuras (no ejecutadas): los cuatro comandos de Validation, más `git diff` sobre tests de comportamiento y revisión de otras violaciones para `result-summary.md`.

## FUTURO
Deciden otros nodos/humanos: el mensaje y tipo de commit (closeout), el contenido exacto del `CHANGELOG.md` real, si las violaciones adicionales de `check.sh` merecen tarea propia, y la aprobación del reexport como API pública.
