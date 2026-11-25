## REFORMULACION

Encargo: higiene del board del repo `sldb` (desk). Propósito: que el board refleje el trabajo realmente pendiente. Resultado: cerrar con `deskops closeout` en modo `resolved-by`, citando el sha de `origin/main` que resuelve cada tarea abierta cuyo goal y done_when ya se cumplen; las demás quedan abiertas con motivo. Entregable: `result-summary.md` con tabla tarea → cerrada (sha) / abierta (motivo). Límites: no implementar nada, no tocar `src/`, no cerrar tareas a medias. Nodo ejecutable (`task.code`), no agregado.

## AMBIGUEDADES

1. `"deskops list tasks --root ."` frente a `"deskops list tasks --root sldb"`: no queda fijado el directorio de trabajo ni la raíz; obligaría a inventar desde dónde se ejecuta.
2. `"entre 46 y 49 tareas abiertas"`: rango sin cifra cierta; obligaría a inventar el universo exacto a recorrer.
3. `"si su goal ya se cumple"`: criterio de cumplimiento no operacionalizado; obligaría a inventar el umbral de evidencia.
4. `"con la evidencia que pida el gate"`: se desconoce qué exige el gate de `closeout`; obligaría a inventar campos/argumentos.
5. `"deskops graph missing en 0"` / validación `"deskops graph missing --root sldb"`: no se especifica salida esperada ni formato; obligaría a inventar la condición de éxito.
6. `"commit de desk con [skip ci]"`: no se indica repo, rama ni mensaje; obligaría a inventar destino del commit.
7. `"result-summary.md"`: sin ruta; obligaría a inventar ubicación.
8. `"buscar en git log de origin/main"`: no se indica `fetch` previo; obligaría a decidir si se actualiza la ref.

## DRY-RUN

Lecturas: `deskops list tasks --root sldb` (abiertas), `deskops closeout --help`, contratos de cada tarea, `git log --grep`/`-S` y código en `origin/main`. Cambios previstos: invocaciones de `closeout` modo `resolved-by` con sha y evidencia; creación de `result-summary.md`; commit del desk con `[skip ci]`. Dependencias: `deskops` disponible, `origin/main` accesible, gate de cierre. Validaciones futuras: `deskops graph missing` = 0 y `deskops list tasks`. Sin ejecutar nada.

## FUTURO

Un humano/supervisor confirma qué tareas están realmente resueltas y valida el informe; el gate de `closeout` devuelve su veredicto; otro nodo puede aportar el sha exacto o el `fetch` de `origin/main`.
