## REFORMULACION
Encargo ejecutable `task.code` en el repo `/mnt/ssd/proyectos/SLDB_1`: añadir `sldb notations validate <nombre|ruta>`, que detecte notación, paleta o spec, reutilice los validadores existentes y emita findings de sldb con `--format text|json`, exit 0 sin errores, 1 con findings de error y 2 para nombre desconocido (`unknown notation, palette or spec: <nombre>`). Incluye parser/comando, tests indicados y una línea de CHANGELOG. Límites: no portar pruebas de spec2viz, no validar `vistas.yml`, no cambiar reglas existentes; commit solo coordinador, sin push. No es agregado ni paquete no ejecutable.

## AMBIGUEDADES
1. El Goal dice “detecta si el objetivo es una notación, una paleta o un spec”, pero el Scope limita: “un nombre se busca entre las notaciones y paletas builtin y del store”. No define búsqueda de specs por nombre ni precedencia; obligaría a inventar almacenes, orden y resolución.
2. “si el argumento es un archivo existente, .json o .yml/.yaml” no precisa cómo distinguir JSON; después solo describe YAML: “un YAML con clave "palette" o "colors" en la raíz es paleta, con clave "type" de diagrama ... es spec”. Obligaría a inventar detección JSON y precedencia si coexisten `palette`/`colors` y `type`.
3. “el resto se intenta como notación con load_notation; si el contenido no cuadra con ningún loader, exit 1 con el error del último loader”. No define “resto”, orden de intentos ni qué hacer con archivo existente de otra extensión; obligaría a inventar fallback y selección del error.

## DRY-RUN
Lecturas: `src/sldb/cli/parsers/notations.py`, `src/sldb/cli/commands/notations.py`, loaders/checks citados, `sldb.core.finding`, patrones de `edges.py`/`stores check`, test y CHANGELOG. Cambios previstos: registrar `_add_validate`, implementar detección/resolución, convertir resultados y excepciones en findings, añadir cuatro tests y entrada CHANGELOG. Dependencias: APIs existentes de loaders/checks, `Finding`, `alert_sink`, helpers del test. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/notations/test_notations_sync_spec_cli.py`, probar `sldb notations --help` y un builtin válido. Sin ejecutar nada.

## FUTURO
El ejecutor produce `runs/subagents/<run-dir>/result-summary.md` y, si aplica, el aviso; el coordinador hace `deskops closeout commit` y decide sobre las ambigüedades; un humano valida el cierre.
