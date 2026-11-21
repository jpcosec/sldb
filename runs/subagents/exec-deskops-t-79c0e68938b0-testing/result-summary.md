FALLA

# Testing — el generador del golden de D2 deja de importar spec2viz

## Alcance verificado

Commit del ejecutor: `cfa6477b814bb65b6f34e090bd4ea4fcb61bbc82`
(`D2: retira gen_golden.py (importaba spec2viz) y deja README`), con el trailer
`Task-Id: task-el-generador-del-golden-de-d2-deja-de-importar-spec2viz-para-que-el-retiro-de-spec2viz-no-cuente-a-s`.

Archivos del commit:

- `runs/subagents/20261116-exec-oraculo-d2/gen_golden.py` — borrado (`git rm`, 16 líneas).
- `runs/subagents/20261116-exec-oraculo-d2/README.md` — nuevo, 3 líneas. Documenta que el script
  generó el golden de `ce0bd384` a partir de spec2viz y que se retiró por el retiro de spec2viz;
  no contiene ningún `import`.

Verificaciones de contenido:

- `gen_golden.py` ya no existe en el árbol de trabajo.
- `grep -rn gen_golden src tests` → sin coincidencias.
- `grep -rnE '^\s*(from|import)\s+spec2viz' --include='*.py'` en todo el repo (sin `.git`/`.venv`)
  → sin coincidencias. No queda ningún import de spec2viz en Python dentro de sldb.
- El golden de D2 y sus tests no se tocaron.

## Tests ejecutados

El commit no incluye archivos `tests/*.py` ni módulos de código (`src/`); solo el script de `runs/`
y su README. Corrí la validación explícita de la tarea, de a uno y con el Python de `/tmp/ws-venv`
(`/tmp/ws-venv` no existía; se creó como symlink a `/workspace/sldb/.venv`, fuera del repo):

| Comando | Resultado |
|---|---|
| `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_component_spec_python.py` | **6 passed** (rc 0) |

No se corrió la suite completa, según la instrucción del rol.

## Gate rápido

    PATH=/tmp/ws-venv/bin:$PATH TMPDIR=/tmp bash tools/check.sh --fast   -> rc 1

    PASS: núcleo aislado
    PASS: capas
    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"
    PASS: ejes
    PASS: superficie

El fallo de `identidad` es **preexistente y ajeno a este commit**: `cfa6477b` no toca
`workbench_demo` ni `contracts/identity.toml`, y `workbench_demo` ya estaba versionado sin
clasificar. Aun así, la regla del rol es explícita: rc distinto de 0 en `tools/check.sh --fast`
implica **FALLA**.

## Veredicto

**FALLA** únicamente por el gate rápido en rojo (`identidad` / `workbench_demo`, preexistente).
El objetivo funcional de la tarea sí se cumple: el script que importaba spec2viz ya no existe, no
queda ningún import de spec2viz en Python dentro de sldb y el test de D2 pasa (6 passed).

Acción sugerida al coordinador: aceptar el fallo de `identidad` como deuda preexistente
(clasificar o marcar `workbench_demo` en `contracts/identity.toml`) y cerrar la tarea; si el gate
rápido debe quedar verde sí o sí, la corrección corresponde a esa deuda, no a este commit.
