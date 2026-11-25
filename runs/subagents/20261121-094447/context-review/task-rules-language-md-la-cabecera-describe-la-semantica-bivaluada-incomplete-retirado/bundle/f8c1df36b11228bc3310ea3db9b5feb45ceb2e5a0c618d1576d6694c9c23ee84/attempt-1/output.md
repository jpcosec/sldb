## REFORMULACION

**Propósito:** cerrar el defecto documental residual del retiro de `incomplete`: la cabecera de `docs/architecture/rules-language.md` aún afirma semántica trivaluada aunque el cuerpo (§3) describe el lenguaje como bivaluado.

**Resultado:** cabecera (líneas 3-8) dice “la semántica bivaluada” y añade una frase que remite a la nota de retiro de `incomplete` en §3; `git grep -n -i 'trivaluad' -- docs/ knowledge/` no devuelve afirmaciones vigentes; menciones históricas marcadas como tales.

**Repo:** `sldb`, worktree que entregue dispatch, rutas `docs/` y `knowledge/`.

**Límites:** dentro, `docs/architecture/rules-language.md` y demás archivos de `docs/`/`knowledge/` que el grep muestre afirmando trivaluada como vigente; `knowledge/` se regenera con `sldb selfdoc sync`. Fuera: código y tests. Nodo ejecutable, no agregado.

## AMBIGUEDADES

1. “docs/architecture/rules-language.md:5 sigue diciendo” frente a “La cabecera … (líneas 3-8) dice”: no queda fijada la línea exacta ni la frase literal; obligaría a inventar la redacción precisa.
2. “agrega una frase que remite a la nota de retiro de incomplete en §3”: no se especifica texto ni forma de remisión; obligaría a inventar la frase.
3. “las menciones históricas tienen que decir que es historia”: no define qué marca cumple ese requisito; obligaría a inventar el criterio.
4. “sldb selfdoc check sin alertas nuevas”: no fija baseline de alertas; obligaría a inventar contra qué comparar.
5. “Validation” solo lista pytest, mientras “Done When” exige también el grep y “Implementation Path” p3 exige selfdoc check: no aclara cuáles son puertas obligatorias; obligaría a inventar la jerarquía.

## DRY-RUN

**Lecturas:** TaskDoc, rituales execution/testing/closeout, Board, `docs/architecture/rules-language.md` (cabecera y §3), `git grep -n -i 'trivaluad' -- docs/ knowledge/`, `tests/test_rules_language_spec.py`.

**Cambios previstos:** editar cabecera; corregir menciones vigentes halladas; regenerar `knowledge/` con `sldb selfdoc sync` (no a mano); commit acotado con trailer `Task-Id`.

**Dependencias:** worktree de dispatch, CLI `sldb selfdoc`, pytest, git.

**Validaciones futuras:** grep sin afirmaciones vigentes; `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_rules_language_spec.py`; `sldb selfdoc check`; commit con rutas explícitas.

## FUTURO

Dispatch entrega el worktree; un humano autoriza la excepción de la puerta “identidad” (`f055723d`); `deskops closeout` retira la tarea del Board; el resultado de `selfdoc sync` determina qué archivos de `knowledge/` entran en el commit.
