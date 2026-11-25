## REFORMULACION
Propósito: eliminar la inyección de plantilla en `render_model_markdown`, haciendo que los valores de campos sean datos literales y que solo la plantilla del modelo se evalúe como Jinja. Resultado: roundtrip byte a byte al guardar y extraer; llaves, porcentajes, almohadillas, expresiones, comentarios y bloques de control no alteran ni rompen el render. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: intervenir en `src/sldb/core/renderer_engine/base.py` y, si procede, subclases/llamadores; preservar optrev y líneas ausentes; añadir tests en el archivo existente del renderer; actualizar CHANGELOG; no cambiar la sintaxis de plantillas.

## AMBIGUEDADES
1. «mantener el comportamiento de optrev y de las líneas ausentes»: no define qué es optrev ni cuál es el comportamiento esperado de líneas ausentes; obligaría a inventar casos y semántica.
2. «en un archivo de tests del renderer existente»: no identifica el archivo; obligaría a inventar o descubrir la ruta exacta.
3. «por ejemplo, sustituirlos por variables de Jinja o por tokens que se reemplazan después del render, o escapar el valor con raw»: ofrece varias implementaciones sin criterio de elección; obligaría a decidir sin especificación.
4. «aviso a deskops para que quite su xfail»: no fija canal, formato ni confirmación; obligaría a inventar el procedimiento.
5. «CHANGELOG y commit»: no indica formato de entrada ni mensaje/branch de commit; obligaría a inventar convenciones.

## DRY-RUN
Lecturas: `base.py`, subclases y llamadores de `replace_markers`; tests existentes del renderer; nota de inbox; CHANGELOG. Cambios previstos: separar en `replace_markers` los valores de usuario del código Jinja, eligiendo un mecanismo; añadir tests de roundtrip con dos/tres llaves, expresión, comentario, control y cierre; actualizar CHANGELOG. Dependencias: entorno Jinja, flujo `render_model_markdown`, extracción y fixtures existentes. Validaciones futuras: los cinco comandos de Validation y los tests nuevos. Sin ejecutar nada.

## FUTURO
Otro nodo/ejecutor implementará el cambio y ejecutará las validaciones; CI o revisión humana confirmará el resultado; deskops retirará su xfail tras el aviso; un humano aprobará el commit.
