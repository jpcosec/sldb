REFORMULACION
GO01 es un nodo de decisión/entrega, no un agregado ni un paquete con hijos. Registra la frontera D1: crea un atom en `desk/atoms`, lo enlaza desde la pill en `where` o `how`, hace dos commits en `main` —el primero con atom y pill, el segundo solo con `gates.G_BOUNDARY` en `dag.yaml` a `satisfied` y el hash del primero como evidence— y envía una nota a `deskops/desk/inbox` con el canal `deskops message send`. Resultado: atom, pill enlazada, gate satisfecho y nota con ruta del plan y fila D1. Repo dueño: `sldb`; única escritura externa: inbox de deskops vía `message send`. Límites: no cambia código, no usa amend y solo toca `output_scope`.

AMBIGUEDADES
1. «los tres campos obligatorios del subject atom; el what es el título»: se nombran `what` y `--answer`, pero no el tercer campo obligatorio ni su valor. El ejecutor tendría que inventar el nombre y contenido de ese campo para crear el atom.

DRY-RUN
Lecturas: `dag.yaml` (GO01 y `G_BOUNDARY`), texto actual de la pill, fila D1 de `decisiones.md`, esquema de atom y de mensaje a deskops. Cambios previstos: crear atom; editar pill para enlazarlo en `where` o `how`; commit 1; editar solo `gates.G_BOUNDARY` con `state: satisfied` y evidence con el hash del commit 1; commit 2; enviar nota a deskops con título y cuerpo de dos párrafos. Dependencias: ninguna (`depends_on: []`, `requires: []`). Validaciones futuras: dos commits alcanzables desde `main`, ausencia de amend, atom existente y visible en la pill, archivo nuevo en inbox con título y cuerpo indicados, y gate con estado y hash correctos.

FUTURO
GO02 depende de GO01 y del gate `G_BOUNDARY`; no debe ejecutarse hasta que GO01 cierre. El operador del desk de sldb promueve el nodo y verifica commits; deskops recibe y dispone la nota. La revisión no ejecuta ni decide la disposición humana.
