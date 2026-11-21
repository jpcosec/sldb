FALLA

# Testing — doc del árbol del CLI y chequeo en selfdoc

Commit verificado: `b8e564c2956f1bf7f0ba8d1d942862231a85bf1f` — `selfdoc check compara el árbol argparse con current-cli-tree.md`
(`Task-Id: task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a`).

## Veredicto

**FALLA solo por la puerta rápida del desk.** `bash tools/check.sh --fast` termina con **rc 1**: la puerta
`identidad` falla por el directorio `workbench_demo`, incorporado en `562847e2` (anterior al commit del
ejecutor) y fuera de este cambio. Las demás puertas de `--fast` (núcleo, capas, ejes, superficie) pasan.

El ejecutor dejó constancia en `runs/subagents/exec-deskops-e-b6f9a76678a1/result-summary.md` de que el
coordinador autorizó commitear con esa puerta en rojo *solo* por `workbench_demo`, con la clasificación
pendiente como decisión aparte. Aun así, la regla del rol de testing es explícita: rc distinto de 0 en
`check.sh --fast` ⇒ FALLA. **Si el coordinador acepta formalmente esa roja preexistente como excepción, el
veredicto funcional de este commit es PASA.**

## Verificación funcional (todo en verde)

Entorno: `/tmp/ws-venv` no existe en este contenedor; usé `/workspace/sldb/.venv/bin/python` (Python 3.13.18,
pytest 9.1.1), `TMPDIR=/tmp`. No corrí la suite completa.

| Comando / comprobación | Resultado |
|---|---|
| `python -m pytest -q tests/selfdoc/test_parser.py` (archivo del commit) | **7 passed** |
| `python -m sldb selfdoc check` | **rc 0**, `ok: true`, `cli_tree_missing: []`, `cli_tree_stale: []` |
| `python -m pytest -q tests/test_clean_code_rules.py` | **1236 passed** |
| `python -m pytest -q tests/selfdoc/test_sync.py` (módulo `selfdoc.py` tocado) | **5 passed** |
| `bash tools/check.sh --fast` | **rc 1**; falla solo `identidad` por `workbench_demo` |

Además comprobé el árbol exacto contra el parser: 158 rutas reales y 158 dibujadas (más `help`, que ambos
lados excluyen). La doc padre dibujaba 73 y le faltaban exactamente las **85** rutas que menciona el CHANGELOG.

## Comprobación de detección con la doc real (no solo los tests del ejecutor)

Edité temporalmente `docs/architecture/current-cli-tree.md` y la restauré con `cmp` OK:

- Borrar `├── bench`: `selfdoc check` sale **rc 1** y emite `selfdoc/cli-tree-missing` con `subject: "bench"`.
- Agregar `├── ghost` / `│   └── haunt`: sale **rc 1** y emite `selfdoc/cli-tree-stale` con
  `subject: "ghost"` y `subject: "ghost haunt"`; `report.ok` es falso.

También verifiqué en código que el chequeo corre para `check` y `sync`, solo con el factory propio y si la
doc existe; los alias y `help` no cuentan, y las rutas se arman por indentación del bloque ```text.

## Archivos del commit revisados

`CHANGELOG.md`, `docs/architecture/current-cli-tree.md`, `src/sldb/cli/commands/selfdoc.py`,
`src/sldb/selfdoc/cli_tree.py` (nuevo), `src/sldb/selfdoc/report.py`,
`src/sldb/selfdoc/report_findings.py`, `tests/selfdoc/test_parser.py`. No modifiqué ni commiteé el checkout.
