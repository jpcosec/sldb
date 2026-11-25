## REFORMULACION
Propósito: ajustar el guard de sobrescritura con pérdida para que no rechace perder encabezados no declarados cuyo contenido sobreviva en el texto nuevo. Resultado: cambio en `src/sldb/api/documents/lossy_overwrite.py`, tests de aceptación/rechazo y CHANGELOG. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: dentro el guard, su test y CHANGELOG; fuera la política `structural_noise` y otros guards. Es un nodo ejecutable `task.code`, no un agregado.

## AMBIGUEDADES
1. “cada encabezado no declarado que se pierde tiene su contenido … presente en el texto renderizado nuevo”: no define frontera del contenido, comparación exacta/subcadena, mayúsculas, Unicode ni Markdown. Obligaría a inventar el algoritmo.
2. “normalizado en espacios”: no aclara colapsar saltos, recortar extremos, normalizar Unicode ni quitar marcas. Obligaría a inventar la normalización.
3. “en el valor de algún campo o como párrafo”: no define cómo localizar valores de campos en el texto renderizado ni qué cuenta como párrafo. Obligaría a inventar la detección.
4. “Un test cubre los dos casos” frente a p1/p2: no aclara si son uno o dos tests ni sus nombres. Obligaría a inventar la estructura.
5. “pasa por 'sldb fields set' o 'deskops edit atom'”: no elige comando ni exige validarlo. Obligaría a inventar el criterio CLI.
6. “commit desde el worktree que dispatch te da”: el input no incluye ruta ni worktree. Obligaría a inventar su ubicación.
7. “La puerta 'identidad' … es la excepción autorizada (f055723d)”: no fija alcance ni vigencia. Obligaría a inventar cómo aplicarla.

## DRY-RUN
Un ejecutor leería el TaskDoc, `lossy_overwrite.py:18`, el renderizado de campos, tests de lossy y `tests/api`, y CHANGELOG. Planificaría: test fallido para encabezado perdido con contenido presente; test de rechazo si falta; implementación de comparación normalizada cuerpo-encabezado vs texto renderizado; actualización de tests/CHANGELOG. Dependencias: worktree de dispatch, API de documentos/render, pytest, git y `check.sh`. Validaría luego con pytest dirigido y `tests/api -n 4`; commit con `Task-Id`; `check.sh --fast` con excepción de identidad.

## FUTURO
Dispatch entrega worktree e id; un humano u otro nodo confirma la vigencia de la excepción `f055723d` y revisa el commit; CI valida la suite.
