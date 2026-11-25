## REFORMULACION

Propósito: alinear `label_key` con `normKey` del catálogo haciendo que `_` cuente como separador. Resultado: `label_key("post_published")` devuelve `"post published"` y la clave coincide con `normKey` para letras, dígitos, espacios, guiones bajos y puntuación. Repo: `/mnt/ssd/proyectos/SLDB_1`. Superficie: `src/sldb/api/matching/atom_keys.py`, `tests/matching/test_matching_explicit.py`, `CHANGELOG.md`. Límites: no tocar `normalize_key` ni `_title_aliases`, ni la plantilla JS del catálogo (repo IR), ni el emparejamiento difuso, ni la otra tarea citada.

## AMBIGUEDADES

1. "Entrada en CHANGELOG.md": no indica sección, versión ni formato; obligaría a inventar dónde y cómo redactarla.
2. "commit con esos archivos": no especifica mensaje, rama ni si el commit corresponde al ejecutor; obligaría a inventar la convención.
3. "ajustar el golden solo si el cambio es exactamente la separación de \"_\"": no define cómo comprobar "exactamente" ni qué hacer si el cambio no lo es; obligaría a inventar el criterio de verificación y la decisión de abortar o reportar.
4. "label_key produce la misma clave que normKey para letras, dígitos, espacios, guiones bajos y puntuación": no aclara otros caracteres Unicode (símbolos, emoji) ni si la equivalencia se limita a los cuatro pares listados; obligaría a inventar el alcance real.

## DRY-RUN

Lecturas: `atom_keys.py` (label_key, líneas 14-16), `grep "label_key"` en `src/sldb`, `tests/matching/test_matching_explicit.py`, goldens de matching y `CHANGELOG.md`. Cambios previstos: regex a `re.sub(r"[\W_]+", " ", texto)` conservando minúsculas, colapso y strip; dos tests nuevos (caso simple y parametrizado con los cuatro pares); entrada de changelog. Dependencias: pipeline actual de `label_key`, `normKey` como referencia no editable y pytest. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/matching/`, inspección de diffs en goldens y comprobación de `label_key("post_published") == "post published"`. Nada ejecutado.

## FUTURO

Otro nodo ejecutará la edición y los tests; un humano o política de repo decidirá mensaje/rama del commit y la aceptación del cambio de goldens. La revisión/CI y la confirmación de IR13b de que el átomo se localiza en el navegador quedan fuera de este nodo.
