## REFORMULACION
Nodo ejecutable, no agregado. Encargo: producir en el repositorio `sldb` el documento `docs/architecture/command-taxonomy.md` con una tabla aprobable de operaciones, indicando sustantivo, verbo, lectura/escritura, nivel de permiso, nombres actuales en `sldb.api`, CLI, `sldb serve` y `sldb mcp`, más duplicados, huecos, renombres y nombre canónico propuesto. Incluye una prueba que detecte incorporaciones no documentadas. Límites: no renombrar ni mover código, no implementar el servidor fastmcp, no modificar la CLI; es inventario sin cambio de comportamiento.

## AMBIGUEDADES
1. “nivel de permiso”: no se define escala ni fuente; obligaría a inventar categorías y asignaciones.
2. “Una tabla de operaciones que JP pueda aprobar”: no se indica quién aprueba, con qué criterio ni cuándo; obligaría a inventar el circuito de aprobación.
3. “revisar si SurfaceDoc (knowledge/surfaces/) y sldb selfdoc ya guardan y chequean parte de esto”: faltan rutas, API y criterio de reutilización; obligaría a inventar cómo consultarlos y qué cuenta como reutilizable.
4. “Los nombres se sacan del código (sldb.api.__all__, el parser de la CLI, el enrutador de src/sldb/cli/serve, el registro de src/sldb/mcp)”: no se precisan módulos, atributos ni qué es “comando hoja”; obligaría a inventar reglas de extracción.
5. “exactamente una fila, o en una lista final ‘sin operación’ con su motivo”: no se define cuándo un nombre queda “sin operación”; obligaría a inventar ese criterio.
6. “un nombre canónico propuesto”: no hay convención de nombres; obligaría a inventarla.

## DRY-RUN
Lecturas: ADR, `docs/architecture/mcp.md`, `knowledge/surfaces/`, selfdoc, `sldb.api.__all__`, parser CLI, enrutador de `src/sldb/cli/serve` y registro de `src/sldb/mcp`.
Cambios previstos: crear el documento y `tests/test_command_taxonomy.py`.
Dependencias: registros y rutas citadas, formats de SurfaceDoc/selfdoc.
Validaciones futuras: ejecutar `python -m pytest -q tests/test_command_taxonomy.py`; comprobar cobertura exacta y clasificación lectura/escritura.

## FUTURO
JP decide la aprobación, los niveles de permiso y los nombres canónicos. El servidor fastmcp y el compositor de interfaces consumen después la taxonomía. Renombrar o mover código queda para nodos posteriores.
