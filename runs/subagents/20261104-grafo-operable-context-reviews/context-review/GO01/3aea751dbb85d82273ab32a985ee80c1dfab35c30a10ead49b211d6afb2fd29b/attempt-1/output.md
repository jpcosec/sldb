## REFORMULACION
GO01 es un nodo de entrega, no agregado. Su encargo es registrar la decisión de frontera: crear un atom en `desk/atoms`, enlazarlo en la pill, hacer dos commits en `main` de sldb y dejar `gates.G_BOUNDARY` en `satisfied` con el hash del primer commit como `evidence`. Además debe enviar una nota a deskops por el canal sancionado, escribiendo solo en `deskops/desk/inbox`. Repo dueño: sldb. Límites: no cambia código; solo toca los paths de `output_scope`; el segundo commit edita únicamente `gates.G_BOUNDARY`; sin amend; deskops solo recibe la nota.

## AMBIGUEDADES
1. “creado con deskops add atom --title ... --five-wh-one-plus what --answer ..., los tres campos obligatorios del subject atom”. Faltan los valores de `--title` y de `what`; la aceptación solo exige que “el atom aparece en la pill”, no su título ni su `what`. El ejecutor tendría que inventar ambos, aunque el `answer` está orientado por el texto.

## DRY-RUN
Un ejecutor futuro leería GO01, el gate, la pill actual, la fila D1 y el estado de `desk/atoms` e inbox. Crearía el atom, editaría la pill en `where` o `how`, commitearía atom y enlace, editaría solo `gates.G_BOUNDARY` con state `satisfied` y evidence del primer commit, y commitearía de nuevo. Luego ejecutaría `deskops message send --to deskops --kind suggestion` con el título y cuerpo indicados. Dependencias: ninguna; GO01 produce `G_BOUNDARY`. Validaciones futuras: `git log`/ancestría desde `main`, presencia del atom en la pill, archivo nuevo en inbox con título y cuerpo requeridos, y gate con state/evidence correctos.

## FUTURO
GO02 depende de GO01 y requiere `G_BOUNDARY`; no puede empezar hasta que GO01 cierre. La revisión en frío la acepta quien opera el desk de sldb escribiendo su disposición en `reviews/rN.md`. La promoción usa `deskops add task --from-drawer`; la validación corre con pytest en el host que indique el dueño. Nada de esto se ejecuta aquí.
