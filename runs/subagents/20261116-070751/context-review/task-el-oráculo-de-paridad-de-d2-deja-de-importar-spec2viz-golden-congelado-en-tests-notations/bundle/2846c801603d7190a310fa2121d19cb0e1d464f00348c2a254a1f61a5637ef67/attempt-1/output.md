## REFORMULACION

Tarea ejecutable `task.code` en SLDB_1, no agregada. Propósito: retirar el último uso vivo de spec2viz del oráculo de paridad de D2 en `tests/notations/test_component_spec_python.py`. Resultado: golden JSON congelado en `tests/notations/goldens/component_spec_python_spec2viz.json` (`modules`, `classes`, `defines`, `_source`), test que lee el golden sin importar spec2viz y entrada en `CHANGELOG.md`. Límites: no tocar `vistas.yml`/`identity.toml` ni otros usos; no ajustar `component_spec_from_python` ni el golden a mano; solo módulos, clases y defines; commit y cierre del coordinador.

## AMBIGUEDADES

1. «con spec2viz instalado… Si spec2viz no está instalado en la máquina, generar el golden desde el checkout… con PYTHONPATH»: no fija precedencia ni qué `_source` declarar si la versión instalada difiere del checkout. Obliga a inventar la fuente y el commit.
2. «la lista ordenada de pares [from, to]»: no dice criterio de orden ni tratamiento de duplicados. Obliga a inventar el orden exacto y si se compara lista o conjunto.
3. «El test pasa a leer el golden y comparar contra _defined(spec) convertido a la misma forma»: no aclara si se conservan la aserción exacta de clases y la de `findings`. Obliga a inventar si se mantienen.
4. «La comprobación "sin spec2viz" es: `python -c "import spec2viz"` falla… o bien correr el test con PYTHONPATH=src…»: Validation solo lista pytest y grep; no fija un comando/entorno reproducible. Obliga a inventar cómo garantizarlo.
5. «bajo el encabezado "## 0.1.13 — not released yet"»: no dice qué hacer si ese encabezado no existe o no es el vigente. Obliga a inventar ubicación o versión.

## DRY-RUN

Un ejecutor futuro leería el test, `TREE`/fixture `tree`, `CHANGELOG.md`, `git -C …/spec2viz rev-parse HEAD` y la carpeta `goldens`. Crearía el golden desde spec2viz sobre una copia temporal de `TREE`; reemplazaría `importorskip` y la comparación viva por lectura del golden; añadiría la línea de CHANGELOG. Dependencias: spec2viz instalado o checkout, tree-sitter/`[code]`, pytest y PYTHONPATH. Validaría con `TMPDIR=/dev/shm pytest -q …`, el grep sin imports, la comprobación de que `import spec2viz` falla, y revisión de golden/CHANGELOG antes del closeout.

## FUTURO

El coordinador ejecuta `deskops closeout commit` y el aviso; si la paridad falla, se reporta y un humano decide sin tocar el golden. La disponibilidad/versión de spec2viz y la aceptación del entorno sin spec2viz son decisiones externas. El informe va a `runs/subagents/<run-dir>/result-summary.md`.
