## REFORMULACION

Encargo: añadir a la NotationDoc un campo **opcional** que declare nombre y versión del estándar que implementa (UML, BPMN, IFML, ORCA), cargarlo desde YAML en `src/sldb/notations/notation_spec.py` y exponerlo en la salida de `sldb notations` (listar y validar). Repo: `sldb`. Límites: fuera el contenido de las notaciones (propiedad de specIR) y cualquier regla de cobertura del estándar; dentro solo modelo, carga y salida de CLI. Resultado observable: notación con estándar se valida y lo muestra; sin él sigue válida; nombre vacío o versión sin nombre se rechaza nombrando el campo; documentación de notaciones describe el campo. Validación: `python -m pytest -q tests/test_notation_declares_standard.py`.

## AMBIGUEDADES

1. "comprobar si los tags semánticos de la notación ya pueden llevar el estándar, y elegir el campo solo si no" — el input no dice qué criterio decide que los tags no bastan; obliga a inventar el umbral de decisión y el resultado de la comprobación.
2. "el nombre y la versión del estándar" — no define forma del campo (anidado vs plano), nombre exacto ni si la versión es libre o semver; obliga a inventar contrato YAML.
3. "una versión sin nombre se rechaza" — no aclara si nombre sin versión es válido; obliga a inventar esa mitad de la regla.
4. "validado y visible al listar y validar" — no especifica formato de salida ni si el campo aparece vacío/ausente; obliga a inventar presentación de CLI.
5. "tests/test_notation_declares_standard.py" — no consta que exista; el input no dice si se crea o ya existe.
6. `depends_on: []` frente a "Pedido de specIR (desk/drawer/plans/...)" — no queda fijada dependencia formal.

## DRY-RUN

Lecturas: `docs/architecture/notations-and-views.md`, `tags.md`, `src/sldb/notations/notation_spec.py`, tests de notaciones, `sldb notations` CLI. Cambios previstos: modelo NotationDoc + parser YAML + render de listado/validación + doc + test. Dependencias: decisión tags-vs-campo (ambigüedad 1). Validaciones futuras: pytest nombrado, más suite completa si cambia comportamiento compartido, stores check/check.sh si toca store.

## FUTURO

Un humano/specIR decide el criterio tags-vs-campo y el contrato YAML del campo; otro nodo crea el test y actualiza docs; closeout commitea atómicamente y retira la tarea del Board.
