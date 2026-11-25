## REFORMULACION
Encargo: hacer que la puerta de identidad acepte el directorio `workbench_demo/` versionado en la raíz, que hoy no está clasificado en `contracts/identity.toml` y provoca rc 1 en `bash tools/check.sh --fast`. Resultado: `workbench_demo/` clasificado con categoría adecuada a store demo de superficie (o la que el contrato prevea para fixtures/demos) más una nota del porqué; `tools/check.sh --fast` en rc 0. Repo: este repo SLDB. Límites: solo `contracts/identity.toml` y, si la puerta lo exige, `tools/check_identity.py` y su test; no mover ni borrar `workbench_demo/` (lo usa el tour). Tipo `task.code`, ejecutable por un ejecutor futuro.

## AMBIGUEDADES
1. "con la categoria que corresponda a un store de demo de la superficie" — el input no enumera las categorías existentes ni su semántica; obliga a inventar cuál encaja o a decidir si crear una nueva.
2. "si la puerta lo necesita" — no se especifica qué condición observable autoriza tocar `check_identity.py`/test; obliga a inventar el criterio.
3. "con una nota de por que existe" — no se define formato ni ubicación (comentario TOML, campo, doc); obliga a inventar la representación.
4. "bash tools/check.sh --fast sale con rc 0 en main" — no se aclara si se exige ejecutar en la rama `main` o basta el árbol de trabajo; obliga a inventar el entorno de validación.
5. `summary` y `tags` vacíos, `history`/`references`/`depends_on` vacíos — no aporta contexto sobre estado previo del commit 562847e2; obliga a asumir que nada más bloquea.

## DRY-RUN
Lecturas: `tools/check_identity.py`, `contracts/identity.toml`, `tools/check.sh`, test de identidad, contenido de `workbench_demo/`. Cambios previstos: añadir entrada de clasificación (y regla si procede) en `contracts/identity.toml` con nota; opcionalmente ajustar `check_identity.py` y su test. Dependencias: esquema de categorías existente y lógica de la puerta. Validaciones futuras: `bash tools/check.sh --fast` rc 0 y revisión de que la nota describe el origen del directorio.

## FUTURO
El ejecutor decide la categoría final y el formato de la nota. Un humano confirma si crear categoría nueva es aceptable. Otro nodo/CI valida el rc 0 en `main`.
