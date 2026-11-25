REFORMULACION

Propósito: exponer una API pública de solo lectura para que deskops sepa qué párrafo literal ancla cada campo de la plantilla de un modelo y no lo guarde como valor. Resultado: `sldb.api.template_anchors(model_type) -> dict[str, str]`, que devuelve por campo el texto exacto del párrafo ancla; los campos sin ancla no aparecen. Debe exportarse desde `sldb.api`, cubrirse con tests en `tests/test_literal_paragraph_anchor.py` y documentarse en `CHANGELOG.md`. Repo: `/mnt/ssd/proyectos/SLDB_1` (`sldb`). Límites: no cambia render ni extract, no implementa la opción (b), no toca deskops; solo deja aviso al cerrar. Es una tarea de código ejecutable.

AMBIGUEDADES

1. «va precedido por un párrafo literal que ancla su extracción»: no define adyacencia (inmediato, mismo contenedor, varios párrafos). Obliga a inventar el criterio de asociación.
2. «el texto exacto de ese párrafo tal como render lo escribe y extract lo consume»: no aclara si incluye delimitadores de cursiva (`_..._`), ni trim/saltos; además render y extract podrían diferir. Obliga a inventar la normalización.
3. «dos campos anclados por párrafos en cursiva»: no dice si el valor esperado conserva los `_`. Obliga a inventar la expectativa del test.
4. «model_type»: no especifica si es clase, instancia o nombre. Obliga a inventar el contrato de entrada y errores.
5. Ruta `src/sldb/api/model_registry/template_anchors.py` frente a `from sldb.api import template_anchors`: no dice si hay reexport o dónde vive el módulo. Obliga a inventar la estructura de exports.
6. «usa las mismas recetas que el extractor (TemplateExtractor y el split de nodos), sin reimplementar el parseo»: no indica métodos ni cómo obtener las recetas. Obliga a inventar llamadas internas.
7. «aviso a deskops con deskops message send --to deskops»: no fija el contenido del mensaje.
8. «CHANGELOG.md»: no fija redacción ni formato de la entrada.

DRY-RUN

Un ejecutor leería `template_extractor.py`, `validation.py` (65-68), `test_literal_paragraph_anchor.py`, `git show 9dcabd9a` y los `__init__` de API. Crearía el módulo, el export, tests y la entrada de CHANGELOG. Dependencias: entorno Python, pytest, `tools/check.sh`. Validaría con `TMPDIR=/dev/shm pytest -q tests/test_literal_paragraph_anchor.py`, `bash tools/check.sh --fast` y la importación pública. Sin ejecutar nada.

FUTURO

Deciden/producen otros: el commit; el contenido del aviso a deskops; la revisión humana de la redacción del CHANGELOG y de la adopción de la API por deskops.
