## REFORMULACION
Encargo ejecutable de tipo `task.code` en el repo `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`): añadir a `NotationDoc` un campo opcional que declare nombre y versión del estándar que implementa la notación; cargarlo desde YAML en `src/sldb/notations/notation_spec.py`; validarlo; mostrarlo al listar/validar con `sldb notations`; documentarlo y cubrirlo con `tests/test_notation_declares_standard.py`. Límites: dentro, modelo, carga y salida; fuera, contenido de notaciones y reglas de cobertura del estándar. Antes debe comprobarse si los tags semánticos ya bastan.

## AMBIGUEDADES
1. “visible al listar y validar” frente a “la salida de `sldb notations`”: no precisa subcomandos ni formato. Obliga a inventar columnas, texto o JSON.
2. “un campo opcional en la notación con el nombre y la versión del estándar”: no fija nombre ni estructura del campo. Obliga a inventar `standard: {name, version}` u otra forma.
3. “Un nombre vacío o una versión sin nombre se rechaza”: no cubre nombre sin versión, versión vacía, espacios ni mensaje exacto. Obliga a inventar la matriz de validación.
4. “comprobar si los tags semánticos de la notación ya pueden llevar el estándar, y elegir el campo solo si no”: no define criterio de suficiencia. Obliga a inventar cuándo los tags bastan.
5. “La documentación de notaciones describe el campo”: no identifica archivo ni sección exactos. Obliga a inventar ubicación y contenido.
6. “python -m pytest -q tests/test_notation_declares_standard.py”: no aclara si el test existe o debe crearse. Obliga a inventar su alcance y fixtures.

## DRY-RUN
Lecturas hipotéticas: `docs/architecture/notations-and-views.md`, `tags.md`, `src/sldb/notations/notation_spec.py`, módulo CLI de `sldb notations` y tests existentes.
Cambios previstos: decidir tags frente a campo; si Procede, ampliar el modelo y el parser YAML; validar combinaciones; exponer el dato en listado/validación; actualizar documentación; crear o ajustar el test indicado.
Dependencias: esquema actual, decisión sobre tags, CLI y pytest.
Validaciones futuras: ejecutar el pytest indicado; probar notación con estándar, sin estándar, nombre vacío y versión sin nombre; revisar salida y documentación. Sin ejecutar nada.

## FUTURO
Un humano debe decidir nombre/estructura del campo, formato de salida y criterio sobre tags; specIR aporta los estándares reales; CI u otro nodo ejecutará las pruebas.
