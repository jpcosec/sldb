REFORMULACION
Tarea de decisión (`task.decision`), no un agregado: un ejecutor debe obtener de JP la decisión 6 entre (a) extraer el store de sldb a paquete propio o (b) conservar el desacople interno ya hecho (beb8a99c; tres costuras y `tests/test_store_seams.py`). Resultado: sección "Decisión 6" en `docs/architecture/store-extraction-proposal.md` con fecha ISO, línea de `desk/STANDARDS.md` ya no pendiente, recibo owner accepted por JP y, si (a), tarea de refactor creada. Repo: sldb (`/mnt/ssd/proyectos/SLDB_1`). Límites: no mover código, no hacer push salvo el integrador, no cerrar sin recibo aceptado.

AMBIGUEDADES
1. "por el canal de coordinación (herdr o el supervisor)" — no fija cuál; obligaría a inventar el mecanismo concreto de contacto.
2. "`deskops review record <esta tarea>`" — el placeholder no da id; obligaría a inferir que es el del frontmatter, sin confirmación.
3. "se crea la tarea de refactor que inyecta las tres costuras" — "inyecta" no está definido operativamente; obligaría a inventar alcance del refactor.
4. "El commit del documento lo hace el coordinador con `deskops closeout commit`" — no aclara si ese commit incluye `desk/STANDARDS.md` o si va aparte; obligaría a inventar la política de staging.

DRY-RUN
Un ejecutor futuro leería `docs/architecture/store-extraction-proposal.md`, `desk/STANDARDS.md` y `tests/test_store_seams.py`; pediría la decisión por el canal indicado; escribiría el encabezado "## Decisión 6", la línea "Decisión (AAAA-MM-DD, JP): <opción>", "Motivo: ..." y la lista de opciones con costo; editaría la línea de STANDARDS.md a "Decisión 6 (...): ...; ver docs/..."; registraría el recibo owner; crearía la tarea de refactor si (a); validaría con `grep -n 'Decisión 6'` y `TMPDIR=/dev/shm pytest -q tests/test_store_seams.py`; haría el commit. Dependencias: respuesta de JP, CLI deskops, canal de coordinación.

FUTURO
JP responde y ejecuta el `dispose accepted`; el coordinador realiza el `closeout commit`; el integrador hace push; si (a), otro nodo ejecuta el refactor.
