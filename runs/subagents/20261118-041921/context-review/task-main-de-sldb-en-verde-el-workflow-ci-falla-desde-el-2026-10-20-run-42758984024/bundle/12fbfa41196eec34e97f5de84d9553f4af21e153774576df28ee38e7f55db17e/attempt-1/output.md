## REFORMULACION
Encargo: hacer que el job `store` del CI de sldb construya el store una sola vez y termine con holgura dentro de las 6 h, sin perder las comprobaciones de `stores build --check` ni `selfdoc check`. Resultado: workflow CI en success sobre main (jobs test 3.12, test 3.13 y store), con informe de causa confirmada, opción elegida, tiempos y número de builds antes/después. Repo: sldb en `/mnt/ssd/proyectos/SLDB_1/sldb`, rama main local, sin push; superficie: `.github/workflows/ci.yml`, `src/`, `tests/`, `CHANGELOG.md`. Límites: confirmar la hipótesis en código antes de cambiar; nada de skip/xfail/timeouts; no optimizar símbolos salvo lo necesario; no tocar deskops, pron, trabajo ajeno ni stash; commits con rutas nombradas.

## AMBIGUEDADES
1. “runs/subagents/exec-<nombre del agente scion>/result-summary.md; el brief del ejecutor trae la ruta exacta”: el input no incluye brief ni nombre; obligaría a inventar la ruta exacta del informe.
2. “gh run list --repo jpcosec/sldb --commit <sha integrado> --json status,conclusion,url: success en test 3.12, test 3.13 y store”: `gh run list` devuelve conclusión del run, no de cada job; obligaría a inventar cómo verificar los tres jobs o asumir que la conclusión global basta.

## DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout, `.github/workflows/ci.yml`, código de `stores build --check`, `selfdoc check`, tests y git history. Cambios previstos: editar `ci.yml` para un único build (preferencia p2a, justificando equivalencia con `--check`; si no, p2b); posible test, CHANGELOG e informe. Dependencias: clones de deskops main, pron master y sldb; venv; `/dev/shm/sci`; `gh` y credenciales del integrador. Validaciones futuras: reproducción cronometrada antes/después, build de referencia, exactamente un build, total ≤1,2× referencia, `bash tools/check.sh --fast`, suite completa por el integrador y run CI del sha integrado. Sin ejecutar nada.

## FUTURO
El integrador (`wA:p1`) corre la suite en copia limpia, pushea con jpcosec y aporta el sha integrado y la URL del run; el despacho debe aportar la ruta exacta del informe. Si `--check` y la sustitución no verifican lo mismo, el ejecutor para y un humano decide. Otro nodo cierra la tarea con la URL en references.
