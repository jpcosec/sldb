## REFORMULACION

GO01 es un nodo `delivery` de decisión, hijo de PK01, en el repo sldb. Su propósito es dejar registrada la frontera: sldb evalúa reglas declaradas y los consumidores las autoran. El resultado esperado es la pill reescrita commiteada en `main` de sldb, un atom en `desk/atoms/` enlazado desde la pill, y una nota en el inbox de deskops anunciando el reencuadre y el plan. Límites: no cambia código; su alcance son la pill, el atom y la nota. La aceptación exige esos tres artefactos y que G_BOUNDARY cite el commit.

## AMBIGUEDADES

1. **"nota al inbox de deskops"** y **"deskops tiene la nota en su inbox"**: no se define si la nota se escribe como archivo/commit en el repo deskops, se entrega con una CLI, o quién es el actor autorizado. GO01 es de `owner_repo: sldb`, pero su `output_scope` incluye "inbox de deskops". Además, brief.md §Fuera de alcance dice "tocar deskops". Obliga a inventar el procedimiento cross-repo y el criterio de verificación.

2. **"G_BOUNDARY cita el commit"** frente a la misma fuente, donde G_BOUNDARY figura `state: satisfied` y su evidencia dice "commit pendiente en este plan". Obliga a decidir si el gate ya está satisfecho o si GO01 debe reabrirlo/actualizarlo para citar el commit.

## DRY-RUN

Un ejecutor futuro leería la pill reescrita, las convenciones de `desk/atoms/` y el mecanismo vigente del inbox de deskops. Luego: commitearía la pill en `main` de sldb, crearía el atom con la afirmación de frontera, añadiría el enlace desde la pill y entregaría la nota a deskops. Dependencias: ninguna arista `depends_on`; `requires: G_BOUNDARY`, ya marcado satisfecho. Validaría que la pill y el atom estén en `main`, que el enlace exista y que la nota sea visible en el inbox de deskops; finalmente G_BOUNDARY debería citar el hash del commit. No ejecutaría tests de código porque el nodo no cambia código.

## FUTURO

GO02 y GO03 consumen G_BOUNDARY como prerrequisito. PK01 cierra cuando G_BOUNDARY, G_SEMANTICS y G_SEAM estén satisfechos. El plan de deskops, aún inexistente, producirá G_CONSUMER; ahí se verificará el consumo real del reencuadre. La confirmación de D5, D6 y D7 corresponde al dueño, no a GO01.
