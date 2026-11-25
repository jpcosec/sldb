## REFORMULACION

Propósito: limpiar el board de sldb cerrando las tareas abiertas cuyo trabajo ya está integrado en `origin/main`, para que el board diga qué falta de verdad. Resultado: cada tarea abierta cuyo goal/done_when ya se cumple queda cerrada con `deskops closeout` en modo resolved-by citando el sha; las demás siguen abiertas con una línea de motivo; informe `result-summary.md` con la tabla tarea → cerrada (sha) / abierta (motivo). Repo: el desk de SLDB (`desk/tasks/`, `Board.md`, rituales, pills). Límites: no implementar nada, no tocar `src/`, no cerrar tareas a medias; commit de desk con `[skip ci]`.

## AMBIGUEDADES

1. "entre 46 y 49 tareas abiertas" — censo incierto; obligaría a inventar el conjunto real.
2. "buscar en git log de origin/main y en el código si su goal ya se cumple" — sin criterio de suficiencia; obligaría a inventar qué cuenta como "cumplido".
3. "con la evidencia que pida el gate" — gate no descrito; obligaría a inventar formato/flag.
4. "(ver deskops closeout --help)" — la sintaxis de resolved-by no está en el input; obligaría a inventar el comando.
5. "deskops list tasks --root ." frente a la validación "--root sldb" — raíz contradictoria.
6. "origin/main" — no dice si se hace `fetch`; obligaría a inventar el estado del remoto.
7. "result-summary.md" — ruta no especificada; obligaría a inventar dónde vive.
8. "commit de desk con [skip ci]" frente a closeout por tarea — ¿un commit por cierre o uno final?
9. "una línea en el informe que dice por qué" — granularidad del motivo no acotada.
10. "las que no, siguen abiertas" — ¿se reordenan/re-etiquetan o quedan intactas?

## DRY-RUN

Lecturas: `Board.md`, cada TaskDoc, rituales execution/testing/closeout, pills, `git log --grep`/`-S` sobre `origin/main`, código citado y `deskops closeout --help`. Cambios previstos: N closeouts resolved-by con sha, `result-summary.md`, un commit de desk con `[skip ci]`. Dependencias: deskops con modo resolved-by y gate; `origin/main` accesible. Validaciones futuras: `deskops graph missing` → 0, `deskops list tasks`, árbol limpio, `closeout verify`.

## FUTURO

JP o el supervisor decide qué tareas cuentan como "ya cumplidas" cuando el criterio no es binario, y si se aceptan cierres sin gate. Otro nodo o humano confirma el `fetch` y la ubicación del informe.
