REFORMULACION

Propósito: impedir que `render_model_markdown` interprete como Jinja los valores de campo aportados por el usuario. Resultado: cada valor se guarda y recupera literal, byte a byte; solo la plantilla del modelo es Jinja; llaves, porcentajes, almohadillas, expresiones, comentarios y bloques de control no alteran ni rompen el render. Repo: `sldb` (`/mnt/ssd/proyectos/SLDB_1`). Superficie: `src/sldb/core/renderer_engine/base.py` (`BaseRenderer.replace_markers`) y `CHANGELOG.md`. Límites: no cambiar la sintaxis de plantillas; conservar el comportamiento de optrev y de líneas ausentes; añadir tests de roundtrip en un archivo de tests del renderer existente. Es una tarea ejecutable, no un agregado.

AMBIGUEDADES

1. «en un archivo de tests del renderer existente»: no nombra el archivo. Obligaría a inventar la ruta y el nombre del test.
2. «aviso a deskops para que quite su xfail»: no indica dónde está el xfail ni el canal o verbo de aviso. Obligaría a inventar el mecanismo y el destinatario operativo.
3. «Los comandos de Validation pasan con los tests nuevos de roundtrip»: la lista de Validation no incluye un comando dirigido al archivo de tests del renderer. Obligaría a decidir si los tests nuevos deben quedar cubiertos por `tests/test_cli_v2.py` o por otro comando no listado.

DRY-RUN

Lecturas: `base.py`, sus subclases, llamadores de `replace_markers`, tests existentes del renderer, `CHANGELOG.md` y la nota de inbox referenciada. Cambios previstos: separar dato y plantilla en `replace_markers`, de modo que los valores no lleguen a Jinja como código; preservar optrev y líneas ausentes; añadir tests de roundtrip con dos y tres llaves de apertura, expresión, comentario Jinja, bloques de control y llaves de cierre; actualizar `CHANGELOG.md`. Dependencias: entorno `uv` con extras `code` y `dev`; conocimiento del archivo de tests correcto. Validaciones futuras: los cinco comandos listados, ejecutados sin ejecutar ahora nada.

FUTURO

Un humano o deskops decide el archivo de tests y retira el xfail tras el aviso; otro nodo ejecuta la implementación, los tests y el commit; el cierre usa `deskops closeout` y actualiza el Board y el CHANGELOG.
