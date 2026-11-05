## REFORMULACION

**Propósito:** definir `RuleDoc` como documento con sujeto por familia de modelo (`model <= X`), `where` opcional, condición, severidad, momento y mensaje; validarlo al escribir y exponer `rules check` y `rules explain`.

**Resultado:** modelo y validación, comandos CLI con `Finding`, documentación en `docs/architecture/rules.md`, actualización de `bridge_primitives/README.md` y CHANGELOG.

**Repo:** sldb.

**Límites:** no evalúa en escritura, transición ni `stores check` (GO08); no define anclas `doc:` ni `anchor_state` (GO07); no persiste hechos derivados; no autentica actores.

## AMBIGUEDADES

1. **Contradicción sobre `Finding.what` con `message`.** El scope dice: «si existe, Finding.what = message seguido de la explicación de GO02; si no, solo la explicación», pero después afirma: «what = la explicación de GO02». Obliga a inventar si `message` se antepone, reemplaza o se ignora; la aceptación no lo cubre.
2. **Exit code de `rules check` no definido.** Se especifica «exit 0 si la condición es true, 1 si false, 2 si incomplete» solo para `rules explain`; para `rules check` no se dice qué exit produce un finding `error`, un `alert` o ninguno. Obliga a inventar la semántica de salida del comando.
3. **Formato de `--subject DOC` no definido.** «sldb rules check [--subject DOC]» no indica si `DOC` es `Model:name`, una ruta u otra forma. Obliga a inventar el parseo del argumento.

## DRY-RUN

**Lecturas:** contrato de GO05 (parser/evaluador y explicación), especificación de GO02, registro de modelos y `base_models`, `core/finding.py`, envelope CLI existente, `docs/architecture/` y README de bridge primitives.

**Cambios previstos:** crear `rule_doc.py` con campos y validación; crear API y CLI `rules check`/`rules explain`; emitir `Finding` por el canal existente; documentar y actualizar CHANGELOG.

**Dependencias:** GO05 y el gate `G_SEMANTICS` (pendiente); el canal `Finding`; no depende de GO07 ni GO08.

**Validaciones futuras:** store temporal con `Base`, `X < Base`, `Y < X`, `Z < Base`; findings `error`/`alert` con cláusula y nodo; `check` sin `--subject` solo `on_check`; exits 0/1/2 de `explain`; exclusión por `where`; rechazo de reglas mal formadas; docs y CHANGELOG.

## FUTURO

GO05 entrega el lenguaje y la explicación; GO07 entrega anclas y `anchor_state`; GO08 consumirá el `content_hash` de `RuleDoc` en su caché y evaluará en escritura, transición y check; un humano o el desk de sldb acepta la revisión y resuelve `G_SEMANTICS`; deskops consumirá estas capacidades en su propio plan.
