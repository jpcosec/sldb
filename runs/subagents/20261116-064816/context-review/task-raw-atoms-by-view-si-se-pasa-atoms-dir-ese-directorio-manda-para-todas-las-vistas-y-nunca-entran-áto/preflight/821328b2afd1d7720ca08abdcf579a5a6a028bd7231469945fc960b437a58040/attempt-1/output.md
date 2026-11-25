## REFORMULACION

Propósito: que `raw_atoms_by_view` (src/sldb/api/matching/atoms_by_view.py) use `atoms_dir`, cuando sea truthy, como única fuente de átomos para todas las vistas, sin consultar ningún store; sin `atoms_dir`, mantener el comportamiento actual. Resultado: rama modificada, docstring actualizada, test nuevo en tests/matching/test_matching_refs.py, línea en CHANGELOG.md bajo «## 0.1.13 — not released yet» y aviso a IR. Repo: SLDB_1 (src/sldb, tests/matching). Límites: no cambiar el descubrimiento del store sin `atoms_dir`; el ejecutor no hace push ni commit (lo hace el coordinador); informe en runs/subagents/<run-dir>/result-summary.md.

## AMBIGUEDADES

1. «como cuerpo qué cambió y el commit» frente a «El commit lo hace el coordinador con deskops closeout commit»: el aviso pide un commit que el ejecutor no produce. Obliga a inventar quién envía el aviso y en qué orden.
2. «docstring actualizada»: no fija contenido mínimo ni estilo. Obliga a inventar la redacción.
3. «mensaje "<título corto de la tarea>"»: sin criterio de longitud ni forma de abreviar. Obliga a inventar el truncamiento, aunque lo ejecute el coordinador.
4. «"Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero)»: si el helper vive en otro módulo, no lo cubre. Obliga a decidir importaciones no previstas.

## DRY-RUN

Lecturas: atoms_by_view.py (rama `atoms_dir` y variable `findings`), `grep -rn raw_atoms_by_view tests`, tests/matching/test_matching_refs.py y sus helpers, CHANGELOG.md (encabezado y entradas vecinas). Cambios previstos: si `atoms_dir` es truthy, construir `atoms_by_view` solo desde `parse_atoms(atoms_dir, findings)` para todas las vistas, sin `reader.atoms`; docstring; test con dos vistas (una con store con átomos, otra sin store) más `atoms_dir` con un átomo distinto; línea de CHANGELOG. Dependencias: firma de `parse_atoms`/`findings`, fixtures o `sldb.api` en `tmp_path`, CLI `deskops message send`, registro del repo IR. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/matching/`, encabezado del CHANGELOG, aviso enviado o línea «Aviso a IR» en el informe.

## FUTURO

El coordinador ejecuta `deskops closeout commit` con el mensaje del título corto y, tras el commit, envía `deskops message send --to IR` o registra el fallback en el informe; no hay push. Un humano valida el informe en runs/subagents/<run-dir>/result-summary.md y decide el texto final del commit.
