REFORMULACION
Propósito: dejar en verde el workflow CI de sldb en main, atacando el job store, que se cancela a las 6 h porque `stores build --check` reconstruye en scratch y el paso siguiente vuelve a construir. Resultado: job store con un solo build completo, dentro de holgura de 6 h y sin perder las comprobaciones de `--check` ni `selfdoc check`. Repo/checkout: `/mnt/ssd/proyectos/SLDB_1/sldb`, rama main local; no push. Límites: no skip/xfail/timeouts; no tocar deskops/pron ni trabajo ajeno (`surface/`, stash); commit con rutas nombradas; informe en `runs/subagents/<run>/result-summary.md`. Nodo ejecutable, no agregado.

AMBIGUEDADES
1. "informe en runs/subagents/<run>/result-summary.md": el placeholder `<run>` no está resuelto; obliga a inventar el identificador exacto del directorio.
2. "tiempo total de los pasos del job store": no define qué pasos ni desde/hasta cuándo se cronometran (checkout, setup, preparación de stores, build, selfdoc); obliga a inventar el perímetro de medición.
3. "1,2 veces el de un solo build": no fija qué build es la referencia (antes/después, con/sin symbols); obliga a inventar la línea base.
4. "el clon toma su rama local con git fetch y checkout de ese sha": no indica remoto/ruta para obtener un commit local no pusheado; obliga a inventar el mecanismo.

DRY-RUN
Lecturas: task doc, referencias de inbox, `.github/workflows/ci.yml`, código de `sldb stores build --check`, ayuda CLI, estado del repo. Cambios previstos: confirmar causa; elegir (a)/(b) con evidencia; editar workflow y/o añadir opción `stores build` con test; commit por rutas nombradas. Dependencias: venv, clones en `/dev/shm/sci`, `gh`, permisos de workflow (integrador). Validaciones futuras: reproducción local con rc 0, un build y tiempo <=1,2×; `tools/check.sh --fast`; suite completa por integrador en copia limpia; CI del commit integrado en success.

FUTURO
El integrador (`wA:p1`) ejecuta la suite completa en copia limpia, pushea con `jpcosec` y aporta la URL del run; un humano decide si hay cambio de diseño o si `--check` no es sustituible equivalentemente.
