## REFORMULACION

**Propósito:** que sldb registre la decisión de frontera D1: sldb evalúa reglas declaradas y los consumidores las autoran como documentos. **Resultado:** un atom nuevo en `desk/atoms`, la pill enlazada en `where` o `how`, dos commits en main —el primero con atom y pill; el segundo editando solo `gates.G_BOUNDARY` a `satisfied` con el hash del primero como evidence— y una nota a `deskops/desk/inbox` vía `deskops message send`. **Repo dueño:** sldb; la nota es la única escritura fuera, en deskops. **Límites:** no cambia código; no toca otros documentos de deskops; sin amend; solo `gates.G_BOUNDARY` en `dag.yaml`.

## AMBIGUEDADES

1. «cuyo answer diga que sldb evalúa reglas declaradas sobre documentos, aristas y hashes y que los consumidores las autoran como documentos» frente a «el atom aparece en la pill»: la aceptación no comprueba el contenido del answer. El ejecutor debe inventar la redacción y no hay criterio comprobable de que el answer diga eso.

2. «la pill enlaza el atom en su campo where o how» frente a «el atom aparece en la pill»: la aceptación no exige enlace ni campo. Obliga a decidir si una mención textual basta y permite pasar sin cumplir el enlace.

3. «con el hash del primero como evidence» / «evidence con el hash del primer commit»: no fija hash completo o abreviado; obliga a elegir formato.

## DRY-RUN

Un ejecutor leería la pill, la fila D1 de `decisiones.md`, `dag.yaml` y el estado de main. Crearía el atom con `--title`, `--five-wh-one-plus what` y `--answer`; editaría la pill en `where` o `how`; haría el commit 1; editaría solo `gates.G_BOUNDARY` con `state: satisfied` y evidence; haría el commit 2; enviaría la nota con título y cuerpo de dos párrafos. Dependencias: pill rev 5 ya commiteada, main limpio, CLI de deskops y permiso de escritura en inbox. Validaciones futuras: `git log`/alcanzabilidad, contenido del atom y de la pill, archivo de inbox con título y cuerpo, gate y evidence, ausencia de amend.

## FUTURO

GO02 consume `G_BOUNDARY` para fijar la semántica del lenguaje. deskops lee la nota en su inbox y decide su propio plan. El operador del desk de sldb escribe la disposición de esta revisión (D3).
