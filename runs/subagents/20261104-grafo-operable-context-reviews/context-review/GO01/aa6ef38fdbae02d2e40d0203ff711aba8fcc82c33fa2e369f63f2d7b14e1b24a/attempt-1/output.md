REFORMULACION
Propósito: registrar en sldb la frontera reencuadrada por D1 con un commit en main que incluya la pill ya editada y un atom nuevo; el atom declara que sldb evalúa reglas declaradas sobre documentos, aristas y hashes y que los consumidores las autoran como documentos. La pill enlaza el atom. En el mismo commit, G_BOUNDARY pasa a satisfied con el hash de commit como evidence. Además, nota a deskops vía `deskops message send --to deskops --kind suggestion` desde sldb, con título indicado y cuerpo con ruta del plan y D1; único contacto con deskops. Resultado: commit en main, atom enlazado, gate satisfecho y archivo en deskops/desk/inbox. Repo dueño: sldb. Límites: no cambia código; output_scope acotado a pill, desk/atoms, gates.G_BOUNDARY y deskops/desk/inbox.

AMBIGUEDADES
1. "creado con deskops add atom, five_wh_one_plus what": solo se fija el contenido de "what"; si el esquema exige why/who/when/where/how, el ejecutor debe inventarlos.
2. "el hash se conoce al amend o se cita el commit anterior; cualquiera de las dos formas vale si el hash citado contiene la pill y el atom" frente a "git log de main de sldb muestra un commit... evidence con un hash": no se aclara si el hash citado debe ser alcanzable desde main; con amend puede quedar huérfano.
3. "cuerpo con la ruta del plan y D1": no se fija si D1 se cita por id, fila completa o paráfrasis; el ejecutor inventa el texto.

DRY-RUN
Lecturas: pill en desk/contexts/, decisiones.md (D1), dag.yaml gates.G_BOUNDARY, contrato de deskops add atom y message send. Cambios: crear atom en desk/atoms; editar la pill para enlazarlo; editar solo gates.G_BOUNDARY en dag.yaml; enviar la nota. Dependencias: git en main de sldb, CLI deskops, checkout de sldb. Validaciones futuras: git log muestra commit con pill y atom; atom visible en la pill; archivo nuevo en inbox con el título; gate satisfied con evidence hash.

FUTURO
GO02 consume G_BOUNDARY para fijar semántica; deskops decide qué hace con la suggestion; un humano o revisor en frío valida el commit y, si se exige alcanzabilidad, resuelve amend frente a commit anterior.
