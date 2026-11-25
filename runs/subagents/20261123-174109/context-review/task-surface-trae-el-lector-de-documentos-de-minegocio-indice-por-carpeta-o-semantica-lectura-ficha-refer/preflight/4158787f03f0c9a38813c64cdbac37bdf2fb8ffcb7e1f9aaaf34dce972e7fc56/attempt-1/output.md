REFORMULACION
Encargo ejecutable de código: portar la parte genérica del lector de documentos de la copia de surface de minegocio (reports/lector-minegocio-20261123/superficie) al repo sldb/surface. Resultado: índice por carpeta o semántica, lectura, ficha, referencias y rechazos legibles, contra sldb serve sobre el store real de deskops. Límites: fuera textos, rutas y datos de minegocio; se portan core/{doc-ref,wiki-index,rechazo,imagenes}.ts con tests y fixture, workbench/{WikiIndex,Ficha,NuevaPagina,AvisoGuardado}.tsx, WikiLectura.test y los cambios genéricos enumerados. WorkbenchShell.tsx, vite.config.ts y tsconfig son trabajo local de JP: no tocarlos sin señalarlo en el informe. Cierre: tsc, vitest y check-layers pasan; informe con archivos portados/excluidos, motivos y tiempos por pantalla.

AMBIGUEDADES
1. "indice por carpeta o por semantica": no aclara si son modos conmutables o alternativas; obliga a inventar UX y criterio de selección.
2. "dejar la semantica conectada": no define el estado si falta la dependencia; obliga a inventar si queda visible, deshabilitada o solo en código.
3. "medir el tiempo de carga de cada pantalla": sin método, condiciones frío/caliente, repeticiones ni umbral; obliga a inventar medición y aceptación.
4. "cambios genericos": sin criterio para separar genérico de específico; obliga a inventar la clasificación.
5. "funciona contra sldb serve sobre el store real de deskops": sin configuración, puerto ni forma de arranque; obliga a inventar el entorno.
6. "sin cambios o con el cambio senalado": no aclara si exige aprobación previa o solo mención posterior; obliga a inventar el gate.

DRY-RUN
Lecturas: taskdoc, sugerencia, diff fuente/surface, package.json, tests y componentes. Cambios: añadir ficheros core, workbench y react enumerados, imports, estilos, fixture y tests; sin tocar los tres archivos de JP salvo marcarlos. Dependencias: tarea de tags de deskops, sldb serve/store disponibles, rama de surface. Validaciones futuras: tsc, vitest, check-layers, arranque y cronometraje de índice, lectura y ficha. Nada ejecutado.

FUTURO
El coordinador decide autorizar cambios en WorkbenchShell.tsx, vite.config.ts o tsconfig y avisa a JP. La tarea de tags de deskops decide el agrupado semántico. Un humano valida tiempos y excluidos; el merge final es del coordinador.
