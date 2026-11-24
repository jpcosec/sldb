FALLA

# Testing — Plan del drawer grafo-datalog-daemon: motor Datalog dueño de las aristas (revierte D5) y daemon residente de sldb

Commit del ejecutor: `26993e7d2966997e4d8f97da1a212dad07529a15` — «Plan grafo-datalog-daemon (portado de e5f7b702): motor Datalog duenio de las aristas y daemon; D5 revertida; 4 task.decision para JP», con el trailer `Task-Id` correcto. El commit es de documentación y plan: no toca código de producción (`src/` ni `tests/`).

## Veredicto

**FALLA por la puerta rápida obligatoria.** `bash tools/check.sh --fast` termina con **rc 1**: la puerta `identidad` rechaza el directorio versionado `workbench_demo` («directorio versionado sin clasificar en la raíz»). La regla del rol de testing es explícita: rc distinto de 0 en `check.sh --fast` ⇒ FALLA. Las demás puertas pasan (`núcleo aislado`, `capas`, `ejes`, `superficie`).

La violación es **preexistente y ajena a este commit**: `workbench_demo` ya está versionado en el padre `26993e7d^`, `contracts/identity.toml` no lo clasifica, y el commit no toca ni ese directorio ni el contrato (verificado con `git ls-tree 26993e7d^ workbench_demo` y `git diff 26993e7d^ 26993e7d -- contracts/identity.toml workbench_demo`, vacío). Es la excepción autorizada `f055723d`, todavía pendiente de la decisión de JP.

**Veredicto funcional: PASA.** Si el coordinador acepta formalmente esa excepción preexistente, el contenido del plan cumple el Goal y el Done When: el plan existe, el `dag.yaml` se lee con el lector de `deskops review node`, el informe trae la tabla de tiempos y memoria de la PoC contra el camino actual, D5 figura revertida con fecha y motivo, y hay una `task.decision` por cada decisión abierta (con opciones y recomendación). No encontré un defecto de contenido que impida cerrar.

## Trabajo localizado

- Commit: `26993e7d2966997e4d8f97da1a212dad07529a15` (23 archivos).
- Plan: `desk/drawer/plans/grafo-datalog-daemon/{alcance.md,brief.md,decisiones.md,dag.yaml}`.
- PoC: `desk/drawer/plans/grafo-datalog-daemon/poc/{informe.md,poc_datalog.py,resultado-actual.json,resultado-cozo-mem.json,resultado-cozo-sqlite.json}`.
- D5: `desk/drawer/plans/grafo-operable/decisiones.md` (fila D5 marcada como revertida el 2026-11-23 y fila D5-rev con el motivo).
- Decisiones: 4 `task.decision` en `desk/tasks/` y en el Board/store (P1 motor, P2 propiedad del motor, P3 forma del daemon, P4 invalidación).

## Tests

No hay `tests/*.py` en el commit, ni módulos de `src/` tocados. El único código es `poc/poc_datalog.py`, un script de prueba de concepto, y no existe `tests/test_poc_datalog.py`; por eso no hay pytest aplicable. Se exportó igual `PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-ce2a38aef5ba"`, según el instructivo.

## Qué se verificó

