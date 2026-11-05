## REFORMULACION
Encargo ejecutable de código en el repo `sldb` (worktree propio): separar físicamente el store en `.sldb/` operacional y versionado —`store.yaml` y `core/`— y `.sldb_cache/`, hermano en la raíz, regenerable e ignorado. Debe ajustar `layout.py` (`runtime_dir`), la política de `.gitignore`, `stores init/build/check`, añadir `stores migrate-layout`, retirar el escritor del journal, convertir `journal show` en aviso, reescribir dos docs, añadir un atom, tests y CHANGELOG. Límites: no migra los cuatro stores hermanos ni envía avisos por inbox —lo hará el supervisor—; no inventa API ante contratos ausentes: registra la hipótesis en el TaskDoc.

## AMBIGUEDADES
1. «se niega si .sldb_cache/ existe y no esta vacia salvo --force»: no define si `--force` sobrescribe, fusiona o borra; obligaría a inventar la política de conflicto.
2. «quita las lineas que ignoran .sldb/core/ y .sldb/runtime/»: no fija variantes (`core`, `/core/`, `**/core`), comentarios ni negaciones; obligaría a inventar el parser.
3. «un comando nuevo stores migrate-layout»: no especifica argumentos, store objetivo ni descubrimiento; obligaría a inventar su interfaz CLI.
4. «un atom con la regla»: no indica id, esquema ni texto; obligaría a inventar el atom.
5. «pasa a imprimir un aviso que remite a sldb docs history»: no fija mensaje ni exit code; obligaría a inventar contrato observable.
6. «runtime_dir pasa a .sldb_cache/, hermano de .sldb/ en la raiz del repo»: no define cómo resolver la raíz si el store no está en ella; obligaría a inventar esa resolución.

## DRY-RUN
Lecturas: TaskDoc, `layout.py`, `gitignore_policy.py`, CLI `stores`, `finding.py`, `store/journal/`, docs, tests y CHANGELOG; localizar referencias al journal y supuestos de layout. Cambios previstos: nuevo `runtime_dir`; política idempotente de `.gitignore`; `init/check` con los Findings indicados; `migrate-layout` con movimiento atómico, negativa y `--force`; retirada del escritor; aviso en `journal show`; docs, atom, tests y CHANGELOG. Dependencias: registro CLI, API de Findings, resolución de raíz git, atomicidad del movimiento y tests del layout anterior. Validaciones futuras: `pytest -q tests -k 'layout or gitignore or stores or migrate or journal'`, casos de migración, journal ausente y suite completa en robocop2.

## FUTURO
El supervisor revisa el worktree, ejecuta la suite completa en robocop2, migra los cuatro stores hermanos con `stores migrate-layout`, emite avisos por inbox y cierra junto a `task-congelar-journal-autoridad-arbol`.
