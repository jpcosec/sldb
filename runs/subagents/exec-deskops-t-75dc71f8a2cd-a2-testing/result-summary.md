FALLA

# Testing — `sldb notations validate` (notación, paleta o spec por nombre o ruta)

## Veredicto

**FALLA por la puerta rápida obligatoria.** `bash tools/check.sh --fast` termina con **rc 1**:
la puerta `identidad` rechaza el directorio versionado `workbench_demo` ("directorio versionado sin
clasificar en la raíz"). La regla del rol de testing es explícita: rc distinto de 0 en
`check.sh --fast` ⇒ FALLA.

La roja es **preexistente y ajena a este commit**: `workbench_demo` ya está versionado en el padre
`70bd8e59` y `contracts/identity.toml` no lo clasifica; el commit del ejecutor (`672f8793`) no toca
ni ese directorio ni `contracts/identity.toml`. El contrato de la tarea la declara excepción
autorizada ("verde salvo 'identidad' por workbench_demo"), así que si el coordinador la acepta
formalmente este punto no bloquea.

**Veredicto funcional: FALLA** por un defecto de alcance que el propio ejecutor anota en su informe:
los nombres que existen **solo en el store** se detectan como conocidos, pero luego se validan con
`load_notation(nombre)` / `load_palette(nombre)`, que solo resuelven builtin o archivo. El resultado es
un `-invalid` falso (exit 1) para una notación/paleta válida del store. El Scope y la Precisión (3)
piden buscar el nombre "entre las notaciones y paletas builtin y del store", y el Goal pide exit 0 si
no hay errores. Si el coordinador decide que los nombres solo-store quedan fuera de alcance, habría
que corregir el contrato; tal como está escrito, no se puede cerrar.

## Dónde está el trabajo

- Commit verificado: `672f8793f6180192179c34b1339af6c3be1c18b6`
  ("sldb notations validate valida una notación, una paleta o un spec"), con el trailer
  `Task-Id: task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding`.
  Existe un commit idéntico en el worktree del ejecutor (`be78baa9`); el diff de código/test/CHANGELOG
  entre ambos es vacío.
- Archivos de código:
  - `src/sldb/cli/parsers/notations.py` (`_add_validate`, registrado en `add_notations_group`)
  - `src/sldb/cli/commands/notations.py` (dispatch `validate`)
  - `src/sldb/cli/commands/notations_validate.py` (nuevo)
- Test nuevo: `tests/notations/test_notations_validate_cli.py`.
- Selfdoc regenerado: `.sldb/core/documents/CliCommandDoc/cmd-sldb-notations-validate.yaml`,
  `knowledge/commands/cmd-sldb-notations-validate.md`, `knowledge/surfaces/surface-sldb-notations.md`,
  `surface-sldb-notations.yaml`, modelos e índice del store.
- `CHANGELOG.md`: línea presente bajo `## 0.1.13 — not released yet`.

## Pruebas ejecutadas (de a un archivo)

No existía `/tmp/ws-venv` en este contenedor; se usó el Python del venv del repo
(`/mnt/ssd/proyectos/SLDB_1/sldb/.venv`, Python 3.13.18).

| Comando | Resultado |
|---|---|
| `TMPDIR=/dev/shm python -m pytest -q tests/notations/test_notations_sync_spec_cli.py` (Validation del contrato) | **4 passed** |
| `TMPDIR=/tmp python -m pytest -q tests/notations/test_notations_validate_cli.py` (archivo del commit) | **8 passed** |
| Los dos archivos juntos, `TMPDIR=/dev/shm` | **12 passed** |
| `tests/test_cli_every_command_has_a_handler.py` | **1 passed** |
| `tests/test_cli_format_coverage.py` | **4 passed** |
| `tests/test_cli_reconciliation.py` | **3 passed** |

No existe `tests/test_notations.py` ni `tests/test_notations_validate.py` para los módulos tocados.
No se corrió la suite completa, según la instrucción del rol.

Comprobaciones manuales:

    sldb notations --help                 -> lista {list,sync,validate,view,resolve,from-graph}
    sldb notations validate default       -> rc 0
    sldb notations validate activity      -> rc 0
    python -m sldb selfdoc check          -> rc 0 (167 documentos, sin cambios)

## Defecto funcional: nombres solo-store

Reproducción en un store temporal (`/tmp/valstore`): sincronicé una notación `mynot.yml` (copia de la
builtin `activity` con `name: mynot`) y una paleta `mypal.yml` (copia de `default` con `name: mypal`),
ambas válidas y con exit 0 en el `sync`; después:

    sldb notations list --store .sldb
      -> store_notations: ["NotationDoc:mynot"]

    sldb notations validate mynot --store .sldb
      error: [notations/notation-invalid] mynot: unknown notation 'mynot': not a builtin (...) nor a file
      rc=1

    sldb notations validate mypal --store .sldb
      error: [notations/palette-invalid] mypal: unknown palette 'mypal': not a builtin (default) nor a file
      rc=1

    sldb notations validate activity --store .sldb
      rc=0

Causa: `_kinds_of_name` incluye los nombres del store vía `_store_names`, pero `_run_check` llama a
`load_notation`/`load_palette` sin contexto de store; esos loaders solo resuelven builtin o archivo.
El ejecutor lo reconoce en `runs/subagents/exec-deskops-e-8eb91b4956b3/result-summary.md` ("Store-only
names ... yields a `-invalid` error finding ... store docs are not re-validated from payload").

Esto no lo cubren los tests del commit: el caso de nombre repetido se prueba monkeypatcheando
`_kinds_of_name` y solo usa builtins, y no hay caso de nombre presente únicamente en el store.

## Lo que sí cumple

- Los cuatro casos pedidos existen y pasan: notación builtin válida (exit 0), paleta con contraste
  insuficiente (exit 1), spec inválido (exit 1), nombre desconocido (exit 2 con el mensaje exacto).
- Detección por ruta `.yml`/`.yaml`/`.json`: paleta por `palette`/`colors`, spec por `type`,
  notación en el resto; probé además paleta y spec en `.json` con rc 0.
- Salida de texto por finding y `--json` con `Finding.as_dict()`; alertas (`notations/ambiguous-name`)
  sin cambiar el exit code.
- `selfdoc check` en 0 y CHANGELOG commiteado.

## Gate rápido

    PATH=/mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin:$PATH bash tools/check.sh --fast  -> rc 1

    PASS: núcleo aislado
    PASS: capas
    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"
    PASS: ejes
    PASS: superficie

El commit no interviene en esa roja; verificado que `workbench_demo` está versionado en `70bd8e59`
(padre del ejecutor) y que `contracts/identity.toml` de ese padre tampoco lo clasifica.
