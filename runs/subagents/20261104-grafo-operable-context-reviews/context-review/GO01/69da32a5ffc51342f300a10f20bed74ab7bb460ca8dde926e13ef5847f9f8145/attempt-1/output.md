## REFORMULACION
GO01 es un nodo de entrega ejecutable, no un agregado. Su propósito es registrar en sldb la decisión de frontera D1: un atom nuevo que afirme que sldb evalúa reglas declaradas sobre documentos, aristas y hashes y que los consumidores las autoran como documentos, enlazado desde la pill ya reescrita. El resultado son dos commits en main de sldb —el primero con atom y pill enlazada; el segundo solo con `gates.G_BOUNDARY` en `state: satisfied` y el hash del primero como evidence— y una nota a deskops por `message send`. Repo dueño: sldb; la única escritura en deskops es el archivo de inbox indicado. Límites: no cambia código; no usa amend; no toca otros gates ni otras partes de deskops.

## AMBIGUEDADES
ninguna

## DRY-RUN
Lecturas hipotéticas: `brief.md`, `alcance.md`, `decisiones.md`, `dag.yaml`, la guía, el texto actual de la pill y la fila D1. Cambios previstos: crear el atom con `deskops add atom` y los tres campos indicados; editar la pill con `deskops edit pill` para enlazarlo en `where` o `how`; commitear ambos; editar únicamente `gates.G_BOUNDARY` con `state: satisfied` y evidence igual al hash del primer commit; commitear; enviar la nota con título y cuerpo de dos párrafos indicados. Dependencias: D1 y D3 registradas, pill ya commiteada y CLI de deskops disponible. Validaciones futuras: `git log` de main muestra ambos commits y el primero es alcanzable; búsqueda del atom en la pill; archivo nuevo en `deskops/desk/inbox` con título exacto y cuerpo con ruta y fila D1; `dag.yaml` muestra el gate satisfecho con evidence válida. No se ejecuta nada.

## FUTURO
La revisión en frío la acepta o dispone quien opera el desk de sldb escribiendo en `reviews/rN.md`. GO02 consume `G_BOUNDARY` como prerrequisito. deskops procesa la nota de inbox en su propio plan; `G_CONSUMER` pertenece a ese plan. Nada de esto es ambigüedad de GO01.
