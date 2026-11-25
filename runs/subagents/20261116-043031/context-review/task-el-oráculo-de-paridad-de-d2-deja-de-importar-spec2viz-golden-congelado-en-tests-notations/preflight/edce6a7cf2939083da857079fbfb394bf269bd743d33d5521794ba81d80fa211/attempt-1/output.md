## REFORMULACION

Encargo ejecutable, no agregado. Propósito: eliminar la dependencia viva de `spec2viz` en el test de paridad D2. Resultado: `tests/notations/test_component_spec_python.py` compara contra un golden JSON versionado y no importa `spec2viz` en ninguna rama. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: solo ese test, el golden nuevo `component_spec_python_spec2viz.json` y `CHANGELOG.md`; fuera de alcance `vistas.yml`, `identity.toml`, otros usos de `spec2viz` y cambios en `component_spec_from_python`; si la paridad falla, se reporta, no se retoca el golden.

## AMBIGUEDADES

1. «la entrada que hoy usa el test»: no se identifica fixture, ruta ni argumentos concretos; obligaría a inventar la entrada exacta.
2. «la carpeta goldens de tests/notations»: no fija ruta exacta ni confirma que exista; obligaría a inventar `tests/notations/goldens/`.
3. «la clave "_source" que dice el commit de spec2viz»: no define formato del commit ni cómo obtenerlo desde el checkout; obligaría a inventar hash corto/completo y método.
4. «su salida normalizada»: no precisa normalización previa aparte de serializar con `sort_keys=True` e `indent=2`; obligaría a inventar transformaciones.
5. «comprobado con python -c "import spec2viz" fallando o con PYTHONPATH sin spec2viz»: no fija entorno ni comando único; obligaría a inventar la comprobación exacta.

## DRY-RUN

Lecturas: task doc, `tests/notations/test_component_spec_python.py` (línea 43 y función comparadora), fixtures de entrada, carpeta de goldens, `CHANGELOG.md`; comprobar disponibilidad de `spec2viz` o usar el checkout indicado con `PYTHONPATH`. Cambios previstos: generar una vez el golden JSON con `_source`; sustituir comparación viva por lectura del golden; quitar `importorskip`; anotar en CHANGELOG. Dependencias: tarea previa de escaneo de imports y disponibilidad del checkout o paquete `spec2viz`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_python.py`; grep sin imports de `spec2viz`; ejecución sin `spec2viz` importable. Sin ejecutar nada.

## FUTURO

Otro nodo debe aportar o confirmar el commit/procedencia de `spec2viz`; un humano decide si una discrepancia de paridad bloquea o se reporta, y aprueba el commit final.
