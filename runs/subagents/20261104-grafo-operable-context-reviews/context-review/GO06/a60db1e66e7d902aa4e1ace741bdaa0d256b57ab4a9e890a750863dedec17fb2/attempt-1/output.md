REFORMULACION
GO06 es un nodo `code`/`delivery` del plan grafo-operable, repo dueño sldb, hijo de PK03. Propósito: que una regla sea un documento registrado (`RuleDoc`) con sujeto por familia de modelo, filtro opcional en el lenguaje, condición, severidad (`error|alert`), momento (`on_write|on_transition|on_check`) y mensaje; y exponer `sldb rules check [--subject DOC]` y `sldb rules explain RULE SUBJECT` emitiendo `Finding` por el canal existente. Resultado: modelo, API/CLI, `docs/architecture/rules.md`, reemplazo de la sección Constraint y CHANGELOG. Límites: `output_scope` declarado; depende de GO05 y del gate `G_SEMANTICS` (pending intencional); no autentica actores, no persiste hechos derivados ni ejecuta motores externos; no revisa contratos de vecinos.

AMBIGUEDADES
1. “más un filtro opcional en el lenguaje”: no fija campo, sintaxis ni si filtra antes de la condición; obligaría a inventar esquema y semántica, y la aceptación no lo cubre.
2. “mensaje”: no dice si es obligatorio ni cómo aparece en `Finding`, cuyo “what = la explicación de GO02”; obligaría a inventar uso y validación.
3. “exit 0 si holds, 1 si no”: no define si holds es condición verdadera o ausencia de hallazgo, ni cómo mapea `alert`; obligaría a inventar los exits.
4. “una regla mal formada es rechazada al escribirla con el error del parser”: no delimita si cubre sujeto, filtro, severidad, momento o solo condición; obligaría a inventar la cobertura de validación.

DRY-RUN
Hipotéticamente: leer registro de modelos, `Finding`, API del lenguaje de GO05 y docs; crear `RuleDoc`, API rules, CLI y tests; validar parseo al registrar; actualizar README y CHANGELOG. Dependencias: GO05 y `G_SEMANTICS`. Validaciones futuras: store temporal `Base`, `X < Base`, `Y < X`, `Z < Base`; `error` y `alert` como `Finding`; sin `--subject` solo `on_check`; exits 0/1/2; rechazo de regla mal formada; docs y CHANGELOG. Sin ejecutar.

FUTURO
GO05 produce parser/evaluador y explicación; `G_SEMANTICS` los acepta; GO07 aporta anclas `doc:`; GO08 consume `content_hash` y evalúa `on_write`/`on_check`; la revisión humana acepta el nodo. No son ambigüedades del nodo.
