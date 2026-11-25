REFORMULACION
Propósito: añadir una API pública de lectura, `sldb.api.template_anchors(model_type) -> dict[str, str]`, que devuelva por campo el párrafo ancla literal de su plantilla, reutilizando las recetas del extractor. Resultado: módulo `src/sldb/api/model_registry/template_anchors.py`, exportación en `sldb.api`, tests en `tests/test_literal_paragraph_anchor.py`, entrada en `CHANGELOG.md` e informe en `runs/subagents/<run-dir>/result-summary.md`. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: no implementar la opción (b), no cambiar render/extract, no tocar deskops salvo el aviso, no hacer push; el commit lo hace el coordinador.

AMBIGUEDADES
1. “párrafo literal (texto sin marcadores)” frente a “con sus delimitadores de cursiva”: obliga a decidir si “sin marcadores” excluye solo marcadores de campo o también la cursiva; el ejemplo solo aclara parcialmente.
2. “inmediatamente anterior al marcador del campo dentro de la misma sección”: no define si líneas en blanco, comentarios u otro párrafo intermedio rompen la inmediatez; obliga a fijar un criterio si la receta no lo resuelve.
3. “texto exacto… sin espacios al final”: no dice nada de espacios iniciales ni normalización interna; obliga a inventar si se recorta el inicio.
4. “con cualquier otra cosa lanza TypeError”: no fija mensaje ni si acepta subclases; obliga a decidir texto y validación.
5. “la misma llamada que hace Validator(model).extract”: no nombra la función exacta; obliga a inferirla leyendo el archivo.

DRY-RUN
Lecturas: `src/sldb/core/template_extractor.py`, `src/sldb/runtime/validation.py` (65-68), `tests/test_literal_paragraph_anchor.py`, `CHANGELOG.md` y `src/sldb/api/__init__.py`. Cambios previstos: módulo nuevo, exportación, tests y changelog. Dependencias: recetas/anchor del extractor y helpers de test existentes o `sldb.api` con `tmp_path`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_literal_paragraph_anchor.py`, `bash tools/check.sh --fast` y comprobación de importación. Sin ejecutar.

FUTURO
El ejecutor implementará y reportará; el coordinador revisará, hará el commit con `deskops closeout commit` y gestionará el aviso a deskops. deskops decidirá el consumo posterior de la API.
