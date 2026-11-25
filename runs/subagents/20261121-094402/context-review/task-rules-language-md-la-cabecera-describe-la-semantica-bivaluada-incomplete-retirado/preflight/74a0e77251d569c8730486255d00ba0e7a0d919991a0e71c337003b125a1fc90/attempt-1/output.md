## REFORMULACION
Nodo ejecutable, no agregado. **Propósito:** corregir `docs/architecture/rules-language.md` para que su cabecera declare la semántica bivaluada y remita a la nota de retiro de `incomplete` en §3, eliminando afirmaciones vigentes de semántica trivaluada en `docs/` y `knowledge/`. **Resultado:** cabecera actualizada, `git grep` sin afirmaciones vigentes y test indicado en verde. **Repo:** `/mnt/ssd/proyectos/SLDB_1/sldb`. **Límites:** solo `docs/` y `knowledge/`; `knowledge/` se regenera con `sldb selfdoc sync`, no a mano; código y tests quedan fuera; commit desde el worktree de dispatch con trailer `Task-Id`; excepción autorizada: identidad de `check.sh --fast` en rojo por `workbench_demo` (f055723d).

## AMBIGUEDADES
1. “agrega una frase que remite a la nota de retiro de incomplete en §3”: no fija texto ni ubicación exacta; obliga a inventar redacción y punto de inserción.
2. “cualquier otro archivo de docs/ o knowledge/ que el grep muestre afirmando la semántica trivaluada como vigente”: “afirmando… como vigente” exige un criterio editorial no definido; obliga a decidir qué mención es histórica.
3. “sldb selfdoc check sin alertas nuevas”: no da línea base; obliga a inventar contra qué ejecución se comparan las alertas.
4. “Validation” solo lista pytest, mientras “Implementation Path” p3 pide `selfdoc check` y “Done When” pide grep: no queda claro qué compuertas cierran la tarea; obliga a elegir.

## DRY-RUN
**Lecturas:** TaskDoc; cabecera de `docs/architecture/rules-language.md` (3-8) y §3 (167-188); `git grep -n -i 'trivaluad' -- docs/ knowledge/`; estado del worktree. **Cambios previstos:** editar cabecera a bivaluada y añadir frase hacia §3; corregir menciones vigentes; en `knowledge/`, regenerar con `selfdoc sync`. **Dependencias:** worktree de dispatch, git, selfdoc, pytest y `TMPDIR=/tmp`. **Validaciones futuras:** grep sin afirmaciones vigentes, pytest indicado, `selfdoc check`, commit con trailer; `check.sh --fast` con identidad roja aceptada. Sin ejecutar.

## FUTURO
Dispatch entrega el worktree; las herramientas ejecutan git/selfdoc/pytest; un humano o la política correspondiente acepta la excepción de identidad y revisa el commit y el resultado documental.
