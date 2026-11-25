## REFORMULACION

Propósito: que el merge driver de sldb se instale solo al preparar un store y que `stores check` avise si falta. Resultado: `stores init/scaffold/build` llaman a `install_merge_driver` de forma idempotente cuando el store está en un repo git; fuera de git no actúan y, si git falla, avisan sin romper. `stores check` emite el hallazgo `merge-driver-missing` (warning, fix `sldb stores merge-driver --install`) si faltan líneas de `.gitattributes` o claves `merge.sldb.*`. Repo: sldb; rutas `src/sldb/api/stores/{init_store,scaffold_store,build_store,store_check}.py`, `merge_driver_install.py`, tests y CHANGELOG. Límites: fuera deskops y el driver mismo.

## AMBIGUEDADES

1. «cuando el store está dentro de un repo git» / «fuera de git no hacen nada»: no define cómo detectarlo (¿`rev-parse` desde el store o desde cwd? ¿worktrees/submodules?). Obliga a inventar el criterio.
2. «las tres líneas»: no se enumeran. Obliga a inventar patrón, nombre del driver y contenido exacto de `.gitattributes`.
3. «las claves merge.sldb.*»: no se dice cuáles ni con qué valores. Obliga a inventar la comprobación.
4. «avisan sin romper el comando»: no aclara canal ni formato (¿stderr, warning, código 0?) ni qué cuenta como «git falla». Obliga a inventar el manejo de errores.
5. «store_check.py (o el módulo de hallazgos que use)»: no identifica el módulo ni el esquema del hallazgo. Obliga a inventar estructura y nivel.
6. «tests en tests/api/ o tests/store/»: alternativa sin resolver. Obliga a elegir ubicación.
7. La validación solo nombra `tests/store/test_stores_build.py`, pero el plan exige pruebas de init, check e idempotencia; no queda claro el gate. Obliga a inventar cobertura.
8. «commit con rutas nombradas y Task-Id»: formato exacto del mensaje/trailer no definido. Obliga a inventar convención.

## DRY-RUN

Lecturas: TaskDoc, rituales, Board, pills/átomos, `merge_driver_install.py`, `init_store.py`, `scaffold_store.py`, `build_store.py`, `store_check.py`, tests existentes, `.gitattributes` y `git config` de repos, CHANGELOG. Cambios previstos: tests primero en repo git temporal (a–e); luego llamadas idempotentes best-effort; hallazgo warning con fix; CHANGELOG. Dependencias: binario git, `install_merge_driver`, framework de hallazgos, fixtures de git temporal. Validaciones futuras: el pytest indicado; después suite completa, `tools/check.sh --fast`, `stores check`.

## FUTURO

El integrador ejecuta la suite completa y la de deskops; un humano confirma nivel warning y texto del fix; deskops cierra y commitea; la nota de deskops queda fuera; otro nodo revisa el contenido exacto del driver.