| Chequeo | Resultado |
|---|---|
| `git log -1 --grep "Task-Id: …"` | `26993e7d2966997e4d8f97da1a212dad07529a15` |
| `git show --name-only` | 23 archivos; 0 en `tests/`, 0 en `src/` |
| `deskops graph missing --root .` | 12 faltantes, **todos** de `.worktrees/deskops-e-26633313df8f/.sldb/...` (worktree anidado del ejecutor); ninguno del plan ni de las task.decision. El `validation.log` del ejecutor registra «No missing graph references found» a las 07:16. No hay faltantes atribuibles al commit. |
| `dag.yaml` con el lector de `deskops review node` | parsea; 11 nodos (`ROOT`, `PK01..03`, `DL01..07`), 5 gates y 7 tareas; `execution_authorized: false` |
| D5 revertida | `grafo-operable/decisiones.md`: fila D5 «Revertida por JP el 2026-11-23» y fila D5-rev con motivo; `grafo-datalog-daemon/decisiones.md` también |
| `task.decision` | 4 registradas en el Board/store, cada una con opciones A/B/C y recomendación |
| PoC `report` desde los JSON del commit | reproduce la tabla del informe |
| PoC `facts` re-ejecutado | 39.639 nodos, 230.140 aristas, 7.840 docs, 337 átomos, 35,95 s de primera carga (informe: 39.639 / 230.655 / 7.829 / 337 / 40,0 s) |
| PoC `current` re-ejecutado | terminó; mismas respuestas: 2.557 aristas del nodo, 68 descendientes, 337 átomos, 0 stale. Ver «Observaciones» por los tiempos. |
| Cozo | los pasos Cozo no se re-ejecutaron: `cozo_embedded` no está instalado en el venv; el informe documenta `uv pip install cozo-embedded`. `facts`, `current` y `report` no lo requieren. |

## Observaciones (no gobiernan el veredicto de la puerta, pero el coordinador debería verlas)

1. **Tiempos del camino actual en este contenedor.** La corrida re-ejecutada de `current` tardó **756,9 s** en las 50 consultas sueltas (`13,7 s` por recomposición/live-stale), no los 49,08 s del informe; la carga también fue 34,7 s contra 3,04 s. Las respuestas coinciden. La causa parece ser la carga/concurrencia del workspace (el conteo de aristas del índice cambió entre llamadas), no el script; el propio informe ya señala que la ganancia está en no recomponer y que la composición sigue costando 3 a 40 s.
2. **Metodología de la PoC frente al preflight aceptado.** El preflight pedía 10 nodos al azar con semilla fija, 3 repeticiones y mediana, RSS con `/usr/bin/time -f %M`, y scripts en `reports/grafo-datalog-daemon-20261123/`. El informe usa un nodo «busy» y un «hub», mejor de 5, una corrida por medida, RSS de `/proc/self/status`, y deja el script en `.../poc/`. El Scope de la tarea permite `reports/ o en el plan`, así que la ubicación no es un defecto; la metodología sí se aparta de la resolución del preflight. Queda a criterio del coordinador si la tabla actual alcanza para la decisión de JP.
3. **Comparación de motores.** El informe cubre cliente Python, Datalog y almacenamiento embebido, pero no compara licencias ni el mantenimiento/estabilidad de todos los candidatos más allá de la salvedad sobre Cozo; el preflight los pedía como criterio. La decisión P1 queda abierta para JP.
4. **`deskops graph missing`**: los 12 faltantes vienen de un worktree anidado (`.worktrees/deskops-e-26633313df8f`) que se recreó después del commit; no están en los archivos del commit. Si el coordinador corre el comando en este workspace, los verá; conviene limpiar/retirar ese worktree antes de la foto de cierre.

## Entorno

No existe `/tmp/ws-venv` en este contenedor; se usó el venv del repo (`.venv`, Python 3.13.18, pytest 9.1.1) con `PYTHONPATH=src`, `TMPDIR=/tmp` y `PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-ce2a38aef5ba"`.

## Gate rápido (detalle)

```
── núcleo aislado ── PASS
── capas ── PASS (10 paquetes, 38 aristas, 0 violaciones)
── identidad ── FAIL: directorio versionado sin clasificar en la raíz: workbench_demo
── ejes ── PASS (32 declarados, 1001 archivos mapeados, 0 violaciones)
── superficie ── PASS (129 símbolos pedidos, 597 declarados, 0 violaciones)
omitidas (--fast): afirmaciones pruebas selfdoc
FALLAN: identidad
RC=1
```

Log completo: `runs/subagents/exec-deskops-t-ce2a38aef5ba-testing/validation.log`.
