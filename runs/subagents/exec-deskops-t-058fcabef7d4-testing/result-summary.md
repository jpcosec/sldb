PASA

# Resultado de testing

Tarea: task-la-puerta-identidad-de-tools-check-sh-clasifica-workbench-demo-store-demo-del-workbench-de-surface-e
Rol: deskops-tester
Commit del ejecutor: `05213f930e1450fcd947b56e6dc255e8c55af56d` (`identity: clasifica workbench_demo como foreign`)

## Archivos del commit

    contracts/identity.toml | 6 ++++++

El commit solo agrega el bloque `[[foreign]]` de `workbench_demo`; no toca
`tools/check_identity.py`, ni su test, ni mueve/borra `workbench_demo/`.
No incluye archivos `tests/*.py` ni módulos de código, así que no hay
`tests/test_<modulo>.py` aplicable que ejecutar para este cambio.

## Verificación del contrato

- Existe exactamente un bloque `[[foreign]]` con `path = "workbench_demo"`.
- Tiene las cuatro claves requeridas: `path`, `files`, `what`, `verdict`.
- `files = 213` coincide con `git ls-files workbench_demo | wc -l` (213).
- `what` y `verdict` declaran que es un store de demo del workbench de surface,
  ajeno al producto y a la autoaplicación.
- Los ajenos declarados quedan: `surface`, `sldb`, `workbench_demo`.

## Puertas ejecutadas

Con el Python del venv del repo (Python 3.13.18; `/tmp/ws-venv` no existía en
este contenedor):

    export PATH="$PWD/.venv/bin:$PATH"
    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-058fcabef7d4"
    bash tools/check.sh --fast

Resultado: **rc 0 — TODAS LAS PUERTAS PASAN**

- núcleo aislado: PASS
- capas: PASS
- identidad: PASS — 0 violaciones, 3 directorios declarados ajenos
- ejes: PASS
- superficie: PASS

Puerta de identidad específica:

    .venv/bin/python tools/check_identity.py

Resultado: `PASS: identidad — 10 paquetes de producto, 19 modelos clasificados, 0 violaciones` (rc 0).

## Veredicto

PASA. El bloque `[[foreign]]` de `workbench_demo` está presente y correcto, y
`bash tools/check.sh --fast` termina con rc 0.
